#!/usr/bin/env python3
"""Reference implementation of the scoring logic (docs/SKEMA-DIAGNOSIS.md §4) + smoke tests.

This is the behaviour the web prototype and the Flutter app must reproduce exactly.
Run: python3 tools/score_smoke.py
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
ENTITIES = [json.loads(p.read_text(encoding="utf-8")) for p in sorted((ROOT / "data" / "entities").glob("*.json"))]
HARD = -5

def score(entity, inputs):
    """inputs: feature -> value (or list of values for multi features). Returns (total, reasons, hard_hits)."""
    total, reasons, hard = entity.get("base_prior", 0), [], []
    if total:
        reasons.append(("prior", "prevalensi", total, entity.get("base_prior_note_id"), entity.get("base_prior_source_ids", [])))
    for feat, val in inputs.items():
        vals = val if isinstance(val, list) else [val]
        for v in vals:
            if v == "unknown":
                continue
            claim = entity["feature_weights"].get(feat, {}).get(v)
            if not claim:
                continue
            w = claim["weight"]
            total += w
            reasons.append((feat, v, w, claim.get("note_id"), claim["source_ids"]))
            if w <= HARD:
                hard.append((feat, v))
    for r in entity.get("rules", []):
        ok = True
        for feat, allowed in r["when"].items():
            given = inputs.get(feat)
            given = given if isinstance(given, list) else [given]
            if not any(g in allowed for g in given):
                ok = False; break
        if ok:
            total += r["weight"]
            reasons.append(("rule", r["id"], r["weight"], r.get("note_id"), r["source_ids"]))
    return total, reasons, hard

def rank(inputs):
    rows = []
    for e in ENTITIES:
        t, reasons, hard = score(e, inputs)
        rows.append({"id": e["id"], "name": e["name_en"], "score": t, "hard": hard, "reasons": reasons})
    live = sorted([r for r in rows if not r["hard"]], key=lambda r: -r["score"])
    excluded = sorted([r for r in rows if r["hard"]], key=lambda r: -r["score"])
    return live, excluded

CASES = [
    ("Remaja 15 th, femur distal metafisis, eksentrik, campuran, IC, destruksi korteks, massa, sunburst, osteoid",
     {"age_group": "10-19_open", "bone_class": "long_bone", "longitudinal": "metaphysis", "transverse": "eccentric", "density": "mixed",
      "margin_lodwick": "IC", "cortex": "destruction", "soft_tissue_mass": "present", "periosteal": "spiculated", "matrix": "osteoid"},
     "osteosarcoma_conventional"),
    ("Anak 8 th, femur diafisis, sentral, litik permeatif, korteks relatif utuh, massa besar, onion-skin, tanpa matriks",
     {"age_group": "0-9", "bone_class": "long_bone", "longitudinal": "diaphysis", "transverse": "central", "density": "lytic",
      "margin_lodwick": "III", "cortex": "intact", "soft_tissue_mass": "present", "periosteal": "lamellated", "matrix": "none"},
     "ewing_sarcoma"),
    ("Dewasa 28 th, fisis tertutup, tibia proksimal epifisis-metafisis, eksentrik, litik, IB, ekspansi, tanpa matriks",
     {"age_group": "20-39", "bone_class": "long_bone", "longitudinal": "epiphysis_apophysis", "transverse": "eccentric",
      "density": "lytic", "margin_lodwick": "IB", "cortex": "expansion_shell", "soft_tissue_mass": "absent", "periosteal": "none", "matrix": "none"},
     "giant_cell_tumour_of_bone"),
    ("Anak 12 th, tibia distal metadiafisis, kortikal eksentrik, litik, IA, korteks utuh, tanpa periosteal/matriks",
     {"age_group": "10-19_open", "bone_class": "long_bone", "longitudinal": "metadiaphysis", "transverse": "cortical", "density": "lytic",
      "margin_lodwick": "IA", "cortex": "intact", "soft_tissue_mass": "absent", "periosteal": "none", "matrix": "none"},
     "non_ossifying_fibroma"),
    ("Dewasa 52 th, ilium, sentral, campuran, IC, scalloping dalam, massa, matriks ring-and-arc, >5 cm",
     {"age_group": "40-59", "bone_class": "flat_bone", "longitudinal": "not_applicable", "transverse": "central", "density": "mixed",
      "margin_lodwick": "IC", "cortex": "endosteal_scalloping", "soft_tissue_mass": "present", "periosteal": "none", "matrix": "chondroid", "size_cm": ">5"},
     "chondrosarcoma_central"),
    ("Lansia 68 th, korpus vertebra multipel, litik punched-out IB, tanpa periosteal/matriks",
     {"age_group": "60+", "multiplicity": "multiple", "bone_class": "spine_body", "longitudinal": "not_applicable", "transverse": "central",
      "density": "lytic", "margin_lodwick": "IB", "cortex": "endosteal_scalloping", "soft_tissue_mass": "absent", "periosteal": "none", "matrix": "none"},
     "plasmacytoma_myeloma"),
    ("Anak 7 th, humerus proksimal metafisis, sentral, litik, IA, ekspansi tipis, tanpa matriks",
     {"age_group": "0-9", "bone_class": "long_bone", "longitudinal": "metaphysis", "transverse": "central", "density": "lytic",
      "margin_lodwick": "IA", "cortex": "expansion_shell", "soft_tissue_mass": "absent", "periosteal": "none", "matrix": "none"},
     "simple_bone_cyst"),
    ("Remaja 17 th, tibia diafisis, kortikal, sklerotik, periosteal solid, <2 cm, nyeri malam + NSAID",
     {"age_group": "10-19_unknown", "bone_class": "long_bone", "longitudinal": "diaphysis", "transverse": "cortical", "density": "sclerotic",
      "margin_lodwick": "not_applicable", "cortex": "intact", "soft_tissue_mass": "absent", "periosteal": "solid_thin", "matrix": "none",
      "size_cm": "<2", "clinical_flags": ["night_pain_nsaid_relief"]},
     "osteoid_osteoma"),
    ("Dewasa 60 th, sakrum, litik destruktif, massa presakral besar, tanpa matriks",
     {"age_group": "60+", "bone_class": "sacrum", "longitudinal": "not_applicable", "transverse": "central", "density": "lytic",
      "margin_lodwick": "IC", "cortex": "destruction", "soft_tissue_mass": "present", "periosteal": "none", "matrix": "none"},
     "chordoma"),
    ("Anak 6 th, femur metafisis, sentral, litik-campuran moth-eaten, periosteal lamelar, demam",
     {"age_group": "0-9", "bone_class": "long_bone", "longitudinal": "metaphysis", "transverse": "central", "density": "mixed",
      "margin_lodwick": "II", "cortex": "focal_breach", "soft_tissue_mass": "present", "periosteal": "lamellated", "matrix": "none",
      "clinical_flags": ["fever_or_infection_signs"]},
     "osteomyelitis"),
    ("Remaja 17 th, fisis TERTUTUP, femur distal epifisis-metafisis, eksentrik, litik, IB, ekspansi, tanpa matriks",
     {"age_group": "10-19_closed", "bone_class": "long_bone", "longitudinal": "epiphysis_apophysis", "transverse": "eccentric",
      "density": "lytic", "margin_lodwick": "IB", "cortex": "expansion_shell", "soft_tissue_mass": "absent", "periosteal": "none", "matrix": "none"},
     "giant_cell_tumour_of_bone"),
    ("Remaja 13 th, fisis TERBUKA, humerus proksimal epifisis, eksentrik, litik, IA, korteks utuh, matriks kondroid halus",
     {"age_group": "10-19_open", "bone_class": "long_bone", "longitudinal": "epiphysis_apophysis", "transverse": "eccentric",
      "density": "lytic", "margin_lodwick": "IA", "cortex": "intact", "soft_tissue_mass": "absent", "periosteal": "none", "matrix": "chondroid"},
     "chondroblastoma"),
    # ---- batch 2
    ("Dewasa 30 th, femur distal posterior, permukaan, massa sklerotik padat, osteoid, korteks utuh",
     {"age_group": "20-39", "bone_class": "long_bone", "longitudinal": "metaphysis", "transverse": "juxtacortical_surface", "density": "sclerotic",
      "margin_lodwick": "not_applicable", "cortex": "intact", "soft_tissue_mass": "present", "periosteal": "none", "matrix": "osteoid"},
     "osteosarcoma_parosteal"),
    ("Lansia 72 th, pelvis, campuran, korteks menebal & tulang membesar, multipel, tanpa periosteal",
     {"age_group": "60+", "multiplicity": "multiple", "bone_class": "flat_bone", "longitudinal": "not_applicable", "transverse": "central", "density": "mixed",
      "margin_lodwick": "not_applicable", "cortex": "intact", "soft_tissue_mass": "absent", "periosteal": "none", "matrix": "none"},
     "paget_disease"),
    ("Dewasa 65 th, femur diafisis, sentral, litik permeatif, korteks utuh, massa jaringan lunak besar, tanpa matriks",
     {"age_group": "60+", "bone_class": "long_bone", "longitudinal": "diaphysis", "transverse": "central", "density": "lytic",
      "margin_lodwick": "III", "cortex": "intact", "soft_tissue_mass": "present", "periosteal": "none", "matrix": "none"},
     "primary_bone_lymphoma"),
    ("Dewasa 50 th, femur distal metafisis, sentral, campuran dengan tepi sklerotik serpiginosa IA, korteks utuh, multipel",
     {"age_group": "40-59", "multiplicity": "multiple", "bone_class": "long_bone", "longitudinal": "metaphysis", "transverse": "central", "density": "mixed",
      "margin_lodwick": "IA", "cortex": "intact", "soft_tissue_mass": "absent", "periosteal": "none", "matrix": "none"},
     "bone_infarct"),
    ("Dewasa 45 th, ilium, sklerotik homogen <2 cm, korteks utuh, insidental",
     {"age_group": "40-59", "bone_class": "flat_bone", "longitudinal": "not_applicable", "transverse": "central", "density": "sclerotic",
      "margin_lodwick": "not_applicable", "cortex": "intact", "soft_tissue_mass": "absent", "periosteal": "none", "matrix": "none", "size_cm": "<2"},
     "enostosis"),
    ("Dewasa 35 th, korpus vertebra, litik destruktif IC, massa paravertebral, periosteal tidak ada, demam ringan",
     {"age_group": "20-39", "bone_class": "spine_body", "longitudinal": "not_applicable", "transverse": "central", "density": "lytic",
      "margin_lodwick": "IC", "cortex": "destruction", "soft_tissue_mass": "present", "periosteal": "none", "matrix": "none",
      "clinical_flags": ["fever_or_infection_signs"]},
     "skeletal_tuberculosis"),
    ("Dewasa 24 th, tibia diafisis, kortikal, sklerotik dengan periosteal solid, tanpa massa",
     {"age_group": "20-39", "bone_class": "long_bone", "longitudinal": "diaphysis", "transverse": "cortical", "density": "sclerotic",
      "margin_lodwick": "not_applicable", "cortex": "focal_breach", "soft_tissue_mass": "absent", "periosteal": "solid_thin", "matrix": "none"},
     "stress_fracture"),
    ("Dewasa 55 th, kalkaneus, lusen IA dengan kalsifikasi sentral, korteks utuh",
     {"age_group": "40-59", "bone_class": "calcaneus", "longitudinal": "not_applicable", "transverse": "central", "density": "mixed",
      "margin_lodwick": "IA", "cortex": "intact", "soft_tissue_mass": "absent", "periosteal": "none", "matrix": "none"},
     "intraosseous_lipoma"),
]

if __name__ == "__main__":
    fails = 0
    for title, inputs, expected in CASES:
        live, excluded = rank(inputs)
        top = [f"{r['id']}({r['score']})" for r in live[:5]]
        pos = next((i for i, r in enumerate(live) if r["id"] == expected), None)
        ok = pos is not None and live[pos]["score"] == live[0]["score"]   # tied-for-first counts as first
        fails += 0 if ok else 1
        print(("PASS" if ok else "WARN") + f" | {title}\n       top5: {', '.join(top)}  | expected '{expected}' at rank {None if pos is None else pos+1}"
              f"  | excluded by hard constraint: {len(excluded)}")
    print(f"\n{len(CASES)-fails}/{len(CASES)} vignettes rank the expected entity first.")
