#!/usr/bin/env python3
"""Validate the knowledge base.

Checks:
  1. data/features.json, data/sources.json and every data/entities/*.json parse.
  2. The assembled KB validates against schema/kb-schema.json (JSON Schema 2020-12).
  3. Every feature code / value code used in entities exists in features.json.
  4. Every S-xx referenced anywhere exists in sources.json.
  5. Entity ids are unique and match their file names.
Exit code 1 on any failure. Run: python3 tools/validate_kb.py
"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
errors = []

def load(p):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as ex:
        errors.append(f"{p}: cannot parse JSON: {ex}")
        return None

schema = load(ROOT / "schema" / "kb-schema.json")
features_doc = load(ROOT / "data" / "features.json")
sources_doc = load(ROOT / "data" / "sources.json")
entity_files = sorted((ROOT / "data" / "entities").glob("*.json"))
entities = [e for e in (load(p) for p in entity_files) if e is not None]

if errors:
    print("\n".join(errors)); sys.exit(1)

features = features_doc["features"]
source_ids = {s["id"] for s in sources_doc["sources"]}
feature_values = {f: {v["code"] for v in spec["values"]} | {"unknown"} for f, spec in features.items()}

# 2. schema validation of the assembled KB
kb = {"kb_version": "0.2.0", "features": features, "entities": entities, "sources": sources_doc["sources"]}
try:
    import jsonschema
    v = jsonschema.Draft202012Validator(schema)
    for err in sorted(v.iter_errors(kb), key=lambda e: list(e.path)):
        errors.append(f"schema: {'/'.join(str(x) for x in err.path)}: {err.message[:200]}")
except ImportError:
    print("warning: jsonschema not installed; skipping structural validation")

# 3–5. cross-references
seen_ids = set()
for path, e in zip(entity_files, entities):
    eid = e.get("id")
    if eid != path.stem:
        errors.append(f"{path.name}: id '{eid}' does not match file name")
    if eid in seen_ids:
        errors.append(f"{path.name}: duplicate id '{eid}'")
    seen_ids.add(eid)
    for sid in e.get("source_ids", []):
        if sid not in source_ids:
            errors.append(f"{eid}: unknown source {sid}")
    for feat, vals in e.get("feature_weights", {}).items():
        if feat not in features:
            errors.append(f"{eid}: unknown feature '{feat}'"); continue
        for val, claim in vals.items():
            if val not in feature_values[feat]:
                errors.append(f"{eid}: unknown value '{val}' for feature '{feat}'")
            for sid in claim.get("source_ids", []):
                if sid not in source_ids:
                    errors.append(f"{eid}: {feat}/{val}: unknown source {sid}")
    for r in e.get("rules", []):
        for feat, vals in r.get("when", {}).items():
            if feat not in features:
                errors.append(f"{eid}: rule {r.get('id')}: unknown feature '{feat}'"); continue
            for val in vals:
                if val not in feature_values[feat]:
                    errors.append(f"{eid}: rule {r.get('id')}: unknown value '{val}' for '{feat}'")
        for sid in r.get("source_ids", []):
            if sid not in source_ids:
                errors.append(f"{eid}: rule {r.get('id')}: unknown source {sid}")

# feature-level source refs
for feat, spec in features.items():
    for v in spec["values"]:
        for sid in v.get("source_ids", []):
            if sid not in source_ids:
                errors.append(f"features.json: {feat}/{v['code']}: unknown source {sid}")

if errors:
    print(f"FAILED — {len(errors)} problem(s):")
    print("\n".join("  " + e for e in errors))
    sys.exit(1)

n_claims = sum(len(v) for e in entities for v in e["feature_weights"].values())
used_sources = sorted({s for e in entities for s in e["source_ids"]} |
                      {s for e in entities for v in e["feature_weights"].values() for c in v.values() for s in c["source_ids"]})
print(f"OK — {len(entities)} entities, {n_claims} weighted claims, {sum(len(e['rules']) for e in entities)} rules, "
      f"{len(used_sources)} sources referenced by entities: {', '.join(used_sources)}")
