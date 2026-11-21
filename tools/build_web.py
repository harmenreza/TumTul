#!/usr/bin/env python3
"""Assemble the self-contained web prototype: web/template.html + KB JSON (+ image registry) -> web/index.html.
Run: python3 tools/build_web.py   (run validate_kb.py first)
Example images listed in data/images.json are published next to index.html under web/img/.
"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
features = json.loads((ROOT / "data/features.json").read_text(encoding="utf-8"))["features"]
sources = json.loads((ROOT / "data/sources.json").read_text(encoding="utf-8"))["sources"]
entities = [json.loads(p.read_text(encoding="utf-8")) for p in sorted((ROOT / "data/entities").glob("*.json"))]
kb = {"kb_version": "0.6.3", "features": features, "entities": entities, "sources": sources}
imgp = ROOT / "data/images.json"
images = json.loads(imgp.read_text(encoding="utf-8")) if imgp.exists() else {"images": {}}
ids = {e["id"] for e in entities}
unknown = set(images.get("images", {})) - ids
assert not unknown, f"data/images.json refers to unknown entities: {unknown}"
for eid, recs in images.get("images", {}).items():
    for r in recs:
        if r.get("status") == "approved":
            for k in ("file", "caption_id", "source_title", "source_url", "author", "licence"):
                assert r.get(k), f"{eid}: approved image missing '{k}'"
            assert (ROOT / "web" / r["file"]).exists(), f"{eid}: missing file web/{r['file']}"
enc = lambda o: json.dumps(o, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
html = (ROOT / "web/template.html").read_text(encoding="utf-8").replace("/*__KB__*/", enc(kb)).replace("/*__IMG__*/", enc(images))
(ROOT / "web/index.html").write_text(html, encoding="utf-8")
n = sum(1 for recs in images.get("images", {}).values() for r in recs if r.get("status") == "approved")
print(f"web/index.html written: {len(html)/1024:.0f} KB, {len(entities)} entities, {n} approved example images")
