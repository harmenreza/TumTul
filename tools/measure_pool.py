#!/usr/bin/env python3
"""Measure original pixel size of every candidate for the given entities (Commons from manifest, PMC by download).
Writes pool_sizes/<entity>.json: [{source, key, label?, w, h, url}] — used to find higher-resolution replacements."""
import io, json, pathlib, sys, time
from PIL import Image
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from fetch_hires import s3_best
from fetch_pmc import _open as p_open
ROOT = pathlib.Path(__file__).resolve().parent.parent; OUT = ROOT / "pool_sizes"; OUT.mkdir(exist_ok=True)
Image.MAX_IMAGE_PIXELS = 200_000_000
commons = json.loads((ROOT / "candidates/manifest.json").read_text())
for ent in sys.argv[1:]:
    res = []
    for r in commons.get(ent, []):
        res.append({"source": "commons", "key": r["title"], "w": r["width"], "h": r["height"], "n": r.get("n")})
    for f in [ROOT / f"candidates_pmc/manifest/{ent}.json", ROOT / f"candidates_pmc/manifest/{ent}_gap.json"]:
        if not f.exists(): continue
        for r in json.loads(f.read_text()):
            try:
                url = s3_best(r["pmcid"], r["graphic"]); b = p_open(url, "bytes") if url else None
                im = Image.open(io.BytesIO(b)) if b else None
                res.append({"source": "pmc", "key": r["pmcid"], "label": r["label"], "w": im.width if im else 0, "h": im.height if im else 0,
                            "url": url, "set": f.stem, "n": r.get("n")})
            except Exception as e:
                res.append({"source": "pmc", "key": r["pmcid"], "label": r["label"], "error": str(e)})
            time.sleep(0.3)
    (OUT / f"{ent}.json").write_text(json.dumps(res, indent=1)); print(ent, len(res))
