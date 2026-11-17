#!/usr/bin/env python3
"""Turn the screened picks into web/img/*.jpg and data/images.json records.

Input:  picks JSON  {entity: [["commons", file_title, crop?] | ["pmc", pmcid, fig_label, crop?], ...]}
        captions JSON {entity: [caption_id, ...]}  (our own words, same order as picks)
        candidate manifests from the TumTul GitHub repo (candidates/, candidates_pmc/)
Output: web/img/<entity>-<n>.jpg (max 900 px, JPEG q80) and data/images.json (status from --status).
"""
import json, pathlib, re, sys
from PIL import Image

def lic_url(name):
    m = re.match(r"CC (BY(?:-SA)?) ([0-9.]+)(?: ([a-z]{2}))?$", name or "", re.I)
    if m:
        u = f"https://creativecommons.org/licenses/{m.group(1).lower()}/{m.group(2)}/"
        return u + (f"{m.group(3)}/" if m.group(3) else "")
    if (name or "").upper().startswith("CC0"): return "https://creativecommons.org/publicdomain/zero/1.0/"
    return ""

def main(repo, root, picks_p, caps_p, status):
    repo, root = pathlib.Path(repo), pathlib.Path(root)
    picks = json.loads(pathlib.Path(picks_p).read_text()); caps = json.loads(pathlib.Path(caps_p).read_text())
    commons = json.loads((repo / "candidates/manifest.json").read_text())
    pmc = {}
    for f in (repo / "candidates_pmc/manifest").glob("*.json"):
        for r in json.loads(f.read_text()): pmc[(r["pmcid"], r["label"])] = r
    out = {"version": "0.2.0", "note": json.loads((root / "data/images.json").read_text())["note"], "images": {}}
    (root / "web/img").mkdir(parents=True, exist_ok=True)
    for ent, items in sorted(picks.items()):
        recs = []
        for i, it in enumerate(items, 1):
            crop = it[3] if it[0] == "pmc" and len(it) > 3 else (it[2] if it[0] == "commons" and len(it) > 2 else None)
            if it[0] == "commons":
                r = next(x for x in commons[ent] if x["title"] == it[1])
                src = repo / r["file"]
                rec = {"source_title": r["title"].replace("File:", ""), "source_url": r["page"], "author": r["artist"] or "tidak tercantum",
                       "repository": "Wikimedia Commons", "licence": r["licence"].replace("Public Domain", "Public domain"),
                       "licence_url": r.get("licence_url") or lic_url(r["licence"])}
            else:
                r = pmc[(it[1], it[2])]; src = repo / r["file"]
                au = r["authors"]; au_s = (", ".join(au[:3]) + (" et al." if len(au) > 3 else "")) or "tidak tercantum"
                rec = {"source_title": f'{r["article_title"]} ({r["journal"]}, {r["year"]}), {r["label"].rstrip(":.")}',
                       "source_url": f'https://doi.org/{r["doi"]}' if r["doi"] else r["article_url"], "author": au_s,
                       "repository": f'{r["journal"]} via PubMed Central ({r["pmcid"]})', "licence": r["licence"], "licence_url": r["licence_url"]}
            im = Image.open(src).convert("RGB")
            if crop:
                W, H = im.size; im = im.crop((int(crop[0] * W), int(crop[1] * H), int(crop[2] * W), int(crop[3] * H)))
            im.thumbnail((900, 900))
            fn = f"img/{ent}-{i}.jpg"; im.save(root / "web" / fn, quality=80, optimize=True, progressive=True)
            changes = "dipotong ke panel radiograf, diperkecil" if crop else "diperkecil"
            recs.append({"file": fn, "caption_id": caps[ent][i - 1], **rec, "changes": changes, "status": status})
        out["images"][ent] = recs
    (root / "data/images.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(sum(len(v) for v in out["images"].values()), "images,", len(out["images"]), "entities")

if __name__ == "__main__":
    main(*sys.argv[1:6])
