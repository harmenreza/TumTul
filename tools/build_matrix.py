#!/usr/bin/env python3
"""Build the scoring-matrix reference page: every entity x every feature value, with priors and rules.

Reads data/features.json and data/entities/*.json, inlines them into web/matrix_template.html and writes
web/matrix.html (published as the Claude artifact "TumTul scoring matrix"). Display only: it reads the
knowledge base and changes nothing in it. Labels in SHORT and VS are English display text for the column
headers, outside the data schema.

Run:  python3 tools/build_matrix.py [repo_root] [out.html] [template.html]
Prints the counts shown on the page; for KB 0.6.0 expect
  37 entities, 62 feature values, 1584 weighted claims, 322 hard constraints, 5 rules.
The script stops if an entity file uses a feature value, WHO group or behaviour it does not know.
"""
import collections
import json
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent
OUT = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "web" / "matrix.html"
TPL = pathlib.Path(sys.argv[3]) if len(sys.argv) > 3 else ROOT / "web" / "matrix_template.html"

F = json.loads((ROOT / "data/features.json").read_text(encoding="utf-8"))
E = [json.loads(p.read_text(encoding="utf-8")) for p in sorted((ROOT / "data/entities").glob("*.json"))]

SHORT = {"age_group": "Age & physis", "multiplicity": "Number", "bone_class": "Bone", "longitudinal": "Longitudinal",
         "transverse": "Transverse", "density": "Density", "margin_lodwick": "Margin (Lodwick)", "cortex": "Cortex",
         "soft_tissue_mass": "Soft tissue", "periosteal": "Periosteal reaction", "matrix": "Matrix", "size_cm": "Size",
         "clinical_flags": "Clinical"}
VS = {"0-9": "0–9 y", "10-19_open": "10–19 open", "10-19_closed": "10–19 closed", "10-19_unknown": "10–19 n/a",
      "20-39": "20–39 y", "40-59": "40–59 y", "60+": "60+ y",
      "solitary": "Solitary", "multiple": "Multiple",
      "long_bone": "Long bone", "small_tubular_hand_foot": "Hand / foot", "flat_bone": "Flat bone",
      "spine_body": "Vertebral body", "spine_posterior": "Posterior elements", "sacrum": "Sacrum",
      "clavicle": "Clavicle", "calcaneus": "Calcaneus", "patella": "Patella", "craniofacial": "Craniofacial",
      "epiphysis_apophysis": "Epiphysis", "metaphysis": "Metaphysis", "metadiaphysis": "Metadiaphysis",
      "diaphysis": "Diaphysis",
      "central": "Central", "eccentric": "Eccentric", "cortical": "Intracortical",
      "juxtacortical_surface": "Surface", "juxtacortical_continuous": "Surface, continuous",
      "lytic": "Lytic", "mixed": "Mixed", "sclerotic": "Sclerotic",
      "IA": "IA", "IB": "IB", "IC": "IC", "II": "II moth-eaten", "III": "III permeative",
      "intact": "Intact", "endosteal_scalloping": "Scalloping", "expansion_shell": "Expansion",
      "focal_breach": "Focal breach", "destruction": "Destruction", "saucerization": "Saucerization",
      "absent": "Absent", "present": "Present",
      "none": "None", "solid_thin": "Solid / thin", "shell": "Shell", "lamellated": "Lamellated",
      "spiculated": "Spiculated", "codman": "Codman", "present_unspecified": "Present, unspecified",
      "osteoid": "Osteoid", "chondroid": "Chondroid", "ground_glass": "Ground-glass",
      "coarse_trabeculae": "Coarse trabeculae",
      "<2": "< 2 cm", "2-5": "2–5 cm", ">5": "> 5 cm",
      "night_pain_nsaid_relief": "Night pain, NSAID", "known_primary_malignancy": "Known primary",
      "fever_or_infection_signs": "Fever / infection"}
GROUPS = [("chondrogenic", "Chondrogenic"), ("osteogenic", "Osteogenic"), ("fibrogenic", "Fibrogenic"),
          ("vascular", "Vascular"), ("osteoclastic_giant_cell_rich", "Osteoclastic giant cell-rich"),
          ("notochordal", "Notochordal"), ("other_mesenchymal", "Other mesenchymal"),
          ("haematopoietic", "Haematopoietic"), ("undifferentiated_small_round_cell", "Small round cell"),
          ("non_neoplastic_or_secondary", "Non-neoplastic and secondary")]
BEH = {"benign": "Benign", "intermediate_locally_aggressive": "Intermediate", "malignant": "Malignant",
       "secondary_malignant": "Secondary malignant", "non_neoplastic": "Non-neoplastic"}

# Columns: every feature value offered in the app, in features.json order. 'not_applicable' is hidden in the
# UI and left out here; its claims are still counted (all weight 0 in KB 0.6.0).
feats, cols = [], []
for code, spec in F["features"].items():
    vals = [v["code"] for v in spec["values"] if v["code"] != "not_applicable"]
    feats.append({"c": code, "l": SHORT[code], "n": len(vals)})
    for v in vals:
        cols.append([code, v, VS[v]])
known = {(f, v) for f, v, _ in cols}

ents, nclaims, hard = [], 0, 0
counts, dropped = collections.Counter(), collections.Counter()
for e in E:
    if e["who_group"] not in dict(GROUPS):
        raise SystemExit(f"unknown who_group {e['who_group']} in {e['id']}")
    if e["behaviour"] not in BEH:
        raise SystemExit(f"unknown behaviour {e['behaviour']} in {e['id']}")
    row, notes = [], {}
    for i, (f, v, _) in enumerate(cols):
        c = e["feature_weights"].get(f, {}).get(v)
        if c is None:
            row.append(None)          # no claim: counts as 0, drawn as a dot
            continue
        row.append(c["weight"])
        nclaims += 1
        counts[c["weight"]] += 1
        hard += c["weight"] <= -5
        notes[i] = [c.get("note_id", ""), c["source_ids"]]
    for f, d in e["feature_weights"].items():
        for v, c in d.items():
            if v == "not_applicable":
                nclaims += 1
                dropped[c["weight"]] += 1
            elif (f, v) not in known:
                raise SystemExit(f"unknown value {f}:{v} in {e['id']}")
    ents.append({"id": e["id"], "n": e["name_en"], "ni": e["name_id"], "g": e["who_group"], "b": e["behaviour"],
                 "p": e.get("base_prior", 0), "w": row, "x": notes,
                 "r": [{"id": r["id"], "w": r["weight"], "when": r["when"], "note": r.get("note_id", ""),
                        "s": r["source_ids"]} for r in e.get("rules", [])]})

data = {"feats": feats, "cols": cols, "ents": ents, "groups": GROUPS, "beh": BEH, "vs": VS, "short": SHORT}
stats = {"entities": len(E), "cols": len(cols), "claims": nclaims, "hard": hard,
         "rules": sum(len(e["r"]) for e in ents), "counts": dict(sorted(counts.items())),
         "not_applicable_claims": dict(dropped)}
print(json.dumps(stats))

html = TPL.read_text(encoding="utf-8").replace(
    "/*DATA*/", json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/"))
for k in ("entities", "cols", "claims", "hard", "rules"):
    html = html.replace("{{%s}}" % k, str(stats[k]))
OUT.write_text(html, encoding="utf-8")
print(f"wrote {OUT} ({len(html)} bytes)")
