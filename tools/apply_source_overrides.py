#!/usr/bin/env python3
"""Apply owner-approved SOURCE corrections to data/entities/*.json after the generators have run.

Why this exists: the full-text source check (docs/TINJAUAN-SUMBER-v0.6.md) found claims citing sources that
do not discuss the entity. Corrections approved by the owner are listed in OVERRIDES below and applied here.
Only `source_ids` change. No weight, note, rule, prior or schema field is touched, so every score and ranking
is identical; the script proves this by comparing the file before and after with source_ids removed.

Build order (see README "Build"):
    python3 tools/build_entities_batch2.py     # regenerates all entity files (resets source_ids)
    python3 tools/apply_source_overrides.py    # re-applies the approved source corrections   <-- this script
    python3 tools/validate_kb.py

Run:  python3 tools/apply_source_overrides.py [repo_root] [--check]
  --check   change nothing; exit 1 if any file would change (use in CI / before publishing)
Idempotent. Stops with an error if a listed claim does not exist, so a renamed feature value cannot be
silently skipped.

KB 0.6.1 (2026-11-22, approved by the owner): chondromyxoid fibroma re-cited from S-06 to S-18.
  S-06 (De Salvo 2022) has no section on CMF; S-18 (Gomez-Leon 2023) has one. See docs/USULAN-SUMBER-v0.7.md
  part A for the claim-by-claim table. "add" lists the claims whose finding S-18 states (13) or supports in
  direction only (7); matrix:none already cited S-18.
"""
import copy
import json
import pathlib
import sys

args = [a for a in sys.argv[1:] if not a.startswith("--")]
CHECK = "--check" in sys.argv
ROOT = pathlib.Path(args[0]) if args else pathlib.Path(__file__).resolve().parent.parent

OVERRIDES = {
    "chondromyxoid_fibroma": {
        "drop_everywhere": ["S-06"],          # removed from every claim, every rule and the entity's own source_ids
        "add": {                               # (feature, value) -> sources to add if not present
            ("age_group", "20-39"): ["S-18"],
            ("age_group", "60+"): ["S-18"],
            ("bone_class", "long_bone"): ["S-18"],
            ("bone_class", "small_tubular_hand_foot"): ["S-18"],
            ("longitudinal", "metaphysis"): ["S-18"],
            ("transverse", "eccentric"): ["S-18"],
            ("transverse", "juxtacortical_surface"): ["S-18"],
            ("density", "lytic"): ["S-18"],
            ("density", "sclerotic"): ["S-18"],            # direction only
            ("margin_lodwick", "IA"): ["S-18"],
            ("margin_lodwick", "IC"): ["S-18"],            # direction only
            ("margin_lodwick", "II"): ["S-18"],            # direction only
            ("margin_lodwick", "III"): ["S-18"],           # direction only
            ("cortex", "expansion_shell"): ["S-18"],
            ("periosteal", "none"): ["S-18"],
            ("periosteal", "lamellated"): ["S-18"],        # direction only
            ("periosteal", "spiculated"): ["S-18"],        # direction only
            ("periosteal", "codman"): ["S-18"],            # direction only
            ("matrix", "none"): ["S-18"],                  # already cited
            ("matrix", "chondroid"): ["S-18"],
        },
    },
    # KB 0.6.1, approved 2026-11-22: S-31 (Ariyaratne 2023, Primary Osseous Malignancies of the Spine) read in full.
    # 11 claims supported, 9 direction only (marked). Not added: matrix:none (+2), which S-31 mildly contradicts
    # (punctate calcification is common), and the 11 claims S-31 does not discuss. See docs/USULAN-SUMBER-v0.7.md B2.
    "chordoma": {
        "add": {
            ("age_group", "20-39"): ["S-31"],
            ("age_group", "40-59"): ["S-31"],
            ("age_group", "60+"): ["S-31"],
            ("age_group", "0-9"): ["S-31"],                 # direction only
            ("age_group", "10-19_open"): ["S-31"],          # direction only
            ("age_group", "10-19_closed"): ["S-31"],        # direction only
            ("age_group", "10-19_unknown"): ["S-31"],       # direction only
            ("bone_class", "sacrum"): ["S-31"],
            ("bone_class", "spine_body"): ["S-31"],
            ("bone_class", "long_bone"): ["S-31"],
            ("bone_class", "flat_bone"): ["S-31"],
            ("bone_class", "spine_posterior"): ["S-31"],
            ("transverse", "central"): ["S-31"],            # direction only
            ("density", "lytic"): ["S-31"],
            ("density", "sclerotic"): ["S-31"],             # direction only
            ("cortex", "destruction"): ["S-31"],
            ("cortex", "intact"): ["S-31"],                 # direction only
            ("soft_tissue_mass", "present"): ["S-31"],
            ("soft_tissue_mass", "absent"): ["S-31"],       # direction only
            ("matrix", "chondroid"): ["S-31"],              # direction only
        },
    },
    # KB 0.6.1, approved 2026-11-22: S-32 (Ariyaratne 2023, Primary Benign Neoplasms of the Spine) read in full.
    # 3 claims supported, 5 direction only (marked). Not added: cortex:destruction (-5), which S-32 contradicts
    # (aggressive haemangioma with bone destruction), and the 23 claims it does not discuss (no age data).
    "vertebral_haemangioma": {
        "add": {
            ("bone_class", "spine_body"): ["S-32"],
            ("matrix", "coarse_trabeculae"): ["S-32"],
            ("soft_tissue_mass", "present"): ["S-32"],
            ("transverse", "central"): ["S-32"],            # direction only
            ("density", "mixed"): ["S-32"],                 # direction only
            ("density", "lytic"): ["S-32"],                 # direction only
            ("cortex", "intact"): ["S-32"],                 # direction only
            ("cortex", "focal_breach"): ["S-32"],           # direction only
        },
    },
    # KB 0.6.2, approved 2026-11-22: S-33 (Kitajima 2018, single case with a general description; read in full).
    # Supported claims only. Because the source is a case report, direction-only claims are left uncited
    # (see docs/USULAN-SUMBER-v0.7.md D3).
    "osteosarcoma_periosteal": {
        "add": {
            ("age_group", "10-19_unknown"): ["S-33"],
            ("age_group", "10-19_open"): ["S-33"],
            ("age_group", "10-19_closed"): ["S-33"],
            ("age_group", "20-39"): ["S-33"],
            ("bone_class", "long_bone"): ["S-33"],
            ("longitudinal", "diaphysis"): ["S-33"],
            ("transverse", "juxtacortical_surface"): ["S-33"],
            ("cortex", "saucerization"): ["S-33"],
            ("soft_tissue_mass", "present"): ["S-33"],
            ("periosteal", "spiculated"): ["S-33"],
            ("matrix", "chondroid"): ["S-33"],
        },
    },
    # KB 0.6.2, approved 2026-11-22: S-34 (Nedopil 2013, case plus literature review) and S-35 (Stefanidis 2011,
    # single case); both read in full. Supported claims only (see docs/USULAN-SUMBER-v0.7.md D1).
    "desmoplastic_fibroma": {
        "add": {
            ("age_group", "20-39"): ["S-34", "S-35"],
            ("age_group", "10-19_unknown"): ["S-34", "S-35"],
            ("age_group", "10-19_open"): ["S-34", "S-35"],
            ("age_group", "10-19_closed"): ["S-34", "S-35"],
            ("bone_class", "long_bone"): ["S-34", "S-35"],
            ("bone_class", "flat_bone"): ["S-34", "S-35"],
            ("bone_class", "craniofacial"): ["S-34", "S-35"],
            ("longitudinal", "metaphysis"): ["S-34"],
            ("density", "lytic"): ["S-34", "S-35"],
            ("cortex", "focal_breach"): ["S-34", "S-35"],
        },
    },
    # KB 0.6.3, approved 2026-11-22: S-36 (Rivas-Garcia 2013, imaging review of Pott's disease with a 48-patient
    # series; read in full from the owner's PDF; cite_only, no CC licence). Supported claims only
    # (see docs/USULAN-SUMBER-v0.7.md F1).
    "skeletal_tuberculosis": {
        "add": {
            ("age_group", "40-59"): ["S-36"],
            ("bone_class", "spine_body"): ["S-36"],
            ("density", "lytic"): ["S-36"],
            ("density", "mixed"): ["S-36"],
            ("density", "sclerotic"): ["S-36"],
            ("cortex", "destruction"): ["S-36"],
            ("soft_tissue_mass", "present"): ["S-36"],
            ("multiplicity", "multiple"): ["S-36"],
        },
    },
}


def strip_sources(obj):
    """Copy of an entity with every source list removed, for the 'nothing else changed' proof."""
    if isinstance(obj, dict):
        return {k: strip_sources(v) for k, v in obj.items() if k not in ("source_ids", "base_prior_source_ids")}
    if isinstance(obj, list):
        return [strip_sources(v) for v in obj]
    return obj


def apply(entity, spec):
    e = copy.deepcopy(entity)
    drop = set(spec.get("drop_everywhere", []))
    for feat, vals in e["feature_weights"].items():
        for claim in vals.values():
            claim["source_ids"] = [s for s in claim["source_ids"] if s not in drop]
    for rule in e.get("rules", []):
        rule["source_ids"] = [s for s in rule["source_ids"] if s not in drop]
    e["source_ids"] = [s for s in e["source_ids"] if s not in drop]
    for (feat, val), add in spec.get("add", {}).items():
        claim = e["feature_weights"].get(feat, {}).get(val)
        if claim is None:
            raise SystemExit(f"{e['id']}: claim {feat}:{val} not found - override table is out of date")
        for s in add:
            if s not in claim["source_ids"]:
                claim["source_ids"].append(s)
            if s not in e["source_ids"]:
                e["source_ids"].append(s)
    for feat, vals in e["feature_weights"].items():
        for val, claim in vals.items():
            if not claim["source_ids"]:
                raise SystemExit(f"{e['id']}: {feat}:{val} would be left without any source")
    return e


known = {s["id"] for s in (lambda d: d["sources"] if isinstance(d, dict) else d)(
    json.loads((ROOT / "data/sources.json").read_text(encoding="utf-8")))}
changed = 0
for eid, spec in OVERRIDES.items():
    path = ROOT / "data" / "entities" / f"{eid}.json"
    raw = path.read_text(encoding="utf-8")
    before = json.loads(raw)
    after = apply(before, spec)
    assert strip_sources(before) == strip_sources(after), f"{eid}: something other than source_ids changed"
    used = {s for vals in after["feature_weights"].values() for c in vals.values() for s in c["source_ids"]}
    used |= set(after["source_ids"])
    missing = used - known
    if missing:
        raise SystemExit(f"{eid}: unknown source codes {sorted(missing)}")
    n = sum(1 for f, vals in before["feature_weights"].items() for v, c in vals.items()
            if c["source_ids"] != after["feature_weights"][f][v]["source_ids"])
    if after == before:
        print(f"{eid}: already up to date")
        continue
    changed += 1
    print(f"{eid}: {n} claims re-cited; entity sources {before['source_ids']} -> {after['source_ids']}")
    if not CHECK:
        # keep the generators' file style: same indent, key order and trailing newline as the existing file
        indent = len(raw.split("\n")[1]) - len(raw.split("\n")[1].lstrip()) if "\n" in raw else None
        text = json.dumps(after, ensure_ascii=False, indent=indent or None,
                          sort_keys=(json.dumps(before, ensure_ascii=False, indent=indent or None, sort_keys=True)
                                     + ("\n" if raw.endswith("\n") else "") == raw))
        path.write_text(text + ("\n" if raw.endswith("\n") else ""), encoding="utf-8")
if CHECK and changed:
    raise SystemExit(f"{changed} file(s) would change: run tools/apply_source_overrides.py")
print("source overrides:", "check only, " if CHECK else "", f"{changed} file(s) changed")
