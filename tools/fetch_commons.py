#!/usr/bin/env python3
"""Collect candidate example radiographs per entity from Wikimedia Commons.

Runs on a GitHub Actions runner (network access to Commons). For each entity in
tools/commons_queries.json it searches the File namespace, keeps only files under a
free licence that allows reuse in a free app (CC0, public domain, CC BY, CC BY-SA),
downloads a 640 px thumbnail, and writes:

  candidates/manifest.json         one record per candidate with full attribution metadata
  candidates/thumbs/<entity>/NN.jpg
  candidates/sheets/<entity>.jpg   numbered contact sheet for screening

Nothing here is an approval: the owner chooses the final three per entity in data/images.json.
"""
import html, io, json, pathlib, re, sys, time, urllib.parse, urllib.request
from PIL import Image, ImageDraw

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "candidates"
API = "https://commons.wikimedia.org/w/api.php"
UA = "TumTul-reference-app/0.1 (educational bone-tumour reference; candidate collection script)"
PER_QUERY, MAX_PER_ENTITY = 25, 15
OK_LICENCE = re.compile(r"^(cc0|public domain|pd|cc by(-sa)? [0-9.]+( [a-z]+)?)$", re.I)
NOT_XRAY = re.compile(r"histolog|micrograph|\bH&E\b|\bHE\b|stain|immunohisto|mikroskop|patholog|gross|specimen|präparat|"
                      r"\bMRI\b|\bMRT\b|\bT1\b|\bT2\b|\bSTIR\b|\bCT\b|computed tomograph|PET|scintigra|szintigra|bone scan|"
                      r"canine|dog|\bcat\b|hund|katze|horse|pferd|photo of patient|clinical photo", re.I)

def get(params):
    q = urllib.parse.urlencode({**params, "format": "json", "formatversion": "2"})
    req = urllib.request.Request(f"{API}?{q}", headers={"User-Agent": UA})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except Exception as e:
            print("retry", attempt, e, file=sys.stderr); time.sleep(3 * (attempt + 1))
    raise RuntimeError("Commons API failed")

def plain(s, n=500):
    s = re.sub(r"<[^>]+>", " ", s or ""); s = html.unescape(re.sub(r"\s+", " ", s)).strip()
    return s[:n]

def search(term):
    d = get({"action": "query", "generator": "search", "gsrnamespace": 6, "gsrlimit": PER_QUERY,
             "gsrsearch": f"{term} filetype:bitmap", "prop": "imageinfo|categories", "cllimit": 50, "clshow": "!hidden",
             "iiprop": "url|size|mime|extmetadata", "iiurlwidth": 640})
    return (d.get("query") or {}).get("pages", [])

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()

def sheet(paths, dest):
    W, H, cols = 320, 320, 5
    rows = (len(paths) + cols - 1) // cols
    canvas = Image.new("RGB", (W * cols, H * rows), "white"); d = ImageDraw.Draw(canvas)
    for i, p in enumerate(paths):
        im = Image.open(p).convert("RGB"); im.thumbnail((W - 8, H - 28))
        x, y = (i % cols) * W, (i // cols) * H
        canvas.paste(im, (x + (W - im.width) // 2, y + 24))
        d.rectangle([x, y, x + 40, y + 22], fill="black"); d.text((x + 6, y + 5), f"{i + 1:02d}", fill="white")
    canvas.save(dest, quality=82)

def main(only=None):
    queries = {k: v for k, v in json.loads((ROOT / "tools/commons_queries.json").read_text(encoding="utf-8")).items() if not k.startswith("_")}
    manifest = json.loads((OUT / "manifest.json").read_text()) if (OUT / "manifest.json").exists() else {}
    for ent, terms in queries.items():
        if only and ent not in only: continue
        seen, recs = set(), []
        for t in terms:
            for p in search(t):
                if p["title"] in seen or not p.get("imageinfo"): continue
                seen.add(p["title"]); ii = p["imageinfo"][0]; md = ii.get("extmetadata", {})
                val = lambda k: (md.get(k) or {}).get("value", "")
                lic = plain(val("LicenseShortName"), 60)
                text = " ".join([p["title"], plain(val("ImageDescription")), " ".join(c["title"] for c in p.get("categories", []))])
                rec = {"title": p["title"], "page": ii.get("descriptionurl"), "original": ii.get("url"), "thumb": ii.get("thumburl"),
                       "width": ii.get("width"), "height": ii.get("height"), "mime": ii.get("mime"),
                       "licence": lic, "licence_url": plain(val("LicenseUrl"), 200), "artist": plain(val("Artist"), 200),
                       "credit": plain(val("Credit"), 300), "description": plain(val("ImageDescription")),
                       "date": plain(val("DateTimeOriginal"), 40), "attribution_required": val("AttributionRequired"),
                       "categories": [c["title"] for c in p.get("categories", [])][:15], "query": t,
                       "flag_not_radiograph": bool(NOT_XRAY.search(text)), "licence_ok": bool(OK_LICENCE.match(lic))}
                recs.append(rec)
            time.sleep(0.5)
        # radiographs with a free licence first; drop anything not freely licensed
        recs = [r for r in recs if r["licence_ok"] and r["mime"] in ("image/jpeg", "image/png", "image/gif")]
        recs.sort(key=lambda r: (r["flag_not_radiograph"],))
        recs = recs[:MAX_PER_ENTITY]
        tdir = OUT / "thumbs" / ent; tdir.mkdir(parents=True, exist_ok=True); paths = []
        for i, r in enumerate(recs, 1):
            try:
                b = fetch(r["thumb"] or r["original"]); im = Image.open(io.BytesIO(b)).convert("RGB")
                p = tdir / f"{i:02d}.jpg"; im.save(p, quality=85); r["n"] = i; r["file"] = str(p.relative_to(ROOT)); paths.append(p)
            except Exception as e:
                r["error"] = str(e)
            time.sleep(0.3)
        recs = [r for r in recs if "file" in r]
        if paths:
            (OUT / "sheets").mkdir(parents=True, exist_ok=True); sheet(paths, OUT / "sheets" / f"{ent}.jpg")
        manifest[ent] = recs
        print(f"{ent}: {len(recs)} candidates")
        (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")

if __name__ == "__main__":
    main(set(sys.argv[1:]) or None)
