#!/usr/bin/env python3
"""Collect candidate radiograph figures per entity from open-access articles in Europe PMC.

Runs on a GitHub Actions runner. Keeps only articles whose licence (read from the article XML) is
CC BY, CC BY-SA or CC0, and only figures whose caption mentions a radiograph. Writes
candidates_pmc/manifest.json, candidates_pmc/thumbs/<entity>/NN.jpg and candidates_pmc/sheets/<entity>.jpg.
Candidates are not approvals; the owner chooses the final images.
"""
import io, json, pathlib, re, shutil, sys, time, urllib.error, urllib.parse, urllib.request
import xml.etree.ElementTree as ET
from PIL import Image
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from fetch_commons import sheet  # same contact-sheet layout

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "candidates_pmc"
REST = "https://www.ebi.ac.uk/europepmc/webservices/rest"
UA = "TumTulCandidateBot/0.2 (https://github.com/harmenreza/TumTul; educational bone-tumour reference app)"
XL = "{http://www.w3.org/1999/xlink}href"
MAX_ARTICLES, MAX_FIGS = 40, 25
XRAY = re.compile(r"radiograph|x-?ray|plain film|roentgenogra|radiography", re.I)
OTHER = re.compile(r"\bMRI\b|magnetic resonance|\bCT\b|computed tomograph|T1|T2|STIR|scintigra|bone scan|PET|histolog|H&E|hematoxylin|haematoxylin|microscop|immunohisto|intraoperative|gross", re.I)
OK_LIC = re.compile(r"creativecommons\.org/(licenses/(by|by-sa)/|publicdomain/zero/)", re.I)

def _open(url, kind):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                b = r.read()
                return json.loads(b) if kind == "json" else b
        except urllib.error.HTTPError as e:
            if e.code in (401, 403, 404, 410): return None   # not retryable
            wait = int(e.headers.get("Retry-After") or 0) or min(120, 8 * 2 ** attempt)
            print(f"retry {attempt} {e.code} {url[:90]}", file=sys.stderr); time.sleep(wait)
        except Exception as e:
            print(f"retry {attempt} {e}", file=sys.stderr); time.sleep(8 * (attempt + 1))
    return None

def text(el):
    return re.sub(r"\s+", " ", "".join(el.itertext())).strip() if el is not None else ""

def search(term):
    q = f'(TITLE_ABS:"{term}") AND OPEN_ACCESS:y AND HAS_FT:y AND (LICENSE:"cc by" OR LICENSE:"cc-by" OR LICENSE:"cc by-sa" OR LICENSE:"cc0")'
    url = f"{REST}/search?" + urllib.parse.urlencode({"query": q, "format": "json", "pageSize": 40, "resultType": "lite", "sort": "CITED desc"})
    d = _open(url, "json") or {}
    return [r for r in (d.get("resultList") or {}).get("result", []) if r.get("pmcid")]

def figures(pmcid):
    b = _open(f"{REST}/{pmcid}/fullTextXML", "bytes")
    if not b: return None, []
    try: root = ET.fromstring(b)
    except ET.ParseError: return None, []
    lic = root.find(".//permissions/license")
    lic_url = (lic.get(XL) if lic is not None else "") or ""
    if not lic_url:
        ali = root.find(".//{http://www.niso.org/schemas/ali/1.0/}license_ref"); lic_url = text(ali)
    meta = {"licence_url": lic_url, "licence_text": text(lic)[:300],
            "journal": text(root.find(".//journal-title")), "year": text(root.find(".//pub-date/year")),
            "article_title": text(root.find(".//article-title"))[:300],
            "doi": text(root.find(".//article-id[@pub-id-type='doi']")),
            "authors": [f"{text(c.find('name/surname'))} {text(c.find('name/given-names'))[:1]}".strip()
                        for c in root.findall(".//contrib-group/contrib[@contrib-type='author']")][:6]}
    figs = []
    for f in root.iter("fig"):
        g = f.find(".//graphic")
        if g is None or not g.get(XL): continue
        cap = text(f.find("caption")); label = text(f.find("label"))
        figs.append({"label": label, "caption": cap[:700], "graphic": g.get(XL),
                     "xray": bool(XRAY.search(cap)), "other": bool(OTHER.search(cap))})
    return meta, figs

def licence_name(u):
    m = re.search(r"licenses/(by(?:-sa)?)/([0-9.]+)", u or "")
    if m: return f"CC {m.group(1).upper()} {m.group(2)}"
    return "CC0 1.0" if "publicdomain/zero" in (u or "") else ""

S3 = "https://pmc-oa-opendata.s3.amazonaws.com"
_s3_cache = {}
def s3_files(pmcid):
    """Keys in the public PMC Open Access bucket for an article (all versions)."""
    if pmcid not in _s3_cache:
        b = _open(f"{S3}/?" + urllib.parse.urlencode({"list-type": "2", "prefix": f"{pmcid}.", "max-keys": "1000"}), "bytes") or b""
        _s3_cache[pmcid] = re.findall(r"<Key>([^<]+)</Key>", b.decode("utf-8", "ignore"))
    return _s3_cache[pmcid]

def image_url(pmcid, graphic):
    base = graphic.split("/")[-1]
    stem = base.rsplit(".", 1)[0] if re.search(r"\.(jpe?g|png|gif|tiff?)$", base, re.I) else base
    keys = [k for k in s3_files(pmcid) if k.split("/")[-1].rsplit(".", 1)[0] == stem and re.search(r"\.(jpe?g|png|gif)$", k, re.I)]
    keys.sort(key=lambda k: (not k.lower().endswith((".jpg", ".jpeg")), k), reverse=False)
    # newest article version last in lexical order -> prefer it
    keys.sort(key=lambda k: k.split("/")[0], reverse=True)
    return f"{S3}/{keys[0]}" if keys else None

def run_entity(ent, terms, manifest):
    arts, seen = [], set()
    for t in terms:
        for r in search(t):
            if r["pmcid"] not in seen: seen.add(r["pmcid"]); arts.append(r)
        time.sleep(1)
    cands = []
    for a in arts[:MAX_ARTICLES]:
        meta, figs = figures(a["pmcid"]); time.sleep(1)
        if not meta or not OK_LIC.search(meta["licence_url"] or ""): continue
        for f in figs:
            if not f["xray"]: continue
            cands.append({**f, **meta, "pmcid": a["pmcid"], "licence": licence_name(meta["licence_url"]),
                          "article_url": f"https://europepmc.org/article/PMC/{a['pmcid'][3:]}",
                          "image": image_url(a["pmcid"], f["graphic"])})
    cands.sort(key=lambda c: c["other"])          # radiograph-only captions first
    cands = cands[:MAX_FIGS]
    tdir = OUT / "thumbs" / ent; shutil.rmtree(tdir, ignore_errors=True); tdir.mkdir(parents=True, exist_ok=True)
    keep, paths = [], []
    for c in cands:
        if not c["image"]: continue
        b = _open(c["image"], "bytes"); time.sleep(0.5)
        if not b: continue
        try:
            im = Image.open(io.BytesIO(b)).convert("RGB"); im.thumbnail((1200, 1200))
        except Exception: continue
        n = len(keep) + 1; p = tdir / f"{n:02d}.jpg"; im.save(p, quality=85)
        c["n"] = n; c["file"] = str(p.relative_to(ROOT)); keep.append(c); paths.append(p)
    if paths:
        (OUT / "sheets").mkdir(parents=True, exist_ok=True); sheet(paths, OUT / "sheets" / f"{ent}.jpg")
    manifest[ent] = keep
    print(f"{ent}: {len(keep)} figures from {len(arts)} articles")

def main(only=None):
    q = {k: v for k, v in json.loads((ROOT / "tools/pmc_queries.json").read_text(encoding="utf-8")).items() if not k.startswith("_")}
    OUT.mkdir(exist_ok=True)
    mp = OUT / "manifest.json"; manifest = json.loads(mp.read_text()) if mp.exists() else {}
    for ent, terms in q.items():
        if only and ent not in only: continue
        if not only and len(manifest.get(ent, [])) >= 8: print(f"{ent}: kept existing"); continue
        try: run_entity(ent, terms, manifest)
        except Exception as e: print(f"{ent}: FAILED {e}", file=sys.stderr)
        mp.write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")

if __name__ == "__main__":
    main(set(sys.argv[1:]) or None)
