#!/usr/bin/env python3
"""Download full-resolution originals for the selected example images (tools/image_picks.json).

Commons: the original file (or a 2560 px rendition if the original is larger than 25 MB).
PMC: the largest image file for the figure in the public PMC Open Access S3 bucket.
Writes hires/<entity>/<n>.<ext> and hires/manifest.json (pixel size per image). Runs on GitHub Actions.
"""
import io, json, pathlib, re, sys, time, urllib.parse
from PIL import Image
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from fetch_commons import _open as c_open, get as c_get, UA
from fetch_pmc import _open as p_open, S3

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "hires"
Image.MAX_IMAGE_PIXELS = 200_000_000

def commons_original(title):
    d = c_get({"action": "query", "titles": title, "prop": "imageinfo", "iiprop": "url|size", "iiurlwidth": 2560})
    ii = d["query"]["pages"][0]["imageinfo"][0]
    return ii["url"] if ii.get("size", 0) < 25_000_000 else ii.get("thumburl") or ii["url"]

def s3_best(pmcid, graphic):
    b = p_open(f"{S3}/?" + urllib.parse.urlencode({"list-type": "2", "prefix": f"{pmcid}.", "max-keys": "1000"}), "bytes") or b""
    txt = b.decode("utf-8", "ignore")
    items = re.findall(r"<Key>([^<]+)</Key>.*?<Size>(\d+)</Size>", txt, re.S)
    base = graphic.split("/")[-1]; stem = re.sub(r"\.(jpe?g|png|gif|tiff?)$", "", base, flags=re.I)
    cands = [(int(sz), k) for k, sz in items if re.sub(r"\.(jpe?g|png|gif|tiff?)$", "", k.split("/")[-1], flags=re.I) == stem
             and re.search(r"\.(jpe?g|png|gif|tiff?)$", k, re.I)]
    return f"{S3}/{max(cands)[1]}" if cands else None

def main():
    picks = json.loads((ROOT / "tools/image_picks.json").read_text())
    commons = json.loads((ROOT / "candidates/manifest.json").read_text())
    pmc = {}
    for f in (ROOT / "candidates_pmc/manifest").glob("*.json"):
        for r in json.loads(f.read_text()): pmc[(r["pmcid"], r["label"])] = r
    man = {}
    for ent, items in picks.items():
        (OUT / ent).mkdir(parents=True, exist_ok=True); man[ent] = []
        for i, it in enumerate(items, 1):
            try:
                if it[0] == "commons":
                    url = commons_original(it[1]); b = c_open(url, False)
                else:
                    r = pmc[(it[1], it[2])]; url = s3_best(it[1], r["graphic"]); b = p_open(url, "bytes") if url else None
                if not b: raise RuntimeError("no data")
                im = Image.open(io.BytesIO(b)); im.load(); im = im.convert("L") if im.mode in ("L", "I;16", "I") else im.convert("RGB")
                im.thumbnail((3000, 3000)); p = OUT / ent / f"{i}.png"; im.save(p, optimize=True)
                man[ent].append({"n": i, "url": url, "w": im.width, "h": im.height, "file": str(p.relative_to(ROOT))})
                print(ent, i, im.size)
            except Exception as e:
                man[ent].append({"n": i, "error": str(e)}); print(ent, i, "FAILED", e, file=sys.stderr)
            time.sleep(1)
        (OUT / "manifest.json").write_text(json.dumps(man, indent=1))

if __name__ == "__main__":
    main()
