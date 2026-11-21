#!/usr/bin/env python3
"""Read-only review of the TumTul scoring knowledge base (KB 0.6.0). Changes nothing in data/ or schema/.

Reads data/features.json, data/entities/*.json, data/sources.json and (optionally) the coded validation cases,
then prints every table used in docs/TINJAUAN-SKOR-v0.6.md and writes the classification of all hard constraints
to docs/tinjauan-skor-v0.6-hard-constraints.csv.

Run:  python3 tools/review_scoring.py [repo_root] > docs/tinjauan-skor-v0.6-keluaran.txt
Python 3 standard library only. Deterministic: same KB -> same output.

Scoring is the normative logic of docs/SKEMA-DIAGNOSIS.md section 4 / tools/score_smoke.py:
  score = base_prior + sum(weights of filled feature values) + sum(rule weights whose `when` matches);
  any single weight <= -5 moves the entity to the excluded list.
UI input rules (v0.6.3) used for "reachable" inputs:
  longitudinal only when bone_class = long_bone; margin_lodwick only when density in {lytic, mixed} and
  transverse not in {juxtacortical_surface, juxtacortical_continuous}; blocked pairs: surface transverse x
  cortex endosteal_scalloping; juxtacortical_continuous x density lytic; not_applicable is hidden.

The classification of hard constraints (HC_OVERRIDES), the expected-claim list (EXPECTED), the mimic groups
(MIMIC_GROUPS) and the vignettes (VIGNETTES) are the reviewer's own judgement / constructed cases, written
from standard MSK radiology knowledge. They are hypotheses for v0.7, not validation, and nothing is applied.
"""
import collections
import csv
import itertools
import json
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent
FEAT = json.loads((ROOT / "data/features.json").read_text(encoding="utf-8"))["features"]
ENTS = [json.loads(p.read_text(encoding="utf-8")) for p in sorted((ROOT / "data/entities").glob("*.json"))]
SRC = {s["id"]: s for s in json.loads((ROOT / "data/sources.json").read_text(encoding="utf-8"))["sources"]}
HARD = -5
SCALE = {-5, -2, 0, 1, 2, 3}
FO = list(FEAT)                                    # feature order
VALS = {f: [v["code"] for v in FEAT[f]["values"] if v["code"] != "not_applicable"] for f in FO}
EID = [e["id"] for e in ENTS]
ENT = {e["id"]: e for e in ENTS}
PRIOR = {e["id"]: e.get("base_prior", 0) for e in ENTS}
SURF = ("juxtacortical_surface", "juxtacortical_continuous")
CORE6 = ["age_group", "bone_class", "longitudinal", "transverse", "density", "margin_lodwick"]
SHORT = {
    "adamantinoma_ofd_spectrum": "OFD-adamantinoma", "aneurysmal_bone_cyst": "ABC", "bone_infarct": "Bone infarct",
    "bone_metastasis": "Metastasis", "bpop_nora_lesion": "BPOP", "brown_tumour": "Brown tumour",
    "chondroblastoma": "Chondroblastoma", "chondromyxoid_fibroma": "CMF", "chondrosarcoma_central": "Central CS",
    "chordoma": "Chordoma", "clear_cell_chondrosarcoma": "Clear cell CS", "desmoplastic_fibroma": "Desmoplastic fibroma",
    "enchondroma": "Enchondroma", "enostosis": "Enostosis", "ewing_sarcoma": "Ewing sarcoma",
    "fibrous_dysplasia": "Fibrous dysplasia", "giant_cell_tumour_of_bone": "GCTB",
    "intraosseous_ganglion_geode": "Geode/ganglion", "intraosseous_lipoma": "Intraosseous lipoma",
    "langerhans_cell_histiocytosis": "LCH", "non_ossifying_fibroma": "NOF", "osteoblastoma": "Osteoblastoma",
    "osteochondroma": "Osteochondroma", "osteoid_osteoma": "Osteoid osteoma", "osteomyelitis": "Osteomyelitis",
    "osteosarcoma_conventional": "Conventional OS", "osteosarcoma_parosteal": "Parosteal OS",
    "osteosarcoma_periosteal": "Periosteal OS", "osteosarcoma_telangiectatic": "Telangiectatic OS",
    "paget_disease": "Paget", "periosteal_chondroma": "Periosteal chondroma", "plasmacytoma_myeloma": "Myeloma",
    "primary_bone_lymphoma": "Lymphoma", "simple_bone_cyst": "SBC", "skeletal_tuberculosis": "Skeletal TB",
    "stress_fracture": "Stress fracture", "vertebral_haemangioma": "Vertebral haemangioma"}


def w(eid, f, v):
    """Weight of a claim, or None when the entity states nothing for this value."""
    c = ENT[eid]["feature_weights"].get(f, {}).get(v)
    return None if c is None else c["weight"]


def w0(eid, f, v):
    x = w(eid, f, v)
    return 0 if x is None else x


def score(eid, inputs):
    """inputs: feature -> value or list (clinical_flags). Returns (total, [(feature, value)] hard hits)."""
    e = ENT[eid]
    total, hard = PRIOR[eid], []
    for f, val in inputs.items():
        for v in (val if isinstance(val, list) else [val]):
            x = w(eid, f, v)
            if x is None:
                continue
            total += x
            if x <= HARD:
                hard.append((f, v))
    for r in e.get("rules", []):
        if all(any(g in allowed for g in (inputs.get(f) if isinstance(inputs.get(f), list) else [inputs.get(f)]))
               for f, allowed in r["when"].items()):
            total += r["weight"]
    return total, hard


def rank(inputs, use_prior=True):
    live, excl = [], {}
    for eid in EID:
        t, hard = score(eid, inputs)
        if not use_prior:
            t -= PRIOR[eid]
        if hard:
            excl[eid] = (t, hard)
        else:
            live.append((eid, t))
    live.sort(key=lambda x: (-x[1], x[0]))
    return live, excl


def comp_rank(live, eid):
    """Competition rank (ties share a rank): 1 + number of live entities with a strictly higher score."""
    d = dict(live)
    return None if eid not in d else 1 + sum(1 for _, s in live if s > d[eid])


def valid(inp):
    """UI reachability of a (partial) input."""
    if "longitudinal" in inp and inp.get("bone_class") != "long_bone":
        return False
    if "margin_lodwick" in inp and (inp.get("density") not in ("lytic", "mixed") or inp.get("transverse") in SURF):
        return False
    if inp.get("transverse") in SURF and inp.get("cortex") == "endosteal_scalloping":
        return False
    if inp.get("transverse") == "juxtacortical_continuous" and inp.get("density") == "lytic":
        return False
    return all(v != "not_applicable" for v in inp.values())


def best(gain, rules, feats=None, fixed=None, const=0):
    """Maximise const + sum gain(f, v) + sum rule gains over reachable inputs (every feature may stay unfilled).
    gain(f, v) -> number or None (None = value not allowed). rules: [(when, weight)].
    feats: features that may be filled (default all). fixed: {feature: value} that must be present.
    Returns (best_total, assignment) or (None, None)."""
    feats = list(FO if feats is None else feats)
    fixed = fixed or {}
    rule_feats = {f for when, _ in rules for f in when}
    joint = [f for f in ("bone_class", "longitudinal", "transverse", "density", "margin_lodwick", "cortex")
             if f in feats]
    joint += [f for f in feats if f in rule_feats and f not in joint and f != "clinical_flags"]
    indep = [f for f in feats if f not in joint]
    base, assign0 = const, {}
    for f in indep:
        if f == "clinical_flags":
            if f in fixed:
                need = fixed[f] if isinstance(fixed[f], list) else [fixed[f]]
                if any(gain(f, v) is None for v in need):
                    return None, None
            else:
                need = []
            sel = list(need) + [v for v in VALS[f] if v not in need and (gain(f, v) or 0) > 0]
            base += sum(gain(f, v) for v in sel)
            if sel:
                assign0[f] = sel
            continue
        opts = [(0, None)] if f not in fixed else []
        for v in ([fixed[f]] if f in fixed else VALS[f]):
            g = gain(f, v)
            if g is not None:
                opts.append((g, v))
        if not opts:
            return None, None
        g, v = max(opts, key=lambda o: o[0])
        base += g
        if v is not None:
            assign0[f] = v
    options = []
    for f in joint:
        o = [] if f in fixed else [None]
        o += [v for v in ([fixed[f]] if f in fixed else VALS[f]) if gain(f, v) is not None]
        options.append(o)
    top, top_assign = None, None
    for combo in itertools.product(*options):
        inp = {f: v for f, v in zip(joint, combo) if v is not None}
        if not valid(inp):
            continue
        t = base + sum(gain(f, v) for f, v in inp.items())
        for when, rw in rules:
            if all(inp.get(f) in allowed for f, allowed in when.items()):
                t += rw
        if top is None or t > top:
            top, top_assign = t, dict(inp)
    if top is None:
        return None, None
    top_assign.update(assign0)
    return top, top_assign


def ent_gain(eid):
    return lambda f, v: (None if (w(eid, f, v) is not None and w(eid, f, v) <= HARD) else w0(eid, f, v))


def ent_rules(eid, sign=1):
    return [(r["when"], sign * r["weight"]) for r in ENT[eid].get("rules", [])]


def separation(a, b, fixed=None, feats=None):
    """Max of score(a) - score(b) over reachable inputs where neither is excluded (optionally within a fixed
    context and a restricted feature set). None when the context itself excludes one of the two."""
    def g(f, v):
        x, y = w(a, f, v), w(b, f, v)
        if (x is not None and x <= HARD) or (y is not None and y <= HARD):
            return None
        return (x or 0) - (y or 0)
    return best(g, ent_rules(a) + ent_rules(b, -1), feats=feats, fixed=fixed, const=PRIOR[a] - PRIOR[b])[0]


def fmt(inp):
    return ", ".join(f"{f}={'+'.join(v) if isinstance(v, list) else v}" for f, v in inp.items())


def table(headers, rows):
    print("| " + " | ".join(headers) + " |")
    print("|" + "|".join("---" for _ in headers) + "|")
    for r in rows:
        print("| " + " | ".join(str(x) for x in r) + " |")
    print()


def h(title):
    print("\n" + "=" * 100 + "\n" + title + "\n" + "=" * 100)


# ----------------------------------------------------------------------------------------------------------
# Reviewer judgement tables (hypotheses; nothing here is applied to the KB)
# ----------------------------------------------------------------------------------------------------------
# class a = justified, b = questionable (rare but reported / plausible in atypical, fractured, advanced cases),
# c = inconsistent with a sibling value or a closely related entity. proposed = weight to TEST in v0.7.
B, C = "b", "c"
HC_OVERRIDES = {
    # --- age
    ("giant_cell_tumour_of_bone", "age_group", "10-19_open"): (B, "GCTB pada skeletal imatur dilaporkan pada sebagian kecil kasus (lesi metafisis menempel fisis); aturan desain 'fisis terbuka = bukan GCTB' menyingkirkan kasus nyata ini", -2, "sedang"),
    ("bone_metastasis", "age_group", "10-19_open"): (C, "0-9 berbobot -2 tetapi seluruh dekade 10-19 berbobot -5; metastasis pada remaja (neuroblastoma, rabdomiosarkoma, karsinoma nasofaring) jarang tetapi nyata, dan flag riwayat keganasan tidak dapat menolongnya", -2, "sedang"),
    ("bone_metastasis", "age_group", "10-19_closed"): (C, "sama dengan 10-19_open: tidak konsisten dengan 0-9 (-2)", -2, "sedang"),
    ("bone_metastasis", "age_group", "10-19_unknown"): (C, "sama dengan 10-19_open: tidak konsisten dengan 0-9 (-2)", -2, "sedang"),
    ("chordoma", "age_group", "0-9"): (B, "Kordoma anak terdokumentasi (terutama basis kranii, tipe poorly differentiated); sangat jarang di sakrum/spine", -2, "rendah"),
    ("chordoma", "age_group", "10-19_open"): (B, "Kordoma remaja jarang tetapi dilaporkan (basis kranii > spine mobil)", -2, "rendah"),
    ("chordoma", "age_group", "10-19_closed"): (B, "Kordoma remaja jarang tetapi dilaporkan", -2, "rendah"),
    ("chordoma", "age_group", "10-19_unknown"): (B, "Kordoma remaja jarang tetapi dilaporkan", -2, "rendah"),
    ("intraosseous_ganglion_geode", "age_group", "0-9"): (B, "Kista subkondral pada anak dengan artropati (hemofilia, JIA) dilaporkan; ganglion intraoseus usia 11 th ada di V2-73", -2, "rendah"),
    ("chondroblastoma", "age_group", "40-59"): (B, "Kondroblastoma dewasa paruh baya dilaporkan, terutama di tulang pendek/pipih (kalkaneus, patela, temporal) yang oleh KB sendiri diberi +1", -2, "sedang"),
    ("chondroblastoma", "age_group", "60+"): (B, "Sama dengan 40-59; lebih jarang", -2, "rendah"),
    ("simple_bone_cyst", "age_group", "60+"): (B, "Kista simpel dewasa/lansia (femur proksimal, kalkaneus, ilium) dilaporkan; rujukan tersingkir di V3-34", -2, "sedang"),
    ("aneurysmal_bone_cyst", "age_group", "60+"): (B, "ABC primer usia lanjut sangat jarang tetapi dilaporkan", -2, "rendah"),
    ("ewing_sarcoma", "age_group", "60+"): (B, "Ewing usia >60 sangat jarang tetapi ada di registri; limfoma tetap banding utama", -2, "rendah"),
    ("langerhans_cell_histiocytosis", "age_group", "60+"): (B, "LCH dewasa dapat muncul pada usia berapa pun", -2, "rendah"),
    ("osteoblastoma", "age_group", "60+"): (B, "Osteoblastoma usia lanjut jarang tetapi dilaporkan", -2, "rendah"),
    ("osteoid_osteoma", "age_group", "60+"): (B, "Osteoid osteoma usia lanjut jarang tetapi dilaporkan", -2, "rendah"),
    ("osteosarcoma_periosteal", "age_group", "60+"): (B, "Rentang usia yang dilaporkan mencapai dekade ke-7", -2, "rendah"),
    # --- location
    ("simple_bone_cyst", "longitudinal", "epiphysis_apophysis"): (B, "Nilai ini mencakup apofisis: kista simpel trokanter mayor adalah lokasi yang dikenal; perluasan ke epifisis setelah fisis menutup juga dilaporkan", -2, "sedang"),
    ("osteochondroma", "longitudinal", "epiphysis_apophysis"): (B, "Nilai ini mencakup apofisis; osteokondroma di dekat apofisis (trokanter minor, tuberositas) dapat dikodekan demikian", -2, "rendah"),
    ("bpop_nora_lesion", "transverse", "juxtacortical_continuous"): (B, "BPOP dengan kesan kontinuitas korteks-meduler dilaporkan; rujukan tersingkir di V2-15", -2, "sedang"),
    # --- density
    ("bpop_nora_lesion", "density", "lytic"): (B, "BPOP dini/belum terosifikasi tampak radiolusen; rujukan tersingkir di V3-46", -2, "sedang"),
    ("chordoma", "density", "sclerotic"): (B, "Kordoma korpus vertebra mobil dapat sklerotik (ivory vertebra) pada sebagian kasus; KB memberi spine_body +2", -2, "sedang"),
    ("aneurysmal_bone_cyst", "density", "sclerotic"): (B, "ABC fase penyembuhan/involusi mengalami osifikasi", -2, "rendah"),
    ("simple_bone_cyst", "density", "sclerotic"): (B, "Kista yang menyembuh (pascafraktur) terisi tulang; riwayat sklerotik disebut pada V3-35", -2, "rendah"),
    # --- margin
    ("osteosarcoma_conventional", "margin_lodwick", "IA"): (B, "Osteosarkoma bertepi tegas/sklerotik yang meniru lesi jinak dilaporkan; rujukan tersingkir di V3-09", -2, "sedang"),
    ("osteosarcoma_telangiectatic", "margin_lodwick", "IA"): (B, "Entitas ini didefinisikan sebagai peniru ABC (ABC: IA +1); tepi sklerotik jarang tetapi mungkin", -2, "rendah"),
    ("ewing_sarcoma", "margin_lodwick", "IA"): (B, "Tepi sklerotik pada Ewing sangat tidak lazim tetapi dilaporkan", -2, "rendah"),
    ("intraosseous_ganglion_geode", "margin_lodwick", "IC"): (B, "Tepi sebagian tidak tegas pada ganglion intraoseus; rujukan tersingkir di V2-74", -2, "sedang"),
    ("fibrous_dysplasia", "margin_lodwick", "IC"): (B, "Lesi ground-glass sering berbaur bertahap dengan tulang normal (terutama kraniofasial, lesi panjang); tepi tidak selalu tegas", -2, "sedang"),
    ("chondromyxoid_fibroma", "margin_lodwick", "IC"): (B, "Sebagian kecil CMF tanpa tepi tegas; lompatan IB 0 -> IC -5. Catatan: CMF sudah over-called, uji bersama H penurunan bobot CMF", -2, "rendah"),
    ("simple_bone_cyst", "margin_lodwick", "IC"): (B, "Tepi kabur setelah fraktur patologis", -2, "rendah"),
    ("vertebral_haemangioma", "margin_lodwick", "IC"): (B, "Hemangioma agresif; penerapan Lodwick pada korpus vertebra sendiri meragukan", -2, "rendah"),
    ("brown_tumour", "margin_lodwick", "II"): (B, "Tulang hiperparatiroid dapat tampak agresif/berbintik; v0.6 sudah melonggarkan destruksi korteks untuk entitas ini", -2, "rendah"),
    ("osteoblastoma", "margin_lodwick", "II"): (B, "Osteoblastoma agresif dapat bertepi tidak tegas; lompatan IC 0 -> II -5", -2, "rendah"),
    ("adamantinoma_ofd_spectrum", "margin_lodwick", "II"): (B, "Adamantinoma klasik adalah keganasan dan dapat berarea destruktif; lompatan IC 0 -> II -5", -2, "rendah"),
    # --- cortex
    ("ewing_sarcoma", "cortex", "expansion_shell"): (B, "Ewing pada iga, fibula, dan tulang tubular kecil sering digambarkan ekspansil", -2, "sedang"),
    ("primary_bone_lymphoma", "cortex", "expansion_shell"): (B, "Ekspansi jarang tetapi dilaporkan", -2, "rendah"),
    ("chondroblastoma", "cortex", "destruction"): (B, "Kondroblastoma agresif dengan destruksi korteks dilaporkan; rujukan tersingkir di V3-06", -2, "sedang"),
    ("chondromyxoid_fibroma", "cortex", "destruction"): (B, "Korteks CMF dapat tampak hilang sebagian pada radiograf. Catatan: CMF sudah over-called", -2, "rendah"),
    ("vertebral_haemangioma", "cortex", "destruction"): (B, "Hemangioma vertebra agresif dengan penembusan korteks dan perluasan epidural", -2, "rendah"),
    ("bpop_nora_lesion", "cortex", "destruction"): (B, "Destruksi korteks disebut pada temuan operasi V3-46; klasiknya korteks utuh", -2, "rendah"),
    # --- soft tissue
    ("chondroblastoma", "soft_tissue_mass", "present"): (B, "Kondroblastoma agresif/dengan ABC sekunder dapat meluas ke jaringan lunak; rujukan tersingkir di V3-06", -2, "sedang"),
    ("intraosseous_ganglion_geode", "soft_tissue_mass", "present"): (B, "Ganglion intraoseus dapat berhubungan dengan ganglion jaringan lunak; rujukan tersingkir di V2-74", -2, "sedang"),
    ("stress_fracture", "soft_tissue_mass", "present"): (B, "Kalus/hematoma/edema periosteal dapat terbaca sebagai massa; pitfalls entitas sendiri menyebut kalus agresif", -2, "rendah"),
    ("simple_bone_cyst", "soft_tissue_mass", "present"): (B, "Hematoma fraktur patologis; definisi entitas menyebut fraktur sebagai presentasi tersering", -2, "rendah"),
    ("non_ossifying_fibroma", "soft_tissue_mass", "present"): (B, "Hematoma fraktur patologis pada lesi besar", -2, "rendah"),
    ("chondromyxoid_fibroma", "soft_tissue_mass", "present"): (B, "Perluasan jaringan lunak jarang tetapi dilaporkan. Catatan: CMF sudah over-called", -2, "rendah"),
    # --- periosteal
    ("osteosarcoma_conventional", "periosteal", "shell"): (C, "Temuan yang sama diberi -2 pada cortex=expansion_shell tetapi -5 pada periosteal=shell", -2, "sedang"),
    ("ewing_sarcoma", "periosteal", "shell"): (B, "Sejalan dengan cortex=expansion_shell: Ewing iga/tulang kecil ekspansil", -2, "rendah"),
    ("simple_bone_cyst", "periosteal", "lamellated"): (C, "Reaksi periosteal pascafraktur; v0.6 melonggarkan nilai yang sama untuk CMF (-2) tetapi tidak untuk lesi yang jauh lebih sering fraktur", -2, "sedang"),
    ("non_ossifying_fibroma", "periosteal", "lamellated"): (C, "Sama: fraktur patologis pada NOF besar; CMF sudah -2", -2, "sedang"),
    ("fibrous_dysplasia", "periosteal", "lamellated"): (C, "Sama: fraktur/shepherd's crook; CMF sudah -2", -2, "sedang"),
    ("enchondroma", "periosteal", "lamellated"): (B, "Fraktur patologis enkondroma tangan", -2, "rendah"),
    ("brown_tumour", "periosteal", "lamellated"): (B, "Fraktur patologis pada tulang hiperparatiroid", -2, "rendah"),
    ("osteoid_osteoma", "periosteal", "lamellated"): (B, "Reaksi solid terbentuk dari lamela yang menyatu; pada anak dapat tampak berlapis", -2, "rendah"),
    ("stress_fracture", "periosteal", "spiculated"): (B, "Pitfalls entitas sendiri: kalus agresif dapat meniru osteosarkoma", -2, "rendah"),
    # --- matrix
    ("osteomyelitis", "matrix", "osteoid"): (B, "Sekuestrum/involukrum dan sklerosis reaktif padat dapat dipilih pembaca sebagai 'osteoid (padat)'; menyingkirkan infeksi dari banding osteosarkoma berisiko di daerah endemik", -2, "sedang"),
    ("skeletal_tuberculosis", "matrix", "osteoid"): (B, "Sekuestrum pada TB (lebih jarang daripada piogenik)", -2, "rendah"),
    ("chondrosarcoma_central", "matrix", "osteoid"): (B, "Kalsifikasi kondroid padat dapat terbaca 'padat/cloud-like'; komponen dediferensiasi osteosarkomatosa disebut di pitfalls entitas", -2, "sedang"),
    ("enchondroma", "matrix", "osteoid"): (B, "Enkondroma terkalsifikasi padat dapat terbaca sebagai matriks padat", -2, "rendah"),
    ("clear_cell_chondrosarcoma", "matrix", "osteoid"): (B, "Secara histologis mengandung tulang woven; mineralisasi amorf mungkin", -2, "rendah"),
    ("periosteal_chondroma", "matrix", "osteoid"): (B, "Kondroma periosteal dapat mengalami osifikasi", -2, "rendah"),
    ("primary_bone_lymphoma", "matrix", "osteoid"): (B, "Sekuestrum dan sklerosis reaktif dilaporkan pada limfoma tulang", -2, "rendah"),
    ("langerhans_cell_histiocytosis", "matrix", "osteoid"): (B, "Button sequestrum dapat terbaca sebagai fokus padat", -2, "rendah"),
    ("aneurysmal_bone_cyst", "matrix", "osteoid"): (B, "ABC sekunder pada osteoblastoma; mineralisasi septa pada CT", -2, "rendah"),
    ("aneurysmal_bone_cyst", "matrix", "chondroid"): (B, "ABC sekunder pada kondroblastoma (disebut di pitfalls entitas)", -2, "rendah"),
    ("skeletal_tuberculosis", "matrix", "chondroid"): (B, "Kalsifikasi abses/kaseosa dapat terbaca sebagai kalsifikasi intralesi", -2, "rendah"),
    ("brown_tumour", "matrix", "ground_glass"): (B, "'Ground-glass' adalah deskriptor klasik tulang hiperparatiroid/osteodistrofi renal", -2, "sedang"),
    ("simple_bone_cyst", "matrix", "ground_glass"): (B, "Kista yang menyembuh terisi tulang berdensitas kabur", -2, "rendah"),
    ("bone_metastasis", "matrix", "ground_glass"): (B, "Metastasis blastik berdensitas kabur dapat disebut ground-glass oleh sebagian pembaca", -2, "rendah"),
    # --- size
    ("osteoid_osteoma", "size_cm", ">5"): (C, "KB menilai densitas lesi dari sklerosis reaktif (sclerotic +3) tetapi ukuran dari nidus; pembaca yang mengukur zona sklerosis (>5 cm) menyingkirkan diagnosis yang benar", -2, "sedang"),
    ("intraosseous_ganglion_geode", "size_cm", ">5"): (B, "Geode raksasa (RA, CPPD, OA lanjut) dilaporkan melebihi 5 cm", -2, "sedang"),
}
HC_DEFAULT = {
    "age_group": "Di luar rentang usia entitas menurut definisi/epidemiologi; tidak ditemukan alasan kuat untuk melonggarkan",
    "bone_class": "Lokasi bertentangan dengan definisi atau predileksi tetap entitas",
    "longitudinal": "Segmen bertentangan dengan definisi lokasi entitas",
    "transverse": "Posisi transversal bertentangan dengan definisi (lesi permukaan vs intrameduler; kontinuitas korteks-meduler khas osteokondroma)",
    "density": "Densitas bertentangan dengan definisi entitas",
    "margin_lodwick": "Tepi agresif/tepi sklerotik ini pada dasarnya tidak dilaporkan untuk entitas tanpa komplikasi",
    "cortex": "Perubahan korteks ini bertentangan dengan perilaku biologis entitas",
    "soft_tissue_mass": "Massa jaringan lunak sejati tidak diharapkan pada entitas ini",
    "periosteal": "Pola periosteal ini pada dasarnya tidak dilaporkan pada entitas ini",
    "matrix": "Jenis matriks ini bertentangan dengan garis diferensiasi entitas",
    "size_cm": "Ukuran bertentangan dengan definisi entitas",
}

# Claims the reviewer expected to find (direction only). The script prints what the KB actually holds.
EXPECTED = [
    ("osteoblastoma", "clinical_flags", "night_pain_nsaid_relief", "+", "nyeri malam; respons NSAID lebih lemah daripada osteoid osteoma"),
    ("osteomyelitis", "clinical_flags", "night_pain_nsaid_relief", "+", "abses Brodie meniru osteoid osteoma secara klinis"),
    ("stress_fracture", "clinical_flags", "night_pain_nsaid_relief", "0/-", "nyeri terkait beban; saat ini tidak dibedakan dari osteoid osteoma oleh flag ini"),
    ("ewing_sarcoma", "clinical_flags", "fever_or_infection_signs", "+", "demam dan penanda inflamasi sering pada Ewing; kini flag hanya menaikkan infeksi"),
    ("langerhans_cell_histiocytosis", "clinical_flags", "fever_or_infection_signs", "+", "LCH dapat disertai demam/penanda inflamasi (V1-24)"),
    ("primary_bone_lymphoma", "clinical_flags", "fever_or_infection_signs", "+", "gejala B"),
    ("plasmacytoma_myeloma", "clinical_flags", "known_primary_malignancy", "0", "tidak ada klaim; flag hanya menaikkan metastasis"),
    ("plasmacytoma_myeloma", "multiplicity", "solitary", "-", "multiple +3 tetapi soliter tidak dinilai"),
    ("bone_metastasis", "cortex", "endosteal_scalloping", "+", "metastasis ginjal/tiroid ekspansil-scalloping disebut di S-01"),
    ("bone_metastasis", "bone_class", "spine_posterior", "+", "destruksi pedikel adalah tanda klasik metastasis"),
    ("plasmacytoma_myeloma", "bone_class", "sacrum", "+", "plasmasitoma sakrum termasuk banding massa sakral"),
    ("plasmacytoma_myeloma", "periosteal", "shell", "+", "plasmasitoma ekspansil"),
    ("giant_cell_tumour_of_bone", "bone_class", "patella", "+", "GCTB dan kondroblastoma adalah banding klasik patela"),
    ("giant_cell_tumour_of_bone", "soft_tissue_mass", "absent", "0", "tidak dinilai"),
    ("osteosarcoma_conventional", "size_cm", ">5", "+", "sarkoma derajat tinggi umumnya besar saat diagnosis"),
    ("ewing_sarcoma", "size_cm", ">5", "+", "sda."),
    ("osteosarcoma_conventional", "size_cm", "<2", "-", "sda."),
    ("non_ossifying_fibroma", "size_cm", "<2", "+", "fibrous cortical defect <2 cm menurut definisi entitas"),
    ("enostosis", "matrix", "osteoid", "0/+", "pembaca dapat memilih 'osteoid (padat)' untuk pulau tulang; kini -2"),
    ("osteosarcoma_parosteal", "size_cm", ">5", "+", "pitfall BPOP menyebut parosteal OS lebih besar"),
    ("chordoma", "bone_class", "small_tubular_hand_foot", "-5", "long_bone dan flat_bone -5 tetapi tangan/kaki tanpa klaim"),
    ("chordoma", "bone_class", "clavicle", "-5", "sda."),
    ("chordoma", "bone_class", "calcaneus", "-5", "sda."),
    ("chordoma", "bone_class", "patella", "-5", "sda."),
    ("vertebral_haemangioma", "bone_class", "small_tubular_hand_foot", "-", "entitas vertebra; long_bone -2 tetapi tangan/kaki tanpa klaim"),
    ("vertebral_haemangioma", "bone_class", "spine_posterior", "+", "hemangioma sering meluas ke elemen posterior"),
    ("simple_bone_cyst", "periosteal", "shell", "0/+", "lesi ekspansil; shell tidak dinilai"),
    ("fibrous_dysplasia", "periosteal", "shell", "0/+", "sda."),
    ("skeletal_tuberculosis", "bone_class", "spine_posterior", "0", "tidak dinilai"),
    ("osteomyelitis", "multiplicity", "multiple", "+", "S-01: osteomielitis dapat multifokal pada anak"),
    ("ewing_sarcoma", "multiplicity", "multiple", "0", "S-01: dapat multifokal pada anak; tidak dinilai"),
]

# (name, members, context): the context fixes the shared setting of the group; sep_ctx is computed inside it
# on the 12 radiographic/demographic features (clinical_flags left out because it is optional and rarely filled).
MIMIC_GROUPS = [
    ("Lesi epifisis", ["giant_cell_tumour_of_bone", "chondroblastoma", "clear_cell_chondrosarcoma", "intraosseous_ganglion_geode"], {"bone_class": "long_bone", "longitudinal": "epiphysis_apophysis"}),
    ("Sel bulat kecil vs infeksi", ["ewing_sarcoma", "osteomyelitis", "langerhans_cell_histiocytosis", "primary_bone_lymphoma"], {"bone_class": "long_bone"}),
    ("Kondroid sentral", ["enchondroma", "chondrosarcoma_central", "bone_infarct"], {"bone_class": "long_bone", "transverse": "central"}),
    ("Litik ekspansil", ["aneurysmal_bone_cyst", "osteosarcoma_telangiectatic", "simple_bone_cyst", "giant_cell_tumour_of_bone"], {"bone_class": "long_bone", "density": "lytic"}),
    ("Fibro-oseus/eksentrik", ["non_ossifying_fibroma", "chondromyxoid_fibroma", "fibrous_dysplasia", "adamantinoma_ofd_spectrum"], {"bone_class": "long_bone"}),
    ("Nidus/sklerosis kortikal", ["osteoid_osteoma", "osteoblastoma", "stress_fracture", "osteomyelitis"], {"bone_class": "long_bone", "transverse": "cortical"}),
    ("Lesi permukaan", ["osteochondroma", "osteosarcoma_parosteal", "bpop_nora_lesion", "periosteal_chondroma", "osteosarcoma_periosteal"], {"bone_class": "long_bone", "transverse": "juxtacortical_surface"}),
    ("Dewasa/aksial", ["bone_metastasis", "plasmacytoma_myeloma", "primary_bone_lymphoma", "paget_disease", "vertebral_haemangioma"], {"bone_class": "spine_body"}),
    ("Sklerotik fokal", ["enostosis", "bone_metastasis", "osteoid_osteoma"], {"density": "sclerotic"}),
    ("Infeksi", ["osteomyelitis", "skeletal_tuberculosis"], {"bone_class": "spine_body"}),
    ("Sakrum", ["chordoma", "giant_cell_tumour_of_bone", "chondrosarcoma_central"], {"bone_class": "sacrum"}),
    ("Agresif anak/remaja", ["osteosarcoma_conventional", "ewing_sarcoma", "osteomyelitis"], {"bone_class": "long_bone"}),
]

# Constructed textbook vignettes (reviewer's own; NOT validation cases). Short keys as in tools/review_cases_v1_v4.txt.
VIGNETTES = [
    ("C01", "osteosarcoma_conventional", "14 th, femur distal metafisis, campuran moth-eaten, destruksi, massa, Codman, osteoid", "a=10o m=sol b=lb l=meta t=central d=mixed g=II c=destr s=pres p=codman x=osteoid z=>5"),
    ("C02", "osteosarcoma_telangiectatic", "16 th, tibia proksimal metafisis, litik ekspansil tepi tidak tegas, massa, Codman", "a=10u m=sol b=lb l=meta t=ecc d=lytic g=IC c=exp s=pres p=codman x=none z=>5"),
    ("C03", "osteosarcoma_parosteal", "32 th, femur distal posterior, massa permukaan padat terosifikasi, korteks utuh", "a=20-39 m=sol b=lb l=meta t=jsurf d=scl c=intact p=none x=osteoid z=>5"),
    ("C04", "osteosarcoma_periosteal", "17 th, tibia diafisis, massa permukaan, saucerization, spikula tegak lurus", "a=10c m=sol b=lb l=dia t=jsurf d=mixed c=sauc s=pres p=spic x=chondroid z=>5"),
    ("C05", "osteoid_osteoma", "22 th, femur diafisis, sklerosis kortikal, periosteal solid, nidus <2 cm, nyeri malam", "a=20-39 m=sol b=lb l=dia t=cortical d=scl c=intact s=abs p=solid x=none z=<2 k=night"),
    ("C06", "osteoblastoma", "18 th, elemen posterior vertebra, ekspansil campuran dengan osteoid, 3 cm", "a=10c m=sol b=sp d=mixed g=IA c=exp s=abs p=none x=osteoid z=2-5"),
    ("C07", "osteochondroma", "12 th, femur distal metafisis, eksostosis dengan kontinuitas korteks-meduler", "a=10o m=sol b=lb l=meta t=jcont d=scl c=intact s=abs p=none x=none z=2-5"),
    ("C08", "enchondroma", "45 th, humerus proksimal metafisis, sentral, kalsifikasi ring-and-arc, tanpa scalloping", "a=40-59 m=sol b=lb l=meta t=central d=mixed g=IB c=intact s=abs p=none x=chondroid z=2-5"),
    ("C09", "enchondroma", "30 th, falang proksimal, litik sentral ekspansil dengan kalsifikasi kondroid", "a=20-39 m=sol b=hf t=central d=lytic g=IB c=exp s=abs p=none x=chondroid z=<2"),
    ("C10", "periosteal_chondroma", "25 th, humerus proksimal, lesi permukaan dengan saucerization dan penyangga, kalsifikasi kondroid", "a=20-39 m=sol b=lb l=meta t=jsurf d=lytic c=sauc s=abs p=solid x=chondroid z=2-5"),
    ("C11", "chondroblastoma", "15 th fisis terbuka, epifisis tibia proksimal, litik eksentrik tepi sklerotik, kalsifikasi halus", "a=10o m=sol b=lb l=epi t=ecc d=lytic g=IA c=intact s=abs p=none x=chondroid z=2-5"),
    ("C12", "chondromyxoid_fibroma", "22 th, tibia proksimal metafisis, litik eksentrik berlobus tepi sklerotik, ekspansi", "a=20-39 m=sol b=lb l=meta t=ecc d=lytic g=IA c=exp s=abs p=none x=none z=2-5"),
    ("C13", "chondrosarcoma_central", "58 th, femur proksimal metadiafisis, sentral, scalloping dalam, kondroid, >5 cm", "a=40-59 m=sol b=lb l=md t=central d=mixed g=IC c=scal s=abs p=none x=chondroid z=>5"),
    ("C14", "chondrosarcoma_central", "55 th, ilium, campuran dengan kalsifikasi kondroid, destruksi korteks, massa besar", "a=40-59 m=sol b=flat t=central d=mixed g=IC c=destr s=pres p=none x=chondroid z=>5"),
    ("C15", "clear_cell_chondrosarcoma", "38 th, kaput femur, litik berbatas tegas tanpa tepi sklerotik, kalsifikasi", "a=20-39 m=sol b=lb l=epi t=central d=lytic g=IB c=intact s=abs p=none x=chondroid z=2-5"),
    ("C16", "desmoplastic_fibroma", "24 th, femur distal metafisis, litik sentral ekspansil dengan pseudotrabekulasi, tanpa matriks", "a=20-39 m=sol b=lb l=meta t=central d=lytic g=IB c=exp s=abs p=none x=none z=>5"),
    ("C17", "vertebral_haemangioma", "50 th, korpus vertebra, trabekula vertikal kasar, korteks utuh", "a=40-59 m=sol b=sb t=central d=mixed c=intact s=abs p=none x=coarse_trabeculae z=2-5"),
    ("C18", "aneurysmal_bone_cyst", "13 th fisis terbuka, femur distal metafisis, litik eksentrik blow-out dengan cangkang tipis", "a=10o m=sol b=lb l=meta t=ecc d=lytic g=IB c=exp s=abs p=shell x=none z=>5"),
    ("C19", "non_ossifying_fibroma", "11 th fisis terbuka, tibia distal metafisis, litik eksentrik tepi sklerotik berlobus", "a=10o m=sol b=lb l=meta t=ecc d=lytic g=IA c=intact s=abs p=none x=none z=2-5"),
    ("C20", "giant_cell_tumour_of_bone", "30 th, radius distal epi-metafisis sampai subkondral, litik eksentrik tanpa tepi sklerotik", "a=20-39 m=sol b=lb l=epi t=ecc d=lytic g=IB c=exp s=abs p=none x=none z=>5"),
    ("C21", "chordoma", "62 th, sakrum garis tengah, litik destruktif dengan massa presakral besar", "a=60+ m=sol b=sacrum t=central d=lytic g=IC c=destr s=pres p=none x=none z=>5"),
    ("C22", "simple_bone_cyst", "9 th, humerus proksimal metafisis, litik sentral, korteks menipis", "a=0-9 m=sol b=lb l=meta t=central d=lytic g=IB c=exp s=abs p=none x=none z=>5"),
    ("C23", "fibrous_dysplasia", "20 th, femur proksimal metadiafisis, ground-glass dengan rind sklerotik, ekspansi", "a=20-39 m=sol b=lb l=md t=central d=mixed g=IA c=exp s=abs p=none x=gg z=>5"),
    ("C24", "adamantinoma_ofd_spectrum", "28 th, tibia diafisis anterior, kortikal, multilokuler campuran, ekspansi", "a=20-39 m=sol b=lb l=dia t=cortical d=mixed g=IA c=exp s=abs p=none x=none z=>5"),
    ("C25", "adamantinoma_ofd_spectrum", "6 th (OFD), tibia diafisis anterior, kortikal, litik tepi sklerotik, bowing", "a=0-9 m=sol b=lb l=dia t=cortical d=lytic g=IA c=exp s=abs p=none x=none z=2-5"),
    ("C26", "intraosseous_lipoma", "48 th, kalkaneus, lusen tepi sklerotik tipis, korteks utuh", "a=40-59 m=sol b=calcaneus t=central d=lytic g=IA c=intact s=abs p=none x=none z=2-5"),
    ("C27", "intraosseous_lipoma", "45 th, femur intertrokanter, lusen sentral tepi sklerotik", "a=40-59 m=sol b=lb l=meta t=central d=lytic g=IA c=intact s=abs p=none x=none z=2-5"),
    ("C28", "bpop_nora_lesion", "30 th, falang proksimal, massa termineralisasi menempel di permukaan, korteks utuh, tanpa kontinuitas", "a=20-39 m=sol b=hf t=jsurf d=scl c=intact s=abs p=none x=osteoid z=<2"),
    ("C29", "plasmacytoma_myeloma", "66 th, pelvis, lesi litik punched-out multipel dengan scalloping", "a=60+ m=mult b=flat t=central d=lytic g=IB c=scal s=abs p=none x=none"),
    ("C30", "plasmacytoma_myeloma", "55 th, plasmasitoma soliter korpus vertebra, litik ekspansil dengan massa", "a=40-59 m=sol b=sb d=lytic g=IB c=exp s=pres p=none x=none"),
    ("C31", "primary_bone_lymphoma", "50 th, femur metadiafisis, permeatif, korteks relatif utuh, massa besar, lamelar", "a=40-59 m=sol b=lb l=md t=central d=lytic g=III c=intact s=pres p=lam x=none z=>5"),
    ("C32", "langerhans_cell_histiocytosis", "6 th, femur diafisis, litik sentral berbatas tegas, scalloping, periosteal lamelar", "a=0-9 m=sol b=lb l=dia t=central d=lytic g=IB c=scal s=abs p=lam x=none z=2-5"),
    ("C33", "ewing_sarcoma", "12 th, femur diafisis, moth-eaten, korteks terputus fokal, massa besar, onion-skin", "a=10o m=sol b=lb l=dia t=central d=lytic g=II c=fb s=pres p=lam x=none z=>5"),
    ("C34", "ewing_sarcoma", "24 th, ilium, permeatif dengan massa jaringan lunak besar", "a=20-39 m=sol b=flat t=central d=lytic g=III c=fb s=pres p=none x=none z=>5"),
    ("C35", "bone_metastasis", "66 th, riwayat karsinoma, femur proksimal, litik moth-eaten destruktif, lesi multipel", "a=60+ m=mult b=lb l=md t=central d=lytic g=II c=destr s=pres p=none x=none k=primary"),
    ("C36", "bone_metastasis", "70 th, riwayat karsinoma prostat, pelvis, fokus sklerotik multipel", "a=60+ m=mult b=flat t=central d=scl c=intact s=abs p=none x=none k=primary"),
    ("C37", "osteomyelitis", "7 th, demam, tibia proksimal metafisis, litik tidak tegas, periosteal lamelar", "a=0-9 m=sol b=lb l=meta t=central d=lytic g=IC c=fb s=abs p=lam x=none k=fever"),
    ("C38", "osteomyelitis", "14 th (abses Brodie), tibia distal metafisis, litik lonjong tepi sklerotik tebal, periosteal solid", "a=10o m=sol b=lb l=meta t=central d=lytic g=IA c=intact s=abs p=solid x=none z=2-5"),
    ("C39", "skeletal_tuberculosis", "30 th, korpus vertebra, destruksi litik dengan massa paravertebral, demam subfebris", "a=20-39 m=sol b=sb d=lytic g=IC c=destr s=pres p=none x=none k=fever"),
    ("C40", "skeletal_tuberculosis", "8 th, femur distal epi-metafisis melintasi fisis, litik dengan penembusan korteks", "a=0-9 m=sol b=lb l=epi t=ecc d=lytic g=IB c=fb s=pres p=none x=none z=2-5"),
    ("C41", "intraosseous_ganglion_geode", "55 th, subkondral tibia proksimal, kista kecil tepi sklerotik", "a=40-59 m=sol b=lb l=epi t=ecc d=lytic g=IA c=intact s=abs p=none x=none z=<2"),
    ("C42", "bone_infarct", "52 th, femur distal metadiafisis, sentral, sklerosis serpiginosa, multipel", "a=40-59 m=mult b=lb l=md t=central d=mixed g=IA c=intact s=abs p=none x=none"),
    ("C43", "stress_fracture", "22 th pelari, tibia diafisis, sklerosis kortikal dengan periosteal solid", "a=20-39 m=sol b=lb l=dia t=cortical d=scl c=intact s=abs p=solid x=none"),
    ("C44", "stress_fracture", "72 th (insufisiensi), sakrum, pita sklerotik", "a=60+ m=sol b=sacrum d=scl c=intact s=abs p=none x=none"),
    ("C45", "paget_disease", "70 th, tibia proksimal mulai subartikular, campuran, trabekula kasar, tulang membesar", "a=60+ m=sol b=lb l=epi t=central d=mixed g=IB c=exp s=abs p=none x=coarse_trabeculae z=>5"),
    ("C46", "paget_disease", "68 th, korpus vertebra, sklerotik membesar dengan trabekula kasar", "a=60+ m=sol b=sb d=scl c=exp s=abs p=none x=coarse_trabeculae"),
    ("C47", "brown_tumour", "45 th, lesi litik ekspansil multipel tulang panjang, tanpa matriks", "a=40-59 m=mult b=lb l=dia t=ecc d=lytic g=IB c=exp s=abs p=none x=none z=2-5"),
    ("C48", "enostosis", "40 th, femur proksimal metafisis, fokus sklerotik homogen <2 cm", "a=40-59 m=sol b=lb l=meta t=central d=scl c=intact s=abs p=none x=none z=<2"),
]

KEYS = {"a": "age_group", "m": "multiplicity", "b": "bone_class", "l": "longitudinal", "t": "transverse", "d": "density",
        "g": "margin_lodwick", "c": "cortex", "s": "soft_tissue_mass", "p": "periosteal", "x": "matrix", "z": "size_cm",
        "k": "clinical_flags"}
ALIAS = {"lb": "long_bone", "hf": "small_tubular_hand_foot", "flat": "flat_bone", "sb": "spine_body", "sp": "spine_posterior",
         "cranio": "craniofacial", "epi": "epiphysis_apophysis", "meta": "metaphysis", "md": "metadiaphysis", "dia": "diaphysis",
         "na": "not_applicable", "ecc": "eccentric", "jsurf": "juxtacortical_surface", "jcont": "juxtacortical_continuous",
         "scl": "sclerotic", "scal": "endosteal_scalloping", "exp": "expansion_shell", "fb": "focal_breach", "destr": "destruction",
         "sauc": "saucerization", "solid": "solid_thin", "lam": "lamellated", "spic": "spiculated", "unspec": "present_unspecified",
         "gg": "ground_glass", "sol": "solitary", "mult": "multiple", "abs": "absent", "pres": "present",
         "night": "night_pain_nsaid_relief", "primary": "known_primary_malignancy", "fever": "fever_or_infection_signs",
         "10o": "10-19_open", "10c": "10-19_closed", "10u": "10-19_unknown"}


def parse(s):
    out = {}
    for tok in s.split():
        k, v = tok.split("=", 1)
        f = KEYS[k]
        vals = [ALIAS.get(x, x) for x in v.split(",")]
        for x in vals:
            if x not in [c["code"] for c in FEAT[f]["values"]]:
                raise SystemExit(f"unknown value {f}:{x}")
        out[f] = vals if f == "clinical_flags" else vals[0]
    return out


def load_cases():
    """Coded validation cases: project JSON if present locally, else the compact transcription."""
    cases = []
    js = [ROOT / f"data/validation/cases_v{i}.json" for i in (1, 2, 3, 4)]
    if all(p.exists() for p in js):
        for p in js:
            for c in json.loads(p.read_text(encoding="utf-8")):
                r = c.get("result", {})
                cases.append((c["case_id"], c["truth_entity_id"], c.get("typicality", "?")[:1].upper(),
                              r.get("rank") or 0, r.get("truth_score"), c["features"]))
        return cases, "data/validation/cases_v1..v4.json"
    p = ROOT / "tools/review_cases_v1_v4.txt"
    if not p.exists():
        return [], None
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        cid, truth, typ, rk, sc, feats = line.split("|")
        cases.append((cid, truth, typ, int(rk), int(sc), parse(feats)))
    return cases, "tools/review_cases_v1_v4.txt (transkripsi ringkas)"


# ----------------------------------------------------------------------------------------------------------
def part0():
    h("0. HITUNGAN DASAR DAN HIGIENE DATA")
    counts, nclaims, na, offscale, nosrc, badsrc = collections.Counter(), 0, [], [], [], []
    only_s01 = with_s01 = 0
    src_use = collections.Counter()
    combo = collections.Counter()
    hard_no_note = hard_total = note_total = 0
    axial_only_s01 = axial_total = 0
    citeonly_only = 0
    for e in ENTS:
        for f, d in e["feature_weights"].items():
            if f not in FEAT:
                offscale.append((e["id"], f, "unknown feature"))
            for v, c in d.items():
                nclaims += 1
                if v == "not_applicable":
                    na.append((e["id"], f, c["weight"]))
                else:
                    counts[c["weight"]] += 1
                    if v not in VALS.get(f, []):
                        offscale.append((e["id"], f, v))
                if c["weight"] not in SCALE:
                    offscale.append((e["id"], f, v, c["weight"]))
                s = c.get("source_ids", [])
                if not s:
                    nosrc.append((e["id"], f, v))
                badsrc += [(e["id"], f, v, x) for x in s if x not in SRC]
                for x in s:
                    src_use[x] += 1
                combo[",".join(s)] += 1
                only_s01 += s == ["S-01"]
                with_s01 += "S-01" in s
                if all(SRC.get(x, {}).get("license_status") == "cite_only" for x in s) and s:
                    citeonly_only += 1
                if c.get("note_id"):
                    note_total += 1
                if c["weight"] <= HARD:
                    hard_total += 1
                    hard_no_note += not c.get("note_id")
                if (f == "bone_class" and v in ("spine_body", "spine_posterior", "sacrum", "craniofacial")):
                    axial_total += 1
                    axial_only_s01 += s == ["S-01"]
    nrules = sum(len(e.get("rules", [])) for e in ENTS)
    print(f"entitas {len(ENTS)}; nilai fitur ditawarkan {sum(len(v) for v in VALS.values())}; klaim total {nclaims} "
          f"(termasuk {len(na)} not_applicable); klaim pada nilai yang ditawarkan {nclaims - len(na)}; aturan {nrules}")
    print("distribusi bobot (nilai ditawarkan):", dict(sorted(counts.items(), reverse=True)))
    print("hard constraint:", hard_total, "; tanpa note_id:", hard_no_note)
    print("klaim dengan note_id:", note_total, "dari", nclaims)
    print("klaim not_applicable (tersembunyi di UI):", na)
    print("bobot di luar skala / nilai tak dikenal:", offscale or "tidak ada")
    print("klaim tanpa source_ids:", nosrc or "tidak ada", "; source id tak terdaftar:", badsrc or "tidak ada")
    print(f"klaim yang hanya mengutip S-01: {only_s01} dari {nclaims} ({only_s01 / nclaims * 100:.1f}%); "
          f"klaim yang mengutip S-01 (sendiri atau bersama): {with_s01} ({with_s01 / nclaims * 100:.1f}%)")
    print(f"klaim yang hanya mengutip sumber cite-only: {citeonly_only}")
    print(f"klaim bone_class aksial/kraniofasial (spine_body, spine_posterior, sacrum, craniofacial): {axial_total}; "
          f"di antaranya hanya mengutip S-01 (review skeleton apendikular): {axial_only_s01}")
    table(["Kombinasi sumber pada klaim", "Jumlah klaim"], combo.most_common())
    table(["Sumber", "Lisensi", "Status", "Dipakai pada klaim"],
          [(s, SRC[s].get("license"), SRC[s].get("license_status"), src_use.get(s, 0)) for s in SRC])
    print(f"sumber terdaftar: {len(SRC)}; tidak dikutip oleh klaim mana pun: {sum(1 for x in SRC if not src_use.get(x))}")
    hard_only_s01 = sum(1 for e in ENTS for f, d in e["feature_weights"].items() for v, c in d.items()
                        if c["weight"] <= HARD and c["source_ids"] == ["S-01"])
    p3 = sum(1 for e in ENTS for f, d in e["feature_weights"].items() for v, c in d.items() if c["weight"] == 3)
    p3_only = sum(1 for e in ENTS for f, d in e["feature_weights"].items() for v, c in d.items()
                  if c["weight"] == 3 and c["source_ids"] == ["S-01"])
    print(f"hard constraint yang hanya mengutip S-01: {hard_only_s01} dari {hard_total}; "
          f"+3 yang hanya mengutip S-01: {p3_only} dari {p3}")
    ent_only = [e["id"] for e in ENTS if all(c["source_ids"] == ["S-01"] for d in e["feature_weights"].values() for c in d.values())]
    print(f"entitas yang SEMUA klaimnya hanya mengutip S-01 ({len(ent_only)}):", ", ".join(ent_only))
    print("Sumber kedua per entitas (kombinasi sumber terbanyak pada klaimnya):")
    for e in ENTS:
        cc = collections.Counter(",".join(c["source_ids"]) for d in e["feature_weights"].values() for c in d.values())
        print(f"  {SHORT[e['id']]}: sumber entitas {e['source_ids']}; klaim: " + "; ".join(f"{k} x{v}" for k, v in cc.most_common()))
    print("aturan khusus:")
    for e in ENTS:
        for r in e.get("rules", []):
            blocked = [(f, v) for f, allowed in r["when"].items() for v in allowed if (w(e["id"], f, v) or 0) <= HARD]
            print(f"  {e['id']}.{r['id']} bobot {r['weight']} when {r['when']} sumber {r['source_ids']}"
                  f"{' | nilai when yang sendiri -5: ' + str(blocked) if blocked else ''}")
    print("prior:", dict(collections.Counter(PRIOR.values())))
    print("entitas tanpa definition_id/pitfalls_id:", [e["id"] for e in ENTS if not e.get("definition_id") or not e.get("pitfalls_id")] or "tidak ada")


def part1(cases):
    h("1. HARD CONSTRAINT")
    rows = []
    for e in ENTS:
        for f in FO:
            for v in VALS[f]:
                c = e["feature_weights"].get(f, {}).get(v)
                if c and c["weight"] <= HARD:
                    cls, reason, prop, conf = HC_OVERRIDES.get((e["id"], f, v), ("a", HC_DEFAULT[f], "tetap -5", "sedang"))
                    rows.append((e["id"], f, v, cls, reason, prop, conf, ",".join(c["source_ids"])))
    unknown = [k for k in HC_OVERRIDES if (w(*k) or 0) > HARD]
    if unknown:
        raise SystemExit(f"HC_OVERRIDES refers to non-hard claims: {unknown}")
    out = ROOT / "docs/tinjauan-skor-v0.6-hard-constraints.csv"
    with out.open("w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh)
        wr.writerow(["entity", "feature", "value", "class", "reason", "proposed", "confidence", "cited_sources"])
        wr.writerows(rows)
    print(f"total hard constraint: {len(rows)} -> {out.relative_to(ROOT)}")
    cc = collections.Counter(r[3] for r in rows)
    print("kelas:", dict(cc), "| keyakinan pada kelas b/c:", dict(collections.Counter(r[6] for r in rows if r[3] != "a")))
    table(["Fitur", "-5 total", "a", "b", "c"],
          [(f, sum(1 for r in rows if r[1] == f), *(sum(1 for r in rows if r[1] == f and r[3] == k) for k in "abc")) for f in FO
           if any(r[1] == f for r in rows)])
    print("Kelas b/c dengan keyakinan sedang:")
    table(["Entitas", "Fitur:nilai", "Kelas", "Usul uji", "Alasan"],
          [(SHORT[r[0]], f"{r[1]}:{r[2]}", r[3], r[5], r[4]) for r in rows if r[3] != "a" and r[6] == "sedang"])
    # per value
    per_val = collections.Counter((r[1], r[2]) for r in rows)
    print("Nilai fitur menurut jumlah entitas yang disingkirkan (>= 9):")
    table(["Fitur:nilai", "Entitas disingkirkan", "% dari 37", "juga -2", "positif (>=1)"],
          [(f"{f}:{v}", n, f"{n / len(ENTS) * 100:.0f}%", sum(1 for x in EID if w(x, f, v) == -2),
            sum(1 for x in EID if (w(x, f, v) or 0) >= 1)) for (f, v), n in per_val.most_common() if n >= 9])
    print("Semua nilai dengan >=1 hard constraint:", "; ".join(f"{f}:{v}={n}" for (f, v), n in per_val.most_common()))
    per_ent = collections.Counter(r[0] for r in rows)
    table(["Entitas", "jumlah -5", "kelas b/c"], [(SHORT[k], n, sum(1 for r in rows if r[0] == k and r[3] != "a"))
                                                  for k, n in per_ent.most_common()])
    # combined exclusion: how many entities survive typical aggressive / benign combos
    for label, inp in [("agresif: margin III + destruction + massa + spiculated", {"margin_lodwick": "III", "cortex": "destruction", "soft_tissue_mass": "present", "periosteal": "spiculated"}),
                       ("ground_glass saja", {"matrix": "ground_glass"}),
                       ("juxtacortical_continuous saja", {"transverse": "juxtacortical_continuous"}),
                       ("osteoid + sclerotic", {"matrix": "osteoid", "density": "sclerotic"})]:
        live, excl = rank(inp)
        print(f"  input [{label}]: tersisa {len(live)} entitas, disingkirkan {len(excl)}")
    # cliffs on ordered features
    order = {"age_group": [["0-9"], ["10-19_open", "10-19_closed", "10-19_unknown"], ["20-39"], ["40-59"], ["60+"]],
             "longitudinal": [["epiphysis_apophysis"], ["metaphysis"], ["metadiaphysis"], ["diaphysis"]],
             "margin_lodwick": [["IA"], ["IB"], ["IC"], ["II"], ["III"]],
             "size_cm": [["<2"], ["2-5"], [">5"]]}
    cliffs = []
    for eid in EID:
        for f, levels in order.items():
            for i, lv in enumerate(levels):
                for v in lv:
                    if (w(eid, f, v) or 0) <= HARD:
                        neigh = [x for j in (i - 1, i + 1) if 0 <= j < len(levels) for x in levels[j]]
                        hi = max((w0(eid, f, x) for x in neigh), default=None)
                        if hi is not None and hi >= 0:
                            cliffs.append((SHORT[eid], f"{f}:{v}", hi))
    print(f"'Tebing' pada fitur berurutan (nilai -5 bersebelahan dengan nilai >= 0): {len(cliffs)}")
    table(["Entitas", "Nilai -5", "Bobot tertinggi nilai tetangga"], cliffs)
    # 10-19 triple consistency
    print("Tiga nilai 10-19 (open/closed/unknown) yang tidak seragam:")
    tri = []
    for eid in EID:
        t = tuple(w(eid, "age_group", v) for v in ("10-19_open", "10-19_closed", "10-19_unknown"))
        if len(set(t)) > 1:
            lo, hi = min(t[0], t[1]), max(t[0], t[1])
            note = "unknown = nilai tertinggi" if t[2] == hi and hi != lo else ("unknown di antara" if lo < t[2] < hi else ("unknown = nilai terendah" if t[2] == lo else "unknown di luar rentang"))
            tri.append((SHORT[eid], *t, note))
    table(["Entitas", "open", "closed", "unknown", "Catatan"], tri)
    # validation evidence
    if cases:
        print("Kasus uji v1-v4 dengan entitas rujukan tersingkir oleh hard constraint pada KB ini:")
        ev = []
        for cid, truth, typ, rk, sc, feats in cases:
            if truth not in ENT:
                continue
            t, hard = score(truth, feats)
            if hard:
                ev.append((cid, SHORT[truth], typ, "; ".join(f"{f}={v}" for f, v in hard), t))
        table(["Kasus", "Rujukan", "T/A", "Klaim -5 yang menyingkirkan", "Skor"], ev)
        print(f"  {len(ev)} dari {len(cases)} kasus")


def part2():
    h("2. KESEIMBANGAN STRUKTURAL")
    rows = []
    stats = {}
    for eid in EID:
        cl = [(f, v, w(eid, f, v)) for f in FO for v in VALS[f] if w(eid, f, v) is not None]
        cnt = collections.Counter(x[2] for x in cl)
        full, afull = best(ent_gain(eid), ent_rules(eid), const=PRIOR[eid])
        core, acore = best(ent_gain(eid), ent_rules(eid), feats=CORE6, const=PRIOR[eid])
        three, _ = best(ent_gain(eid), ent_rules(eid), feats=["age_group", "bone_class", "density"], const=PRIOR[eid])
        f3 = sum(1 for f in FO if any(w(eid, f, v) == 3 for v in VALS[f]))
        mean = sum(x[2] for x in cl) / sum(len(VALS[f]) for f in FO)
        stats[eid] = dict(n=len(cl), p3=cnt[3], f3=f3, full=full, core=core, three=three, hard=cnt[-5], afull=afull, acore=acore,
                          neg=cnt[-2] + cnt[-5], mean=mean, full0=full - PRIOR[eid], core0=core - PRIOR[eid])
        rows.append((SHORT[eid], PRIOR[eid], len(cl), cnt[3], f3, cnt[2], cnt[1], cnt[0], cnt[-2], cnt[-5], f"{mean:+.2f}", full, full - PRIOR[eid], core, three))
    rows.sort(key=lambda r: -r[11])
    table(["Entitas", "prior", "klaim", "+3", "fitur ber-+3", "+2", "+1", "0", "-2", "-5", "rata-rata bobot/nilai", "maks semua fitur", "maks tanpa prior", "maks 6 fitur inti", "maks usia+tulang+densitas"], rows)
    for pr in (0, -1, -2):
        g = [e for e in EID if PRIOR[e] == pr]
        med = lambda xs: sorted(xs)[len(xs) // 2]
        print(f"prior {pr}: n={len(g)}; median maks tanpa prior {med([stats[e]['full0'] for e in g])}; median maks 6 inti tanpa prior {med([stats[e]['core0'] for e in g])}; "
              f"median jumlah +3 {med([stats[e]['p3'] for e in g])}; median fitur ber-+3 {med([stats[e]['f3'] for e in g])}")
    for key, lab in (("full", "maks semua fitur"), ("core", "maks 6 fitur inti"), ("three", "maks 3 fitur"), ("n", "jumlah klaim"), ("p3", "jumlah +3")):
        xs = sorted(s[key] for s in stats.values())
        print(f"{lab}: min {xs[0]}, median {xs[len(xs) // 2]}, maks {xs[-1]}, rentang {xs[-1] - xs[0]}")

    def pearson(a, b):
        n = len(a); ma, mb = sum(a) / n, sum(b) / n
        cov = sum((x - ma) * (y - mb) for x, y in zip(a, b))
        va = sum((x - ma) ** 2 for x in a) ** .5; vb = sum((y - mb) ** 2 for y in b) ** .5
        return cov / (va * vb)
    print(f"korelasi Pearson jumlah +3 vs maks semua fitur: {pearson([s['p3'] for s in stats.values()], [s['full'] for s in stats.values()]):.2f}; "
          f"jumlah klaim vs maks: {pearson([s['n'] for s in stats.values()], [s['full'] for s in stats.values()]):.2f}; "
          f"prior vs maks: {pearson([PRIOR[e] for e in EID], [stats[e]['full'] for e in EID]):.2f}")
    # negative-findings bonus
    NEGF = [("cortex", "intact"), ("periosteal", "none"), ("matrix", "none"), ("soft_tissue_mass", "absent")]
    nb = sorted(((SHORT[e], *(w(e, f, v) if w(e, f, v) is not None else "." for f, v in NEGF), sum(w0(e, f, v) for f, v in NEGF)) for e in EID), key=lambda r: -r[-1])
    print("Skor dari empat temuan 'normal/tidak ada' (cortex=intact, periosteal=none, matrix=none, soft_tissue_mass=absent):")
    table(["Entitas", "cortex intact", "periosteal none", "matrix none", "massa absent", "jumlah"], nb)
    print(f"jumlah +3 pada empat nilai tersebut: {sum(1 for e in EID for f, v in NEGF if w(e, f, v) == 3)}; rentang jumlah: {nb[-1][-1]} sampai {nb[0][-1]}")
    # hidden baseline: features whose weights never go below +1 for an entity act like an extra prior
    MAINB = ["long_bone", "flat_bone", "spine_body"]
    hb = []
    for e in EID:
        a = min(w0(e, "age_group", v) for v in VALS["age_group"])
        d = min(w0(e, "density", v) for v in VALS["density"])
        b = min(w0(e, "bone_class", v) for v in MAINB)
        amean = sum(w0(e, "age_group", v) for v in VALS["age_group"]) / len(VALS["age_group"])
        hb.append((SHORT[e], a, f"{amean:+.1f}", d, b, max(a, 0) + max(d, 0) + max(b, 0)))
    hb.sort(key=lambda r: -r[-1])
    print("Bobot minimum pada fitur yang hampir selalu diisi (bila > 0, fitur itu selalu menambah skor = prior tersembunyi):")
    table(["Entitas", "min usia", "rata-rata usia", "min densitas", "min tulang (long/flat/spine_body)", "jumlah minimum positif"], [r for r in hb if r[-1] > 0])
    # +3 inflation per value
    print("Nilai fitur menurut jumlah entitas yang memberinya +3 ('ciri khas'); >= 7 entitas:")
    inf = sorted(((f"{f}:{v}", sum(1 for e in EID if w(e, f, v) == 3), sum(1 for e in EID if w(e, f, v) == 2)) for f in FO for v in VALS[f]), key=lambda r: -r[1])
    table(["Fitur:nilai", "entitas dengan +3", "entitas dengan +2"], [r for r in inf if r[1] >= 7])
    print(f"nilai dengan tepat satu entitas ber-+3: {sum(1 for r in inf if r[1] == 1)}; nilai tanpa +3: {sum(1 for r in inf if r[1] == 0)}; nilai dengan >=7 entitas ber-+3: {sum(1 for r in inf if r[1] >= 7)}")
    print("Input terbaik (semua fitur) untuk tiga entitas tertinggi dan tiga terendah:")
    for eid in sorted(EID, key=lambda x: -stats[x]["full"])[:3] + sorted(EID, key=lambda x: stats[x]["full"])[:3]:
        print(f"  {SHORT[eid]} {stats[eid]['full']}: {fmt(stats[eid]['afull'])}")

    # ---- sparse simulations
    def sim(label, combos):
        top1, top3, top5, exclc, wrongfree = (collections.Counter() for _ in range(5))
        tie1, n3, n5 = collections.Counter(), collections.Counter(), collections.Counter()
        changed3 = changed1 = 0
        gaps, ranges = [], []
        top3_np = collections.Counter()
        for inp in combos:
            live, excl = rank(inp)
            d = dict(live)
            s1 = live[0][1]
            r = {eid: 1 + sum(1 for _, s in live if s > d[eid]) for eid in d}
            t1 = [e for e in d if r[e] == 1]; t3 = {e for e in d if r[e] <= 3}; t5 = [e for e in d if r[e] <= 5]
            tie1[len(t1)] += 1; n3[len(t3)] += 1; n5[len(t5)] += 1
            for e in t1: top1[e] += 1
            for e in t3: top3[e] += 1
            for e in t5: top5[e] += 1
            for e in excl: exclc[e] += 1
            gaps.append(s1 - live[min(4, len(live) - 1)][1]); ranges.append(s1 - live[-1][1])
            live2, _ = rank(inp, use_prior=False)
            d2 = dict(live2)
            r2 = {eid: 1 + sum(1 for _, s in live2 if s > d2[eid]) for eid in d2}
            t3b = {e for e in d2 if r2[e] <= 3}
            for e in t3b: top3_np[e] += 1
            changed3 += t3 != t3b
            changed1 += {e for e in d if r[e] == 1} != {e for e in d2 if r2[e] == 1}
        n = len(combos)
        print(f"\n--- Simulasi input jarang: {label}; {n} kombinasi yang dapat diisi di UI (bobot seragam per kombinasi, bukan prevalensi)")
        table(["Entitas", "prior", "peringkat 1 (termasuk seri)", "%", "3 besar", "%", "5 besar", "%", "disingkirkan %", "3 besar tanpa prior %"],
              [(SHORT[e], PRIOR[e], top1[e], f"{top1[e] / n * 100:.0f}", top3[e], f"{top3[e] / n * 100:.0f}", top5[e], f"{top5[e] / n * 100:.0f}",
                f"{exclc[e] / n * 100:.0f}", f"{top3_np[e] / n * 100:.0f}") for e in sorted(EID, key=lambda x: (-top3[x], -top1[x]))])
        gaps.sort(); ranges.sort()
        print(f"ukuran seri di peringkat 1: {dict(sorted(tie1.items()))}; rata-rata {sum(k * v for k, v in tie1.items()) / n:.2f}")
        print(f"jumlah entitas dengan peringkat <=3: {dict(sorted(n3.items()))}; rata-rata {sum(k * v for k, v in n3.items()) / n:.2f}")
        print(f"jumlah entitas dengan peringkat <=5: {dict(sorted(n5.items()))}; rata-rata {sum(k * v for k, v in n5.items()) / n:.2f}; >10 pada {sum(v for k, v in n5.items() if k > 10)} kombinasi")
        print(f"selisih skor peringkat 1 vs entitas ke-5: median {gaps[n // 2]}, kuartil {gaps[n // 4]}-{gaps[3 * n // 4]}; rentang skor entitas hidup: median {ranges[n // 2]}")
        print(f"prior mengubah himpunan 3 besar pada {changed3} kombinasi ({changed3 / n * 100:.0f}%); mengubah peringkat 1 pada {changed1} ({changed1 / n * 100:.0f}%)")
        never = [SHORT[e] for e in EID if top5[e] == 0]
        print(f"entitas yang tidak pernah masuk 5 besar: {', '.join(never) or 'tidak ada'}")
        print(f"entitas yang tidak pernah masuk 3 besar: {', '.join(SHORT[e] for e in EID if top3[e] == 0) or 'tidak ada'}")
        return top3, n

    A, Bc, D = VALS["age_group"], VALS["bone_class"], VALS["density"]
    c1 = [{"age_group": a, "bone_class": b, "density": d} for a in A for b in Bc for d in D]
    t3a, na_ = sim("usia x tulang x densitas", c1)
    c2 = []
    for a in A:
        for b in Bc:
            for t in VALS["transverse"]:
                for d in D:
                    for lg in (VALS["longitudinal"] if b == "long_bone" else [None]):
                        inp = {"age_group": a, "bone_class": b, "transverse": t, "density": d}
                        if lg:
                            inp["longitudinal"] = lg
                        if valid(inp):
                            c2.append(inp)
    t3b, nb = sim("usia x tulang x (longitudinal bila tulang panjang) x transversal x densitas", c2)
    c3 = [c for c in c2 if c["bone_class"] == "long_bone" and c["transverse"] in ("central", "eccentric", "cortical")]
    sim("subset tulang panjang intrameduler/kortikal dari simulasi kedua", c3)
    c4 = [c for c in c3 if c["age_group"].startswith("10-19") and c["density"] == "lytic"]
    sim("subset remaja 10-19, tulang panjang, litik, intrameduler/kortikal", c4)
    c5 = [c for c in c3 if c["age_group"] in ("20-39", "40-59") and c["density"] == "lytic"]
    sim("subset dewasa 20-59, tulang panjang, litik, intrameduler/kortikal", c5)
    print(f"\nkorelasi Pearson 'maks 6 fitur inti' vs frekuensi 3 besar (simulasi kedua): "
          f"{pearson([stats[e]['core'] for e in EID], [t3b[e] for e in EID]):.2f}; jumlah +3 vs frekuensi 3 besar: "
          f"{pearson([stats[e]['p3'] for e in EID], [t3b[e] for e in EID]):.2f}; jumlah -5 vs frekuensi 3 besar: "
          f"{pearson([stats[e]['hard'] for e in EID], [t3b[e] for e in EID]):.2f}")
    # double counting cortex expansion + periosteal shell
    print("\nPenghitungan ganda temuan yang sama (cortex=expansion_shell + periosteal=shell):")
    table(["Entitas", "expansion_shell", "periosteal shell", "jumlah"],
          [(SHORT[e], w(e, "cortex", "expansion_shell"), w(e, "periosteal", "shell"), w0(e, "cortex", "expansion_shell") + w0(e, "periosteal", "shell"))
           for e in EID if w(e, "periosteal", "shell") is not None])
    return stats


def part3():
    h("3. KLAIM HILANG, TIDAK TERJANGKAU, DAN MENCURIGAKAN")
    rows = []
    for f in FO:
        for v in VALS[f]:
            ws = [w(e, f, v) for e in EID]
            rows.append((f"{f}:{v}", sum(1 for x in ws if x is not None), sum(1 for x in ws if x is None),
                         sum(1 for x in ws if x is not None and x >= 2), sum(1 for x in ws if x == 1), sum(1 for x in ws if x == 0),
                         sum(1 for x in ws if x == -2), sum(1 for x in ws if x is not None and x <= HARD)))
    table(["Fitur:nilai", "klaim ada", "tanpa klaim", ">=+2", "+1", "0", "-2", "-5"], rows)
    print("Nilai yang hanya menaikkan (ada klaim positif, tidak ada satu pun klaim negatif):")
    print("  " + "; ".join(f"{r[0]} (+:{r[3] + r[4]}, tanpa klaim:{r[2]})" for r in rows if r[3] + r[4] > 0 and r[6] + r[7] == 0))
    print("Fitur menurut rata-rata cakupan klaim per nilai:")
    for f in FO:
        n = [sum(1 for e in EID if w(e, f, v) is not None) for v in VALS[f]]
        print(f"  {f}: rata-rata {sum(n) / len(n):.1f} dari 37 entitas per nilai (min {min(n)}, maks {max(n)})")
    print("\nKlaim yang diharapkan peninjau (arah) vs isi KB:")
    table(["Entitas", "Fitur:nilai", "Diharapkan", "Di KB", "Alasan"],
          [(SHORT[e], f"{f}:{v}", exp, "tanpa klaim" if w(e, f, v) is None else w(e, f, v), why) for e, f, v, exp, why in EXPECTED])
    # bone_class gaps
    print("Entitas dengan >=1 bone_class -5: kelas tulang yang tidak punya klaim (himpunan eksklusi tidak lengkap):")
    for eid in EID:
        hard = [v for v in VALS["bone_class"] if (w(eid, "bone_class", v) or 0) <= HARD]
        if hard:
            miss = [v for v in VALS["bone_class"] if w(eid, "bone_class", v) is None]
            print(f"  {SHORT[eid]}: -5 pada {hard}; tanpa klaim pada {miss}")
    print("Kelas tulang batch-3: jumlah entitas dengan klaim / positif / -5")
    for v in VALS["bone_class"]:
        print(f"  {v}: klaim {sum(1 for e in EID if w(e, 'bone_class', v) is not None)}, positif {sum(1 for e in EID if (w(e, 'bone_class', v) or 0) > 0)}, "
              f"-5 {sum(1 for e in EID if (w(e, 'bone_class', v) or 0) <= HARD)}")
    for v in ("clavicle", "calcaneus", "patella", "craniofacial", "small_tubular_hand_foot"):
        live, excl = rank({"bone_class": v, "density": "lytic", "age_group": "20-39"})
        print(f"  contoh 20-39 + {v} + lytic -> 5 teratas: " + ", ".join(f"{SHORT[e]} {s}" for e, s in live[:5]) + f" | disingkirkan {len(excl)}")
    # unreachable / wasted
    print("\nKlaim yang tidak terjangkau atau terbuang:")
    dead = []
    for eid in EID:
        for f, d in ENT[eid]["feature_weights"].items():
            for v, c in d.items():
                if v == "not_applicable":
                    dead.append((SHORT[eid], f"{f}:{v}", c["weight"], "nilai disembunyikan di UI"))
                elif c["weight"] > HARD:
                    t, _ = best(ent_gain(eid), ent_rules(eid), fixed={f: v})
                    if t is None:
                        dead.append((SHORT[eid], f"{f}:{v}", c["weight"], "hanya dapat diisi bersama nilai induk yang -5 bagi entitas ini"))
    table(["Entitas", "Klaim", "Bobot", "Sebab"], dead)
    print("Klaim margin_lodwick pada entitas yang densitas terbaiknya sclerotic (margin tidak dapat diisi pada presentasi khasnya):")
    for eid in EID:
        ds = {d: w0(eid, "density", d) for d in VALS["density"]}
        mg = {v: w(eid, "margin_lodwick", v) for v in VALS["margin_lodwick"] if w(eid, "margin_lodwick", v) is not None}
        if mg and ds["sclerotic"] > max(ds["lytic"], ds["mixed"]):
            print(f"  {SHORT[eid]}: density {ds}; margin {mg}")
    print("Entitas permukaan (central & eccentric -5) yang masih punya klaim margin atau endosteal_scalloping:")
    for eid in EID:
        if (w(eid, "transverse", "central") or 0) <= HARD and (w(eid, "transverse", "eccentric") or 0) <= HARD:
            mg = {v: w(eid, "margin_lodwick", v) for v in VALS["margin_lodwick"] if w(eid, "margin_lodwick", v) is not None}
            print(f"  {SHORT[eid]}: margin {mg or '-'}; endosteal_scalloping {w(eid, 'cortex', 'endosteal_scalloping')}; cortical {w(eid, 'transverse', 'cortical')}")
    print("Klaim longitudinal pada entitas dengan long_bone <= -2:")
    for eid in EID:
        if (w(eid, "bone_class", "long_bone") or 0) <= -2:
            print(f"  {SHORT[eid]}: long_bone {w(eid, 'bone_class', 'long_bone')}; longitudinal {ENT[eid]['feature_weights'].get('longitudinal', {}).keys() and {k: c['weight'] for k, c in ENT[eid]['feature_weights'].get('longitudinal', {}).items()}}")
    # suspicious direction: listed for the report with current values
    print("\nNilai yang dirujuk di bagian 3(c)/(d) laporan (isi KB saat ini):")
    look = [("aneurysmal_bone_cyst", "transverse", "central"), ("aneurysmal_bone_cyst", "transverse", "eccentric"),
            ("osteosarcoma_conventional", "periosteal", "solid_thin"), ("ewing_sarcoma", "periosteal", "solid_thin"),
            ("osteosarcoma_conventional", "matrix", "none"), ("osteosarcoma_conventional", "matrix", "chondroid"),
            ("osteosarcoma_conventional", "age_group", "60+"), ("osteosarcoma_conventional", "age_group", "40-59"),
            ("osteosarcoma_conventional", "transverse", "central"), ("osteosarcoma_conventional", "transverse", "eccentric"),
            ("giant_cell_tumour_of_bone", "bone_class", "long_bone"), ("giant_cell_tumour_of_bone", "age_group", "10-19_unknown"),
            ("chondromyxoid_fibroma", "age_group", "10-19_open"), ("chondromyxoid_fibroma", "transverse", "eccentric"),
            ("chondromyxoid_fibroma", "longitudinal", "metadiaphysis"), ("chondromyxoid_fibroma", "margin_lodwick", "IA"),
            ("chondromyxoid_fibroma", "density", "lytic"), ("chondromyxoid_fibroma", "bone_class", "long_bone"),
            ("skeletal_tuberculosis", "periosteal", "none"), ("skeletal_tuberculosis", "bone_class", "spine_body"),
            ("osteomyelitis", "bone_class", "spine_body"), ("osteomyelitis", "margin_lodwick", "IA"), ("osteomyelitis", "margin_lodwick", "IB"),
            ("stress_fracture", "bone_class", "long_bone"), ("stress_fracture", "transverse", "cortical"), ("stress_fracture", "periosteal", "solid_thin"),
            ("osteoid_osteoma", "transverse", "cortical"), ("osteoid_osteoma", "periosteal", "solid_thin"), ("osteoid_osteoma", "density", "sclerotic"),
            ("enostosis", "matrix", "osteoid"), ("enostosis", "clinical_flags", "known_primary_malignancy"),
            ("bone_metastasis", "density", "sclerotic"), ("bone_metastasis", "multiplicity", "solitary"),
            ("plasmacytoma_myeloma", "density", "sclerotic"), ("plasmacytoma_myeloma", "cortex", "endosteal_scalloping"),
            ("chordoma", "transverse", "central"), ("vertebral_haemangioma", "soft_tissue_mass", "present"),
            ("vertebral_haemangioma", "cortex", "expansion_shell"), ("paget_disease", "cortex", "expansion_shell"),
            ("langerhans_cell_histiocytosis", "bone_class", "spine_body"), ("non_ossifying_fibroma", "periosteal", "present_unspecified"),
            ("simple_bone_cyst", "periosteal", "present_unspecified"), ("simple_bone_cyst", "cortex", "focal_breach"),
            ("fibrous_dysplasia", "cortex", "focal_breach"), ("chondroblastoma", "periosteal", "lamellated"),
            ("primary_bone_lymphoma", "age_group", "10-19_unknown"), ("primary_bone_lymphoma", "cortex", "intact"),
            ("ewing_sarcoma", "soft_tissue_mass", "present"), ("ewing_sarcoma", "cortex", "intact"),
            ("intraosseous_lipoma", "matrix", "osteoid"), ("bone_infarct", "matrix", "chondroid"), ("bone_infarct", "cortex", "endosteal_scalloping"),
            ("enchondroma", "cortex", "endosteal_scalloping"), ("chondrosarcoma_central", "cortex", "intact"),
            ("chondrosarcoma_central", "soft_tissue_mass", "absent"), ("enchondroma", "size_cm", ">5"), ("chondrosarcoma_central", "size_cm", ">5"),
            ("osteoblastoma", "bone_class", "long_bone"), ("osteoblastoma", "size_cm", "<2"), ("osteoid_osteoma", "size_cm", "2-5")]
    print("  " + "; ".join(f"{SHORT[e]} {f}:{v}={'tanpa klaim' if w(e, f, v) is None else w(e, f, v)}" for e, f, v in look))
    # multiplicity & flags
    for f in ("multiplicity", "clinical_flags", "size_cm", "soft_tissue_mass"):
        for v in VALS[f]:
            print(f"  {f}:{v} -> " + ", ".join(f"{SHORT[e]} {w(e, f, v)}" for e in EID if w(e, f, v) is not None))


def part4(stats):
    h("4. PASANGAN MIMIC")
    # all-pair profile distances
    cols = [(f, v) for f in FO for v in VALS[f]]
    pairs = []
    for a, b in itertools.combinations(EID, 2):
        l1 = sum(abs(w0(a, f, v) - w0(b, f, v)) for f, v in cols)
        disc = sum(1 for f, v in cols if abs(w0(a, f, v) - w0(b, f, v)) >= 2)
        hardsep = sum(1 for f, v in cols if (w0(a, f, v) <= HARD) != (w0(b, f, v) <= HARD))
        sab, sba = separation(a, b), separation(b, a)
        pairs.append((a, b, l1, disc, hardsep, sab, sba))
    print("Jarak profil semua pasangan (666): L1 atas 62 nilai (tanpa klaim = 0); diskriminator = nilai dengan selisih >= 2;")
    print("pemisah keras = nilai yang -5 hanya pada salah satu; sep(A>B) = selisih skor maksimum yang dapat dicapai A atas B tanpa menyingkirkan keduanya.")
    xs = sorted(p[2] for p in pairs)
    print(f"L1: min {xs[0]}, median {xs[len(xs) // 2]}, maks {xs[-1]}")
    print("25 pasangan terdekat menurut L1:")
    table(["A", "B", "L1", "diskriminator", "pemisah keras", "sep(A>B)", "sep(B>A)"],
          [(SHORT[a], SHORT[b], l1, d, hs, sab, sba) for a, b, l1, d, hs, sab, sba in sorted(pairs, key=lambda p: p[2])[:25]])
    mx = sorted(pairs, key=lambda p: max(p[5], p[6]))
    print(f"max(sep(A>B), sep(B>A)) terkecil di antara semua pasangan: {max(mx[0][5], mx[0][6])} ({SHORT[mx[0][0]]} vs {SHORT[mx[0][1]]}); "
          f"jumlah pasangan dengan max(sep) <= 12: {sum(1 for p in pairs if max(p[5], p[6]) <= 12)}")
    table(["A", "B", "L1", "sep(A>B)", "sep(B>A)", "pemisah keras"], [(SHORT[a], SHORT[b], l1, sab, sba, hs) for a, b, l1, d, hs, sab, sba in mx[:12]])
    one = sorted(pairs, key=lambda p: min(p[5], p[6]))
    print("Asimetri: entitas yang paling sering 'tidak dapat unggul > 8 poin' atas pasangannya (jumlah pasangan dengan sep <= 8 sebagai pihak yang lemah):")
    weak = collections.Counter()
    for a, b, l1, d, hs, sab, sba in pairs:
        if sab <= 8: weak[a] += 1
        if sba <= 8: weak[b] += 1
    print("  " + ", ".join(f"{SHORT[k]} {v}" for k, v in weak.most_common()))
    strong = collections.Counter()
    for a, b, l1, d, hs, sab, sba in pairs:
        if sab <= 8: strong[b] += 1
        if sba <= 8: strong[a] += 1
    print("  pihak yang sulit dikalahkan: " + ", ".join(f"{SHORT[k]} {v}" for k, v in strong.most_common()))
    P = {(a, b): (l1, d, hs, sab, sba) for a, b, l1, d, hs, sab, sba in pairs}
    P.update({(b, a): (l1, d, hs, sba, sab) for a, b, l1, d, hs, sab, sba in pairs})
    RADIO = [f for f in FO if f != "clinical_flags"]
    for name, group, ctx in MIMIC_GROUPS:
        print(f"\n--- Kelompok: {name} | konteks {ctx}")
        rows = []
        for a, b in itertools.combinations(group, 2):
            l1, d, hs, sab, sba = P[(a, b)]
            rows.append((SHORT[a], SHORT[b], l1, d, hs, sab, sba, separation(a, b, ctx, RADIO), separation(b, a, ctx, RADIO)))
        table(["A", "B", "L1", "diskriminator", "pemisah keras", "sep(A>B)", "sep(B>A)", "sep_ctx(A>B)", "sep_ctx(B>A)"], rows)
        for a, b in itertools.combinations(group, 2):
            ds = [(f, v, w(a, f, v), w(b, f, v)) for f, v in cols if abs(w0(a, f, v) - w0(b, f, v)) >= 2]
            print(f"  {SHORT[a]} vs {SHORT[b]}: " + "; ".join(f"{f}:{v} {'.' if x is None else x}/{'.' if y is None else y}" for f, v, x, y in ds))
    return P


def part4b():
    h("4b. VINYET BUATAN PENINJAU (bukan kasus validasi)")
    rows, res = [], {}
    for vid, exp, desc, s in VIGNETTES:
        inp = parse(s)
        if not valid(inp):
            raise SystemExit(f"vignette {vid} is not reachable in the UI")
        live, excl = rank(inp)
        r = comp_rank(live, exp)
        d = dict(live)
        ties = sum(1 for _, sc in live if exp in d and sc == d[exp])
        top = "; ".join(f"{SHORT[e]} {sc}" for e, sc in live[:4])
        gap = (d[exp] - max(sc for e, sc in live if e != exp)) if exp in d else None
        rows.append((vid, SHORT[exp], len(inp), "disingkirkan: " + str(excl[exp][1]) if exp in excl else r, ties if exp in d else "-", gap, top, len(excl), desc))
        res[vid] = (exp, inp, live, excl, r)
    table(["ID", "Entitas diharapkan", "fitur", "peringkat", "seri", "selisih vs pesaing terbaik", "4 teratas", "disingkirkan", "Deskripsi"], rows)
    ranks = [r[3] for r in rows if isinstance(r[3], int)]
    print(f"vinyet: {len(rows)}; peringkat 1 (termasuk seri): {sum(1 for r in ranks if r == 1)}; peringkat 1 tunggal: "
          f"{sum(1 for r in rows if r[3] == 1 and r[4] == 1)}; 3 besar: {sum(1 for r in ranks if r <= 3)}; di luar 3 besar: {sum(1 for r in ranks if r > 3)}; "
          f"rujukan tersingkir: {sum(1 for r in rows if not isinstance(r[3], int))}")
    ents_first = collections.defaultdict(list)
    for vid, (exp, inp, live, excl, r) in res.items():
        ents_first[exp].append(r)
    print("entitas tanpa vinyet:", [e for e in EID if e not in ents_first] or "tidak ada")
    print("entitas yang vinyet tipikalnya tidak peringkat 1:", "; ".join(f"{SHORT[e]} {rs}" for e, rs in ents_first.items() if any(x != 1 for x in rs)) or "tidak ada")
    # mimic pair check on vignettes
    print("\nUji mimic pada vinyet: skor entitas diharapkan (A) vs anggota kelompok mimic-nya (B) pada kasus tipikal A")
    out = []
    for vid, (exp, inp, live, excl, r) in res.items():
        d = dict(live)
        for name, group, _ctx in MIMIC_GROUPS:
            if exp in group:
                for b in group:
                    if b == exp:
                        continue
                    sb = d.get(b)
                    out.append((vid, SHORT[exp], d.get(exp), SHORT[b], "disingkirkan" if sb is None else sb,
                                "ya" if (sb is None or d.get(exp, -99) > sb) else ("SERI" if d.get(exp) == sb else "TIDAK")))
    table(["Vinyet", "A", "skor A", "B", "skor B", "A di atas B?"], out)
    bad = [o for o in out if o[5] != "ya"]
    print(f"perbandingan: {len(out)}; A tidak di atas B: {len(bad)} -> " + "; ".join(f"{o[0]} {o[1]} vs {o[3]} ({o[2]} vs {o[4]})" for o in bad))
    # which entity wins vignettes wrongly
    wrong = collections.Counter()
    for vid, (exp, inp, live, excl, r) in res.items():
        if r != 1:
            for e, sc in live:
                if sc == live[0][1]:
                    wrong[e] += 1
    print("entitas yang menang pada vinyet entitas lain:", dict((SHORT[k], v) for k, v in wrong.most_common()))
    return res


# Source spot-check (reviewer's reading of the cited open-access sources, 2026-11-21). Verdicts:
# S = supported, P = partly (direction yes, strength no), N = not found in the cited source(s),
# X = cited source says otherwise. "how": FT = full text read via PubMed/PMC tool; WF = publisher page via WebFetch
# (answers produced by a small model from the page; less reliable than FT).
SPOT = [
    ("giant_cell_tumour_of_bone", "age_group", "10-19_open", "P", "S-01 FT; S-16 WF", "S-01: GCT 'biasanya' meluas ke subkondral setelah fisis menutup; S-16 tidak membahas pasien imatur. Arah didukung, 'hampir mustahil' tidak"),
    ("giant_cell_tumour_of_bone", "transverse", "eccentric", "S", "S-01 FT", "S-01 mencantumkan GCT sebagai lesi eksentrik"),
    ("giant_cell_tumour_of_bone", "margin_lodwick", "IB", "S", "S-01 FT", "S-01: IB contohnya GCT"),
    ("chordoma", "bone_class", "long_bone", "N", "S-01 FT", "S-01 (skeleton apendikular) tidak memuat lokasi atau gambaran kordoma"),
    ("chordoma", "bone_class", "sacrum", "N", "S-01 FT", "sda.; seluruh klaim kordoma hanya mengutip S-01"),
    ("ewing_sarcoma", "margin_lodwick", "IA", "P", "S-01 FT", "S-01 menempatkan Ewing pada tipe II/III; tidak menyatakan IA mustahil"),
    ("ewing_sarcoma", "age_group", "60+", "N", "S-01 FT; S-04 WF", "S-01: Ewing lebih sering <15 th; S-04 hanya pasien 3-18 th. Tidak ada pernyataan tentang lansia"),
    ("ewing_sarcoma", "longitudinal", "diaphysis", "P", "S-01 FT; S-04 WF", "S-01 mendukung diafisis; seri S-04 (n=28) mencatat metafisis 36% > diafisis 21%"),
    ("osteosarcoma_conventional", "margin_lodwick", "IA", "P", "S-01 FT; S-15 WF", "Keduanya menyebut tepi tidak tegas/zona transisi lebar; tidak ada pernyataan bahwa tepi sklerotik mustahil"),
    ("osteosarcoma_conventional", "periosteal", "codman", "S", "S-01 FT", "S-01: Codman klasik untuk osteosarkoma"),
    ("osteosarcoma_conventional", "periosteal", "solid_thin", "X", "S-01 FT", "S-01: reaksi periosteal tipis dapat dijumpai pada Ewing dan osteosarkoma; KB memberi -2"),
    ("osteosarcoma_conventional", "age_group", "60+", "X", "S-15 WF", "S-15 menyatakan data baru meragukan puncak kedua usia lanjut; KB memberi 60+ (+1) > 40-59 (0)"),
    ("osteosarcoma_telangiectatic", "margin_lodwick", "IA", "X", "S-15 WF", "S-15: kadang berbatas tegas dengan tepi sklerotik ireguler; KB memberi -5"),
    ("osteosarcoma_telangiectatic", "density", "lytic", "S", "S-15 WF", "S-15: osteolisis luas, ekspansil"),
    ("osteosarcoma_parosteal", "transverse", "juxtacortical_continuous", "S", "S-15 WF", "S-15: tidak ada kontinuitas korteks-meduler (invasi meduler 22-58% adalah hal lain)"),
    ("osteosarcoma_parosteal", "density", "sclerotic", "S", "S-15 WF", "S-15: osifikasi padat sentral"),
    ("osteosarcoma_periosteal", "cortex", "saucerization", "N", "S-01 FT; S-15 WF", "Saucerization tidak disebut di kedua sumber"),
    ("osteosarcoma_periosteal", "longitudinal", "diaphysis", "S", "S-15 WF; S-25 WF", "Diafisis/metadiafisis"),
    ("aneurysmal_bone_cyst", "transverse", "eccentric", "X", "S-01 FT; S-06 WF", "S-01 mencantumkan ABC sebagai lesi SENTRAL; S-06 tidak menyebut eksentrik/sentral. Ajaran umum memang eksentrik, tetapi sumber yang dikutip tidak mendukung +3"),
    ("aneurysmal_bone_cyst", "periosteal", "shell", "S", "S-01 FT", "S-01: pola shell pada GCT dan ABC"),
    ("chondroblastoma", "soft_tissue_mass", "present", "X", "S-06 WF", "S-06 menyebut CT dapat menunjukkan perluasan ke jaringan lunak; KB memberi -5"),
    ("chondroblastoma", "age_group", "40-59", "N", "S-01 FT; S-06 WF", "Keduanya menyebut usia remaja/imatur; tidak ada pernyataan tentang dewasa"),
    ("chondroblastoma", "periosteal", "lamellated", "S", "S-01 FT", "S-01: periostitis berlapis pada sarkoma, osteomielitis, dan kondroblastoma"),
    ("chondromyxoid_fibroma", "margin_lodwick", "IA", "P", "S-01 FT; S-06 WF", "S-01: CMF 'dapat' tampak IA (satu dari 8 lesi). S-06 TIDAK membahas CMF sama sekali, padahal semua klaim CMF mengutip S-01,S-06"),
    ("chondromyxoid_fibroma", "longitudinal", "metadiaphysis", "S", "S-01 FT", "S-01: CMF dan NOF dekat perbatasan metadiafisis"),
    ("simple_bone_cyst", "age_group", "60+", "N", "S-01 FT; S-06 WF", "S-06: 80% pada remaja/usia 20-an; tidak ada pernyataan tentang lansia"),
    ("simple_bone_cyst", "bone_class", "calcaneus", "S", "S-01 FT; S-04 WF", "S-01: banding lesi lusen kalkaneus; S-04: 25% kista simpel di kalkaneus"),
    ("osteoid_osteoma", "age_group", "60+", "P", "S-06 WF", "S-06: dapat timbul pada usia berapa pun, khas dekade kedua"),
    ("osteoid_osteoma", "periosteal", "solid_thin", "S", "S-01 FT", "S-01: reaksi solid khas osteoid osteoma"),
    ("bpop_nora_lesion", "density", "lytic", "P", "S-25 WF", "S-25: terkalsifikasi/terosifikasi bervariasi; lesi lusen tidak dibahas"),
    ("bpop_nora_lesion", "transverse", "juxtacortical_continuous", "S", "S-25 WF", "S-25: ketiadaan kontinuitas meduler adalah pembeda kunci dari osteokondroma"),
    ("periosteal_chondroma", "cortex", "saucerization", "S", "S-25 WF", "S-25: permukaan korteks scalloped dengan/tanpa sklerosis"),
    ("fibrous_dysplasia", "margin_lodwick", "IC", "X", "S-22 WF", "S-22: lesi kraniofasial biasanya TIDAK berbatas tegas; KB memberi craniofacial +3 dan IC -5"),
    ("fibrous_dysplasia", "periosteal", "lamellated", "P", "S-22 WF", "S-22: reaksi periosteal tidak ada kecuali pada fraktur patologis, dan fraktur sering; pola tidak dirinci"),
    ("fibrous_dysplasia", "matrix", "ground_glass", "S", "S-01 FT; S-22 WF", "Ground-glass khas"),
    ("langerhans_cell_histiocytosis", "matrix", "osteoid", "P", "S-23 WF", "S-23 menggambarkan button sequestrum dan fragmen tulang intralesi; bukan matriks, tetapi dapat dikodekan demikian"),
    ("langerhans_cell_histiocytosis", "age_group", "60+", "N", "S-23 WF", "S-23 tidak membahas lansia"),
    ("vertebral_haemangioma", "matrix", "coarse_trabeculae", "P", "S-01 FT; S-19 WF", "S-19 hanya menggambarkan hemangioma KALVARIA (trabekula menebal); gambaran vertebra tidak diuraikan di kedua sumber"),
    ("skeletal_tuberculosis", "periosteal", "spiculated", "N", "S-01 FT", "S-01 hanya menyebut TB sebagai kategori infeksi; tidak ada gambaran radiografik. Seluruh klaim TB hanya mengutip S-01"),
    ("skeletal_tuberculosis", "bone_class", "spine_body", "N", "S-01 FT", "sda."),
    ("osteomyelitis", "margin_lodwick", "IA", "S", "S-01 FT", "S-01: abses Brodie termasuk lesi tipe IA"),
    ("osteomyelitis", "matrix", "osteoid", "N", "S-01 FT", "S-01 tidak menyatakan apa pun tentang mineralisasi pada osteomielitis"),
    ("bone_infarct", "margin_lodwick", "IC", "N", "S-01 FT", "S-01 hanya menyebut infark dini campuran dan infark lanjut sklerotik serpiginosa"),
    ("intraosseous_ganglion_geode", "size_cm", ">5", "N", "S-01 FT", "S-01 tidak memuat ukuran geode"),
    ("intraosseous_lipoma", "margin_lodwick", "IA", "S", "S-01 FT", "S-01: lipoma intraoseus termasuk lesi tipe IA"),
    ("bone_metastasis", "multiplicity", "multiple", "S", "S-01 FT", "S-01: poliostotik pada >90%"),
    ("enostosis", "size_cm", "<2", "S", "S-01 FT", "S-01: sebagian besar 1 mm-2 cm; pulau tulang raksasa >2 cm dilaporkan"),
    ("paget_disease", "longitudinal", "epiphysis_apophysis", "S", "S-01 FT", "S-01: Paget dan clear cell CS masuk banding epifisis usia >40"),
    ("non_ossifying_fibroma", "margin_lodwick", "IA", "S", "S-01 FT", "S-01: contoh klasik tipe IA"),
    ("osteochondroma", "transverse", "juxtacortical_continuous", "S", "S-01 FT; S-06 WF", "Kontinuitas korteks-meduler patognomonik"),
]


def part5():
    h("5. UJI PETIK SUMBER")
    lab = {"S": "didukung", "P": "sebagian (arah ya, kekuatan tidak)", "N": "tidak ditemukan di sumber yang dikutip", "X": "sumber yang dikutip menyatakan lain"}
    rows = []
    for e, f, v, verdict, how, note in SPOT:
        c = ENT[e]["feature_weights"][f][v]
        rows.append((SHORT[e], f"{f}:{v}", c["weight"], ",".join(c["source_ids"]), lab[verdict], how, note))
    table(["Entitas", "Klaim", "Bobot", "Sumber dikutip", "Hasil", "Cara baca", "Catatan"], rows)
    cc = collections.Counter(r[4] for r in rows)
    print(f"klaim diperiksa: {len(rows)}; " + "; ".join(f"{k}: {v}" for k, v in cc.most_common()))
    for grp, test in (("hard constraint (-5)", lambda x: x <= HARD), ("+3", lambda x: x == 3), ("lainnya", lambda x: HARD < x < 3)):
        sub = [r for r in rows if test(r[2])]
        print(f"  {grp}: n={len(sub)}; " + "; ".join(f"{k}: {v}" for k, v in collections.Counter(r[4] for r in sub).most_common()))


def part_cases(cases, src):
    h("6. KASUS UJI v1-v4 PADA KB INI (pemeriksaan transkripsi + over-calling)")
    if not cases:
        print("kasus uji tidak tersedia secara lokal")
        return
    print("sumber kasus:", src, "| jumlah:", len(cases))
    mism = []
    wrong1 = collections.Counter()
    per = collections.defaultdict(lambda: [0, 0, 0, 0, 0])
    for cid, truth, typ, rk, sc, feats in cases:
        live, excl = rank(feats)
        s, hard = score(truth, feats)
        pos = next((i + 1 for i, (e, _) in enumerate(live) if e == truth), 0)
        if s != sc or pos != rk:
            mism.append((cid, f"tersimpan peringkat {rk} skor {sc}", f"dihitung peringkat {pos} skor {s}"))
        vs = cid.split("-")[0]
        cr = comp_rank(live, truth)
        per[vs][0] += 1
        per[vs][1] += pos == 1; per[vs][2] += 1 <= pos <= 3
        per[vs][3] += cr is not None and cr <= 3; per[vs][4] += bool(hard)
        if pos != 1:
            wrong1[live[0][0]] += 1
    print("ketidakcocokan dengan hasil tersimpan (peringkat urut-abjad dan skor rujukan):", mism or "tidak ada")
    # how the small-round-cell rule fires
    fired = collections.Counter()
    for cid, truth, typ, rk, sc, feats in cases:
        if feats.get("soft_tissue_mass") == "present" and feats.get("cortex") in ("intact", "focal_breach"):
            live, _ = rank(feats)
            fired[(feats["cortex"], "rujukan Ewing/limfoma" if truth in ("ewing_sarcoma", "primary_bone_lymphoma") else "rujukan lain",
                   "Ewing/limfoma peringkat 1" if live[0][0] in ("ewing_sarcoma", "primary_bone_lymphoma") else "lainnya peringkat 1")] += 1
    print("aturan 'massa jaringan lunak tanpa destruksi' (Ewing, limfoma) pada kasus v1-v4:")
    for k, v in sorted(fired.items()):
        print(f"  cortex={k[0]}; {k[1]}; {k[2]}: {v} kasus")
    table(["Set", "n", "Top-1 (urut abjad)", "Top-3 (urut abjad)", "Top-3 sadar-seri", "rujukan tersingkir"], [(k, *v) for k, v in sorted(per.items())])
    table(["Entitas di peringkat 1 saat rujukan bukan peringkat 1 (v1-v4)", "kali"], [(SHORT[k], v) for k, v in wrong1.most_common(12)])
    nfeat = [len(c[5]) for c in cases]
    print(f"fitur terisi per kasus: rata-rata {sum(nfeat) / len(nfeat):.1f}")
    fill = collections.Counter(f for c in cases for f in c[5])
    print("frekuensi pengisian fitur (jumlah kasus dari %d): " % len(cases) + ", ".join(f"{f} {fill[f]}" for f in FO))


def main():
    cases, src = load_cases()
    print("TumTul - tinjauan skor KB (keluaran tools/review_scoring.py); KB dibaca dari", "data/")
    part0()
    part1(cases)
    stats = part2()
    part3()
    part4(stats)
    part4b()
    part5()
    part_cases(cases, src)


if __name__ == "__main__":
    main()
