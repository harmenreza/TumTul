#!/usr/bin/env python3
"""Tinjauan sumber KB TumTul v0.6 atas TEKS LENGKAP (baca-saja terhadap data/ dan schema/).

Masukan:
  data/entities/*.json, data/features.json, data/sources.json   (KB)
  docs/tinjauan-skor-v0.6-hard-constraints.csv                   (kelas a/b/c dari tinjauan pertama)
  tools/review_scoring.py                                        (hanya daftar SPOT uji petik lama, dibaca sebagai teks)
  tools/review_source_evidence.tsv                               (temuan per klaim per sumber, dicatat tangan)
  tools/review_source_coverage.tsv                               (cakupan entitas x sumber, dicatat tangan)

Keluaran:
  docs/tinjauan-sumber-v0.6.csv   (satu baris per klaim per set)
  stdout                          (semua tabel ringkasan yang dipakai laporan; disimpan sebagai
                                   docs/tinjauan-sumber-v0.6-keluaran.txt)

Pemakaian:
  python3 tools/review_sources.py              # periksa, gabungkan, tulis CSV, cetak tabel
  python3 tools/review_sources.py --worklist S-06   # daftar klaim set A-D/R yang mengutip S-06 dan belum dicatat

Set: A = hard constraint (-5) kelas b/c pada tinjauan pertama; B = semua +3; C = 18 butir uji petik lama yang
"tidak ditemukan"/"bertentangan"; D = 40 klaim acak (benih tetap) dari sisa KB; R = 5 aturan (rules[]), dilaporkan terpisah.
Vonis per klaim: temuan terbaik di antara sumber yang dikutip menentukan (supports > partly > silent); konflik selalu
dilaporkan, dan menjadi vonis "bertentangan" hanya bila tidak ada sumber yang mendukung atau mendukung sebagian.
Penanda di awal catatan: [daftar] = hanya keanggotaan daftar pada nilai yang diklaim; [daftar-lain] = entitas hanya
tercantum pada nilai lain; [umum] = pernyataan tingkat kelompok (tumor jinak, osteosarkoma umum), bukan entitasnya.

Hanya pustaka standar.
"""
import ast
import collections
import csv
import json
import pathlib
import random
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
FEAT = json.loads((ROOT / "data/features.json").read_text(encoding="utf-8"))["features"]
ENTS = [json.loads(p.read_text(encoding="utf-8")) for p in sorted((ROOT / "data/entities").glob("*.json"))]
SRC = {s["id"]: s for s in json.loads((ROOT / "data/sources.json").read_text(encoding="utf-8"))["sources"]}
ENT = {e["id"]: e for e in ENTS}
HARD = -5
SEED = 20261121           # benih tetap untuk set D
N_D = 40
UNREACHABLE = {"S-21"}                  # tidak ada salinan yang dapat dibaca pada tinjauan ini (S-18: PDF dari pemilik)
EVID = ROOT / "tools/review_source_evidence.tsv"
COVER = ROOT / "tools/review_source_coverage.tsv"
OUT = ROOT / "docs/tinjauan-sumber-v0.6.csv"
FINDINGS = ("supports", "partly", "silent", "conflicts")
RANK = {"supports": 3, "partly": 2, "silent": 1}
COVER_LEVELS = {"1": "gambaran radiografik", "2": "hanya usia/lokasi", "3": "hanya disebut sekilas", "4": "tidak ada"}
DEPTHS = ("uraian", "daftar", "-")

# ---------------------------------------------------------------- klaim
Claim = collections.namedtuple("Claim", "entity feature value weight sources")
CLAIMS = {}
for e in ENTS:
    for f, vals in e["feature_weights"].items():
        for v, c in vals.items():
            CLAIMS[(e["id"], f, v)] = Claim(e["id"], f, v, c["weight"], tuple(c["source_ids"]))
N_FEATURE_CLAIMS = len(CLAIMS)
# aturan (rules[]) ikut diperiksa sebagai set R tersendiri; kuncinya (entitas, "rule", id aturan)
for e in ENTS:
    for r in e.get("rules", []):
        CLAIMS[(e["id"], "rule", r["id"])] = Claim(e["id"], "rule", r["id"], r["weight"], tuple(r["source_ids"]))


def load_sets():
    """A = hard constraint kelas b/c; B = +3; C = 18 butir uji petik lama (N/X); D = sampel acak dari sisanya."""
    hc = list(csv.DictReader((ROOT / "docs/tinjauan-skor-v0.6-hard-constraints.csv").open(encoding="utf-8")))
    hc_class = {(r["entity"], r["feature"], r["value"]): r["class"] for r in hc}
    for k in hc_class:
        assert k in CLAIMS and CLAIMS[k].weight == HARD, f"CSV hard constraint tidak cocok dengan KB: {k}"
    set_a = sorted(k for k, c in hc_class.items() if c in ("b", "c"))
    set_b = sorted(k for k, c in CLAIMS.items() if c.weight == 3 and k[1] != "rule")
    # daftar SPOT dibaca dari teks skrip tinjauan pertama (tanpa menjalankannya)
    text = (ROOT / "tools/review_scoring.py").read_text(encoding="utf-8")
    m = re.search(r"^SPOT = (\[.*?^\])", text, re.S | re.M)
    spot = ast.literal_eval(m.group(1))
    lab = {"S": "didukung", "P": "sebagian", "N": "tidak ditemukan", "X": "bertentangan"}
    earlier = {(e, f, v): lab[verdict] for e, f, v, verdict, how, note in spot}
    earlier_how = {(e, f, v): how for e, f, v, verdict, how, note in spot}
    for k in earlier:
        assert k in CLAIMS, f"butir SPOT tidak ada di KB: {k}"
    set_c = sorted(k for k, v in earlier.items() if v in ("tidak ditemukan", "bertentangan"))
    used = set(set_a) | set(set_b) | set(set_c)
    frame = sorted(k for k in CLAIMS if k not in used and k[2] != "not_applicable" and k[1] != "rule")
    rng = random.Random(SEED)
    set_d = sorted(rng.sample(frame, N_D))
    set_r = sorted(k for k in CLAIMS if k[1] == "rule")
    return {"A": set_a, "B": set_b, "C": set_c, "D": set_d, "R": set_r}, hc_class, earlier, earlier_how, len(frame)


SETS, HC_CLASS, EARLIER, EARLIER_HOW, FRAME_D = load_sets()
NEEDED = sorted(set().union(*(SETS[s] for s in "ABCD")))      # gabungan A-D (tanpa aturan)
ALLCHK = sorted(set(NEEDED) | set(SETS["R"]))                 # semua yang harus punya temuan


# ---------------------------------------------------------------- bukti
def load_evidence():
    ev = collections.defaultdict(dict)
    errors = []
    if not EVID.exists():
        return ev, ["berkas bukti belum ada"]
    with EVID.open(encoding="utf-8", newline="") as fh:
        rd = csv.DictReader(fh, delimiter="\t")
        want = ["entity", "feature", "value", "weight", "source", "finding", "locator", "note"]
        if rd.fieldnames != want:
            sys.exit(f"GAGAL: kepala kolom TSV harus {want}, ditemukan {rd.fieldnames}")
        for n, r in enumerate(rd, start=2):
            k = (r["entity"], r["feature"], r["value"])
            if k not in CLAIMS:
                errors.append(f"baris {n}: klaim tidak ada di KB: {k}")
                continue
            c = CLAIMS[k]
            if str(c.weight) != r["weight"].strip():
                errors.append(f"baris {n}: bobot {r['weight']} != bobot KB {c.weight} untuk {k}")
            if r["source"] not in c.sources:
                errors.append(f"baris {n}: {r['source']} tidak dikutip oleh klaim {k} (dikutip: {','.join(c.sources)})")
            if r["source"] in UNREACHABLE:
                errors.append(f"baris {n}: {r['source']} tidak dapat diakses; tidak boleh ada temuan untuknya")
            if r["finding"] not in FINDINGS:
                errors.append(f"baris {n}: finding '{r['finding']}' tidak dikenal")
            if not r["locator"].strip() or not r["note"].strip():
                errors.append(f"baris {n}: locator/note kosong")
            if r["source"] in ev[k]:
                errors.append(f"baris {n}: duplikat {k} x {r['source']}")
            ev[k][r["source"]] = r
    return ev, errors


def combine(k, ev):
    """Temuan terbaik di antara sumber yang dikutip menentukan; konflik selalu dilaporkan."""
    c = CLAIMS[k]
    reach = [s for s in c.sources if s not in UNREACHABLE]
    unreach = [s for s in c.sources if s in UNREACHABLE]
    rows = [ev[k][s] for s in reach if s in ev.get(k, {})]
    missing = [s for s in reach if s not in ev.get(k, {})]
    if missing:
        return None, missing
    conflicts = [r for r in rows if r["finding"] == "conflicts"]
    pos = sorted((r for r in rows if r["finding"] in RANK), key=lambda r: (-RANK[r["finding"]], r["source"] == "S-01"))
    best = pos[0] if pos else None
    note_extra = ""
    if best is not None and best["finding"] == "supports":
        verdict, dec = "didukung", best
    elif best is not None and best["finding"] == "partly":
        verdict, dec = "sebagian", best
    elif conflicts:
        verdict, dec = "bertentangan", conflicts[0]
    elif unreach:
        verdict, dec = "sumber tidak dapat diakses", None
    else:
        verdict, dec = "tidak ditemukan", best
    if conflicts and verdict in ("didukung", "sebagian"):
        note_extra = " · KONFLIK " + "; ".join(f"{r['source']} ({r['locator']}): {r['note']}" for r in conflicts)
    pending = ""
    if unreach and verdict in ("sebagian", "bertentangan"):
        pending = ",".join(unreach)        # sumber tak terbaca yang masih dapat mengubah vonis
    if verdict == "sumber tidak dapat diakses":
        silent = "; ".join(f"{r['source']}: {r['note']}" for r in rows)
        return {"verdict": verdict, "deciding_source": ",".join(unreach), "locator": "-",
                "note": f"Bergantung pada {','.join(unreach)} yang belum dapat dibaca. " + silent,
                "conflict": bool(conflicts), "pending": ",".join(unreach)}, []
    if verdict == "tidak ditemukan" and len(rows) > 1:
        # semua sumber diam: tampilkan catatan tiap sumber, bukan hanya satu
        return {"verdict": verdict, "deciding_source": ",".join(r["source"] for r in rows),
                "locator": " · ".join(f"{r['source']}: {r['locator']}" for r in rows),
                "note": " · ".join(f"{r['source']}: {r['note']}" for r in rows), "conflict": False, "pending": pending}, []
    return {"verdict": verdict, "deciding_source": dec["source"], "locator": dec["locator"],
            "note": dec["note"] + note_extra, "conflict": bool(conflicts), "pending": pending}, []


# ---------------------------------------------------------------- cetak
def table(headers, rows):
    print("| " + " | ".join(headers) + " |")
    print("|" + "---|" * len(headers))
    for r in rows:
        print("| " + " | ".join(str(x) for x in r) + " |")
    print()


def h(title):
    print("=" * 100)
    print(title)
    print("=" * 100)


VERDICTS = ["didukung", "sebagian", "tidak ditemukan", "bertentangan", "sumber tidak dapat diakses"]


def wfmt(w):
    return "0" if w == 0 else f"{w:+d}"


def e_name(eid):
    return ENT[eid]["name_en"]


def counts_row(label, items):
    cc = collections.Counter(x["verdict"] for x in items)
    return [label, len(items)] + [cc.get(v, 0) for v in VERDICTS]


def wilson(x, n, z=1.96):
    p = x / n
    den = 1 + z * z / n
    mid = (p + z * z / (2 * n)) / den
    half = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / den
    return 100 * (mid - half), 100 * (mid + half)


def worklist(src):
    ev, _ = load_evidence()
    rows = []
    for k in ALLCHK:
        c = CLAIMS[k]
        if src in c.sources and src not in ev.get(k, {}):
            sets = "".join(s for s in "ABCDR" if k in SETS[s])
            rows.append((c.entity, c.feature, c.value, c.weight, sets, ",".join(c.sources)))
    for r in rows:
        print("\t".join(str(x) for x in r))
    print(f"# {len(rows)} klaim set A-D/R mengutip {src} dan belum punya temuan", file=sys.stderr)


def load_coverage():
    cov = {}
    if not COVER.exists():
        return cov
    with COVER.open(encoding="utf-8", newline="") as fh:
        for n, r in enumerate(csv.DictReader(fh, delimiter="\t"), start=2):
            if r["entity"] not in ENT or r["level"] not in COVER_LEVELS or r["depth"] not in DEPTHS:
                sys.exit(f"GAGAL: baris cakupan {n} tidak sah: {r}")
            if (r["level"] == "1") != (r["depth"] in ("uraian", "daftar")):
                sys.exit(f"GAGAL: baris cakupan {n}: depth hanya untuk tingkat 1: {r}")
            cov[(r["entity"], r["source"])] = r
    return cov


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "--worklist":
        return worklist(sys.argv[2])

    h("0. KLAIM DAN SET")
    feat = {k: c for k, c in CLAIMS.items() if k[1] != "rule"}
    wc = collections.Counter(c.weight for c in feat.values())
    print(f"entitas: {len(ENTS)}; klaim bobot fitur: {len(feat)}; bobot: " + ", ".join(f"{wfmt(w)}: {wc[w]}" for w in (3, 2, 1, 0, -2, -5))
          + f"; aturan: {len(SETS['R'])}")
    cs = collections.Counter(s for c in CLAIMS.values() for s in c.sources)
    print("klaim (termasuk aturan) per sumber: " + ", ".join(f"{s} {n}" for s, n in sorted(cs.items())))
    print(f"sumber tidak dapat diakses: {', '.join(sorted(UNREACHABLE))} "
          f"({sum(1 for c in CLAIMS.values() if set(c.sources) & UNREACHABLE)} klaim di seluruh KB; "
          f"{sum(1 for k in ALLCHK if set(CLAIMS[k].sources) & UNREACHABLE)} di set A-D/R)")
    for s in "ABCDR":
        print(f"set {s}: {len(SETS[s])} klaim")
    print(f"set C di dalam A: {len(set(SETS['C']) & set(SETS['A']))}; di dalam B: {len(set(SETS['C']) & set(SETS['B']))}; "
          f"di luar A dan B: {len(set(SETS['C']) - set(SETS['A']) - set(SETS['B']))}")
    print(f"gabungan A-D: {len(NEEDED)} klaim unik ({100 * len(NEEDED) / len(feat):.1f}% dari {len(feat)} klaim bobot fitur)")
    print(f"set D: benih {SEED}, {N_D} dari {FRAME_D} klaim di luar A, B, C (tanpa nilai not_applicable, tanpa aturan)")
    wd = collections.Counter(CLAIMS[k].weight for k in SETS["D"])
    print("set D menurut bobot: " + ", ".join(f"{wfmt(w)}: {wd[w]}" for w in (2, 1, 0, -2, -5)))
    so = sum(1 for k in SETS["D"] if CLAIMS[k].sources == ("S-01",))
    fo = sum(1 for k, c in feat.items() if c.sources == ("S-01",))
    print(f"set D yang hanya mengutip S-01: {so} dari {N_D} ({100 * so / N_D:.0f}%); seluruh KB: {fo} dari {len(feat)} ({100 * fo / len(feat):.1f}%)")
    print()

    ev, errors = load_evidence()
    if errors:
        print("GAGAL - berkas bukti tidak konsisten dengan KB:")
        for e in errors:
            print("  " + e)
        sys.exit(1)
    n_rows = sum(len(v) for v in ev.values())
    print(f"baris bukti: {n_rows} (klaim: {len(ev)}); semuanya cocok dengan klaim, bobot, dan sumber yang dikutip")
    fc = collections.Counter(r["finding"] for v in ev.values() for r in v.values())
    print("temuan per baris: " + ", ".join(f"{k}: {fc[k]}" for k in FINDINGS))
    sc = collections.Counter(r["source"] for v in ev.values() for r in v.values())
    print("baris bukti per sumber: " + ", ".join(f"{s} {n}" for s, n in sorted(sc.items())))
    n_ad = sum(len(v) for k, v in ev.items() if k in NEEDED)
    print(f"baris bukti untuk set A-D: {n_ad} ({sum(1 for k in ev if k in NEEDED)} klaim); untuk aturan (set R): {n_rows - n_ad}")
    extra = sorted(k for k in ev if k not in ALLCHK)
    print(f"baris bukti di luar set A-D/R: {len(extra)}")
    print()

    res, miss = {}, {}
    for k in ALLCHK:
        r, m = combine(k, ev)
        if r is None:
            miss[k] = m
        else:
            res[k] = r
    h("1. KLAIM YANG BELUM LENGKAP")
    if miss:
        for s in "ABCDR":
            mm = [k for k in SETS[s] if k in miss]
            print(f"set {s}: {len(mm)} belum lengkap")
            for k in mm:
                print(f"   {k[0]} {k[1]}:{k[2]} -> belum ada temuan untuk {','.join(miss[k])}")
    else:
        print("tidak ada: semua klaim set A, B, C, D dan R punya temuan untuk setiap sumber terjangkau yang dikutipnya")
    print()

    with OUT.open("w", encoding="utf-8", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["set", "entity", "feature", "value", "weight", "cited_sources", "verdict", "deciding_source", "locator",
                     "note", "earlier_verdict", "unread_cited_source"])
        for s in "ABCDR":
            for k in SETS[s]:
                if k not in res:
                    continue
                c, r = CLAIMS[k], res[k]
                wr.writerow([s, c.entity, c.feature, c.value, c.weight, ",".join(c.sources), r["verdict"], r["deciding_source"],
                             r["locator"], r["note"], EARLIER.get(k, ""), r["pending"]])
    print(f"ditulis: {OUT.relative_to(ROOT)} ({sum(1 for s in 'ABCDR' for k in SETS[s] if k in res)} baris; klaim di dua set muncul dua kali)")
    print()

    def items(keys):
        return [dict(res[k], key=k) for k in keys if k in res]

    def tagged(k, tag):
        return any(r["note"].startswith(tag) for r in ev.get(k, {}).values())

    h("2. VONIS PER SET")
    rows = [counts_row(f"Set {s}", items(SETS[s])) for s in "ABCD"]
    rows.append(counts_row("Gabungan A-D (klaim unik)", items(NEEDED)))
    table(["Set", "n"] + VERDICTS, rows)
    for s in "ABCD":
        it = items(SETS[s])
        n = len(it)
        cc = collections.Counter(x["verdict"] for x in it)
        print(f"Set {s} dalam persen (n = {n}): " + "; ".join(f"{v} {100 * cc.get(v, 0) / n:.0f}%" for v in VERDICTS[:4]))
    print()
    print("Set A menurut kelas tinjauan pertama:")
    table(["Kelas", "n"] + VERDICTS, [counts_row(cl, items([k for k in SETS["A"] if HC_CLASS[k] == cl])) for cl in ("b", "c")])
    print("Set D menurut bobot:")
    table(["Bobot", "n"] + VERDICTS,
          [counts_row(wfmt(w), items([k for k in SETS["D"] if CLAIMS[k].weight == w])) for w in (2, 1, 0, -2, -5)])
    d = items(SETS["D"])
    if d:
        n = len(d)
        ok = sum(x["verdict"] == "didukung" for x in d)
        part = sum(x["verdict"] == "sebagian" for x in d)
        nf = sum(x["verdict"] == "tidak ditemukan" for x in d)
        for lab, x in (("didukung", ok), ("didukung atau sebagian", ok + part), ("tidak ditemukan", nf)):
            lo, hi = wilson(x, n)
            print(f"Set D: {lab} {x}/{n} = {100 * x / n:.0f}% (selang Wilson 95%: {lo:.0f}%-{hi:.0f}%)")
    print()
    print("Klaim yang hanya mengutip S-01 dibanding klaim dengan sumber kedua:")
    rows = []
    for s in "ABCD":
        one = [k for k in SETS[s] if CLAIMS[k].sources == ("S-01",)]
        two = [k for k in SETS[s] if CLAIMS[k].sources != ("S-01",)]
        rows.append(counts_row(f"Set {s} - hanya S-01", items(one)))
        rows.append(counts_row(f"Set {s} - ada sumber lain", items(two)))
    table(["Kelompok", "n"] + VERDICTS, rows)

    h("2b. ANALISIS KEPEKAAN TERHADAP ATURAN KETAT")
    print("Jika keanggotaan daftar pada nilai yang diklaim ([daftar]) dianggap cukup untuk +3/+2:")
    for s in "ABCD":
        ks = [k for k in SETS[s] if k in res and res[k]["verdict"] == "sebagian" and CLAIMS[k].weight >= 2 and tagged(k, "[daftar]")]
        base = sum(1 for k in SETS[s] if k in res and res[k]["verdict"] == "didukung")
        print(f"   set {s}: {len(ks)} klaim 'sebagian' naik menjadi 'didukung' ({base} -> {base + len(ks)} dari {len(SETS[s])})")
    print("Jika tercantum pada nilai lain ([daftar-lain]) dianggap memberi arah untuk bobot negatif:")
    for s in "ABCD":
        ks = [k for k in SETS[s] if k in res and res[k]["verdict"] == "tidak ditemukan" and CLAIMS[k].weight < 0 and tagged(k, "[daftar-lain]")]
        base = sum(1 for k in SETS[s] if k in res and res[k]["verdict"] == "sebagian")
        print(f"   set {s}: {len(ks)} klaim 'tidak ditemukan' naik menjadi 'sebagian' ({base} -> {base + len(ks)} dari {len(SETS[s])})")
    print("Jika pernyataan tingkat kelompok ([umum]) dianggap memberi arah:")
    for s in "ABCD":
        ks = [k for k in SETS[s] if k in res and res[k]["verdict"] == "tidak ditemukan" and tagged(k, "[umum]")]
        print(f"   set {s}: {len(ks)} klaim 'tidak ditemukan' naik menjadi 'sebagian'")
    print()

    print("Batas atas pengaruh gambar S-01 yang isinya tidak terbaca (Fig. 1 dan Fig. 3: ilustrasi predileksi tulang, lokasi, usia):")
    locage = {"age_group", "bone_class", "longitudinal", "transverse"}
    for s in "ABCD":
        ks = [k for k in SETS[s] if k in res and k[1] in locage and "S-01" in CLAIMS[k].sources]
        nf = sum(1 for k in ks if res[k]["verdict"] == "tidak ditemukan")
        pa = sum(1 for k in ks if res[k]["verdict"] == "sebagian")
        print(f"   set {s}: klaim usia/lokasi yang mengutip S-01 dan bervonis 'tidak ditemukan': {nf}; 'sebagian': {pa}")
    print()

    h("3. VONIS PER FITUR (per set)")
    for s in "ABCD":
        print(f"Set {s}:")
        feats = [f for f in FEAT if any(k[1] == f for k in SETS[s])]
        table(["Fitur", "n"] + VERDICTS, [counts_row(f"`{f}`", items([k for k in SETS[s] if k[1] == f])) for f in feats])
    print("Gabungan A-D (klaim unik):")
    table(["Fitur", "n"] + VERDICTS, [counts_row(f"`{f}`", items([k for k in NEEDED if k[1] == f])) for f in FEAT])

    h("4. TEMUAN PER SUMBER (baris bukti: satu klaim x satu sumber)")
    for s in "ABCD":
        print(f"Set {s}:")
        rows = []
        for src in sorted(cs):
            ks = [k for k in SETS[s] if src in CLAIMS[k].sources]
            if not ks:
                continue
            if src in UNREACHABLE:
                rows.append([src, len(ks), "-", "-", "-", "-"])
                continue
            fc = collections.Counter(ev[k][src]["finding"] for k in ks if src in ev.get(k, {}))
            rows.append([src, len(ks)] + [fc.get(x, 0) for x in FINDINGS])
        table(["Sumber", "klaim yang mengutip"] + list(FINDINGS), rows)
    print("Gabungan A-D (klaim unik):")
    rows = []
    for src in sorted(cs):
        ks = [k for k in NEEDED if src in CLAIMS[k].sources]
        if not ks:
            continue
        if src in UNREACHABLE:
            rows.append([src, len(ks), "-", "-", "-", "-", "-"])
            continue
        fc = collections.Counter(ev[k][src]["finding"] for k in ks if src in ev.get(k, {}))
        n = sum(fc.values())
        rows.append([src, len(ks)] + [fc.get(x, 0) for x in FINDINGS] + [f"{100 * fc.get('silent', 0) / n:.0f}%" if n else "-"])
    table(["Sumber", "klaim yang mengutip"] + list(FINDINGS) + ["% diam"], rows)
    print("Sumber penentu vonis didukung/sebagian (gabungan A-D; pada temuan setara dipilih sumber selain S-01):")
    dc = collections.Counter((res[k]["deciding_source"], res[k]["verdict"]) for k in NEEDED if k in res and res[k]["verdict"] in ("didukung", "sebagian"))
    table(["Sumber", "didukung", "sebagian"], [[s2, dc.get((s2, "didukung"), 0), dc.get((s2, "sebagian"), 0)] for s2 in sorted({a for a, _ in dc})])
    print("Klaim dua sumber: apakah sumber selain S-01 menambah dukungan? (gabungan A-D)")
    rows = []
    for src in sorted(cs):
        if src == "S-01" or src in UNREACHABLE:
            continue
        ks = [k for k in NEEDED if src in CLAIMS[k].sources and "S-01" in CLAIMS[k].sources and k in ev and src in ev[k] and "S-01" in ev[k]]
        if not ks:
            continue
        better = sum(RANK.get(ev[k][src]["finding"], 0) > RANK.get(ev[k]["S-01"]["finding"], 0) for k in ks)
        same = sum(RANK.get(ev[k][src]["finding"], 0) == RANK.get(ev[k]["S-01"]["finding"], 0) for k in ks)
        rows.append([src, len(ks), better, same, len(ks) - better - same])
    table(["Sumber kedua", "klaim", "lebih kuat dari S-01", "setara", "lebih lemah dari S-01"], rows)

    h("5. VONIS PER ENTITAS")
    print("Gabungan A-D (klaim unik):")
    table(["Entitas", "n"] + VERDICTS, [counts_row(e["name_en"], items([k for k in NEEDED if k[0] == e["id"]])) for e in ENTS])
    print("Set B (+3) per entitas:")
    table(["Entitas", "n (+3)"] + VERDICTS, [counts_row(e["name_en"], items([k for k in SETS["B"] if k[0] == e["id"]])) for e in ENTS])
    print("Klaim tanpa dukungan (tidak ditemukan/bertentangan) per entitas, gabungan A-D:")
    for e in ENTS:
        ks = [k for k in NEEDED if k[0] == e["id"] and k in res and res[k]["verdict"] in ("tidak ditemukan", "bertentangan")]
        if not ks:
            continue
        b3 = [f"{k[1]}:{k[2]}" for k in ks if CLAIMS[k].weight == 3]
        hc = [f"{k[1]}:{k[2]}" for k in ks if CLAIMS[k].weight == -5]
        ot = [f"{k[1]}:{k[2]} ({wfmt(CLAIMS[k].weight)})" for k in ks if CLAIMS[k].weight not in (3, -5)]
        print(f"- {e['name_en']} [{len(ks)}]")
        if b3:
            print("     +3: " + ", ".join(b3))
        if hc:
            print("     -5: " + ", ".join(hc))
        if ot:
            print("     lain: " + ", ".join(ot))
    print()

    h("6. KLAIM BERTENTANGAN DAN KONFLIK YANG DICATAT")
    rows = []
    for k in NEEDED:
        if k in res and res[k]["verdict"] == "bertentangan":
            c = CLAIMS[k]
            sets = "".join(s for s in "ABCD" if k in SETS[s])
            rows.append([sets, e_name(k[0]), f"`{k[1]}:{k[2]}`", wfmt(c.weight), ",".join(c.sources), res[k]["deciding_source"], res[k]["locator"], res[k]["note"]])
    print(f"vonis bertentangan: {len(rows)}")
    table(["Set", "Entitas", "Klaim", "Bobot", "Sumber dikutip", "Sumber", "Lokasi", "Catatan"], rows)
    rows = []
    for k in NEEDED:
        if k in res and res[k]["conflict"] and res[k]["verdict"] != "bertentangan":
            c = CLAIMS[k]
            sets = "".join(s for s in "ABCD" if k in SETS[s])
            rows.append([sets, e_name(k[0]), f"`{k[1]}:{k[2]}`", wfmt(c.weight), res[k]["verdict"], res[k]["note"]])
    print(f"konflik pada klaim yang tetap didukung/sebagian oleh sumber lain: {len(rows)}")
    table(["Set", "Entitas", "Klaim", "Bobot", "Vonis", "Catatan"], rows)

    h("7. PERUBAHAN TERHADAP UJI PETIK LAMA (50 butir)")
    rows, changed, same = [], 0, 0
    for k in sorted(EARLIER):
        if k not in res:
            continue
        c = CLAIMS[k]
        new, old = res[k]["verdict"], EARLIER[k]
        changed += new != old
        same += new == old
        sets = "".join(s for s in "ABCD" if k in SETS[s])
        rows.append([sets, e_name(k[0]), f"`{k[1]}:{k[2]}`", wfmt(c.weight), old, EARLIER_HOW[k], new, "sama" if new == old else "BERUBAH",
                     res[k]["deciding_source"], res[k]["note"]])
    table(["Set", "Entitas", "Klaim", "Bobot", "Lama", "Cara baca lama", "Baru", "", "Sumber", "Catatan"], rows)
    print(f"butir uji petik lama yang dinilai ulang: {changed + same} dari {len(EARLIER)}; berubah: {changed}; sama: {same}")
    notre = sorted(k for k in EARLIER if k not in res)
    print(f"butir lama yang tidak dinilai ulang (didukung/sebagian dan di luar set A, B, D): {len(notre)}: "
          + ", ".join(f"{e_name(k[0])} {k[1]}:{k[2]}" for k in notre))
    cset = [k for k in SETS["C"] if k in res]
    cc = collections.Counter((EARLIER[k], res[k]["verdict"]) for k in cset)
    print("Set C (lama -> baru): " + "; ".join(f"{a} -> {b}: {n}" for (a, b), n in sorted(cc.items())))
    allr = [k for k in EARLIER if k in res]
    cc = collections.Counter((EARLIER[k], res[k]["verdict"]) for k in allr)
    print("Semua butir lama yang dinilai ulang (lama -> baru): " + "; ".join(f"{a} -> {b}: {n}" for (a, b), n in sorted(cc.items())))
    up = sum(1 for k in allr if VERDICTS.index(res[k]["verdict"]) < VERDICTS.index(EARLIER[k]))
    down = sum(1 for k in allr if VERDICTS.index(res[k]["verdict"]) > VERDICTS.index(EARLIER[k]))
    print(f"arah perubahan: lebih mendukung {up}; kurang mendukung {down}")
    print()

    h("8. CAKUPAN ENTITAS x SUMBER")
    cov = load_coverage()
    if cov:
        print("Tingkat: 1 = memuat gambaran radiografik entitas (uraian = pernyataan tersendiri; daftar = hanya keanggotaan daftar per fitur);")
        print("2 = hanya data usia/lokasi; 3 = hanya disebut sekilas; 4 = tidak ada. Angka dalam kurung = jumlah klaim entitas yang mengutip sumber itu.")
        print("Kolom 'temuan A-D' = baris bukti set A-D untuk pasangan itu: mendukung/sebagian/diam/konflik.")
        rows, best = [], {}
        for e in ENTS:
            per = collections.Counter(s for k, c in feat.items() if k[0] == e["id"] for s in c.sources)
            n = sum(1 for k in feat if k[0] == e["id"])
            lv_best, dp_best = 4, "-"
            for s in sorted(per):
                if s in UNREACHABLE:
                    rows.append([e["name_en"], n, f"{s} ({per[s]})", "tidak dapat diakses", "-", "-", ""])
                    continue
                r = cov.get((e["id"], s))
                if r is None:
                    sys.exit(f"GAGAL: cakupan belum dicatat untuk {e['id']} x {s}")
                fc = collections.Counter(ev[k][s]["finding"] for k in NEEDED if k[0] == e["id"] and s in ev.get(k, {}))
                tally = "/".join(str(fc.get(x, 0)) for x in FINDINGS)
                rows.append([e["name_en"], n, f"{s} ({per[s]})", r["level"], r["depth"], tally, r["note"]])
                key = (int(r["level"]), 0 if r["depth"] == "uraian" else 1)
                if key < (lv_best, 0 if dp_best == "uraian" else 1):
                    lv_best, dp_best = int(r["level"]), r["depth"]
            best[e["id"]] = (lv_best, dp_best)
        table(["Entitas", "klaim", "Sumber (klaim)", "Tingkat", "Kedalaman", "temuan A-D", "Catatan"], rows)
        print("Tabel ringkas (satu baris per entitas; kolom terakhir = klaim set A-D yang tidak ditemukan atau bertentangan / yang diperiksa):")
        rows2 = []
        for e in ENTS:
            per = collections.Counter(s for k, c in feat.items() if k[0] == e["id"] for s in c.sources)

            def cell(s):
                if s in UNREACHABLE:
                    return f"{s} belum dibaca ({per[s]})"
                r = cov[(e["id"], s)]
                lab = r["level"] + ("-" + r["depth"] if r["level"] == "1" else "")
                return f"{s} {lab} ({per[s]})"
            others = "; ".join(cell(s) for s in sorted(per) if s != "S-01") or "-"
            ks = [k for k in NEEDED if k[0] == e["id"] and k in res]
            bad = sum(1 for k in ks if res[k]["verdict"] in ("tidak ditemukan", "bertentangan"))
            rows2.append([e["name_en"], cell("S-01").replace("S-01 ", ""), others, f"{bad}/{len(ks)}"])
        table(["Entitas", "S-01: tingkat (klaim)", "Sumber lain: tingkat (klaim)", "tanpa dukungan / diperiksa"], rows2)
        stray = sorted(k for k in cov if not any(k[0] == c.entity and k[1] in c.sources for c in feat.values()))
        print(f"baris cakupan untuk pasangan yang tidak dikutip klaim mana pun: {len(stray)}")
        groups = collections.defaultdict(list)
        for e in ENTS:
            lv, dp = best[e["id"]]
            lab = {(1, "uraian"): "1-uraian", (1, "daftar"): "1-daftar"}.get((lv, dp), str(lv))
            groups[lab].append(e["name_en"])
        print("Entitas menurut cakupan terbaik di antara sumber terjangkau yang dikutipnya:")
        for lab in ("1-uraian", "1-daftar", "2", "3", "4"):
            print(f"   {lab}: {len(groups[lab])}" + (": " + "; ".join(groups[lab]) if groups[lab] else ""))
        print()
        # entitas yang uraian radiografiknya hanya dari S-01
        only01 = [e["name_en"] for e in ENTS if best[e["id"]] == (1, "uraian")
                  and not any(cov[(e["id"], s)]["depth"] == "uraian" for s in {s for (ee, s) in cov if ee == e["id"]} if s != "S-01")]
        print(f"entitas yang satu-satunya uraian radiografiknya berasal dari S-01: {len(only01)}: " + "; ".join(only01))
        print()
        pc = collections.Counter()
        for (eid, s), r in cov.items():
            pc[(s, r["level"] + ("-" + r["depth"] if r["level"] == "1" else ""))] += 1
        cols = ["1-uraian", "1-daftar", "2", "3", "4"]
        print("Per sumber: jumlah entitas yang mengutipnya menurut tingkat")
        table(["Sumber"] + cols, [[s] + [pc.get((s, c), 0) for c in cols] for s in sorted({s for _, s in cov})])
        rows, tot = [], 0
        for (eid, s), r in sorted(cov.items()):
            if r["level"] in ("2", "3", "4") and s != "S-01":
                n = sum(1 for k, c in feat.items() if k[0] == eid and s in c.sources)
                tot += n
                rows.append([ENT[eid]["name_en"], s, r["level"], n, r["note"]])
        print("Sumber kedua (selain S-01) yang untuk entitas itu tidak memuat gambaran radiografik:")
        table(["Entitas", "Sumber", "Tingkat", "klaim yang mengutip", "Catatan"], rows)
        print(f"jumlah kutipan klaim ke sumber kedua bertingkat 2-4: {tot}")
        nonloc = {"density", "margin_lodwick", "cortex", "soft_tissue_mass", "periosteal", "matrix", "size_cm"}
        bad = [k for k, c in feat.items() if k[1] in nonloc
               and all(s in UNREACHABLE or cov[(k[0], s)]["level"] != "1" for s in c.sources)]
        tot_app = sum(1 for k in feat if k[1] in nonloc)
        print(f"klaim fitur tampilan (densitas, tepi, korteks, jaringan lunak, periosteal, matriks, ukuran) yang tidak satu pun "
              f"sumber terjangkaunya bertingkat 1 untuk entitasnya: {len(bad)} dari {tot_app} di seluruh KB")
        bc = collections.Counter(k[0] for k in bad)
        print("   per entitas: " + "; ".join(f"{e_name(e)} {n}" for e, n in bc.most_common()))
        weak = [k for k, c in feat.items() if k[1] in nonloc
                and all(s in UNREACHABLE or cov[(k[0], s)]["depth"] != "uraian" for s in c.sources)]
        print(f"klaim fitur tampilan yang tidak satu pun sumber terjangkaunya memuat uraian tersendiri (tingkat 1-uraian): {len(weak)} dari {tot_app}")
        wk = collections.Counter(k[0] for k in weak)
        print("   per entitas: " + "; ".join(f"{e_name(e)} {n}" for e, n in wk.most_common()))
    else:
        print("berkas cakupan belum ada")
    print()

    h("9. ATURAN (set R, di luar set A-D)")
    rows = []
    for k in SETS["R"]:
        if k in res:
            c = CLAIMS[k]
            rows.append([e_name(k[0]), f"`{k[2]}`", wfmt(c.weight), ",".join(c.sources), res[k]["verdict"], res[k]["deciding_source"], res[k]["locator"], res[k]["note"]])
    table(["Entitas", "Aturan", "Bobot", "Dikutip", "Vonis", "Sumber", "Lokasi", "Catatan"], rows)
    print("vonis aturan: " + "; ".join(f"{v}: {n}" for v, n in collections.Counter(r[4] for r in rows).most_common()))
    print()

    h("10. DAFTAR LENGKAP VONIS (set A, B, C, D)")
    for s in "ABCD":
        print(f"Set {s}:")
        rows = []
        for k in SETS[s]:
            if k not in res:
                continue
            c = CLAIMS[k]
            rows.append([e_name(k[0]), f"`{k[1]}:{k[2]}`", wfmt(c.weight), ",".join(c.sources), res[k]["verdict"], res[k]["deciding_source"], res[k]["locator"], res[k]["note"]])
        table(["Entitas", "Klaim", "Bobot", "Dikutip", "Vonis", "Sumber", "Lokasi", "Catatan"], rows)


if __name__ == "__main__":
    main()
