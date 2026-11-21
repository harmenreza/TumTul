# Tinjauan Skor Basis Pengetahuan TumTul v0.6.0

**Tanggal:** 2026-11-21 · **Objek:** `data/entities/*.json`, `data/features.json`, `data/sources.json` (KB 0.6.0, skema v1.1.0, aturan isian UI v0.6.3) · **Status:** tinjauan konsistensi dan kewajaran; **tidak ada bobot, entitas, fitur, atau skema yang diubah**.

Semua angka berasal dari `tools/review_scoring.py`; keluaran lengkapnya ada di `docs/tinjauan-skor-v0.6-keluaran.txt`. Klasifikasi 322 hard constraint ada di `docs/tinjauan-skor-v0.6-hard-constraints.csv`. Setiap temuan adalah **hipotesis untuk v0.7** yang harus diuji pada kasus praktik baru sesuai protokol terdaftar, bukan disetel pada kasus v1–v4.

---

## 1. Ringkasan

1. **Temuan "normal/tidak ada" diberi bobot setara ciri khas.** `cortex:intact`, `periosteal:none`, dan `matrix:none` memuat 16 bobot +3; jumlah bobot empat temuan negatif berkisar dari −6 (Conventional OS) sampai +8 (Enostosis, Geode). Akibatnya Bone infarct mengalahkan Enchondroma dan Intraosseous lipoma pada vinyet tipikal keduanya (H-01).
2. **Over-calling CMF dan GCTB bersifat struktural.** GCTB punya maksimum tertinggi pada 6 fitur inti (18), CMF/NOF/SBC 17 (median 14). CMF masuk 3 besar pada 58% kombinasi "remaja, tulang panjang, litik"; GCTB pada 46% kombinasi dewasa yang setara; CMF seri dengan NOF pada vinyet tipikal NOF (H-02, H-03).
3. **Plafon skor tidak setara.** Skor maksimum yang dapat dicapai berkisar 14 (BPOP) sampai 26 (Ewing, Osteoid osteoma). Entitas jarang dirugikan dua kali: oleh prior dan oleh plafon yang lebih rendah (median maksimum tanpa prior 24 / 21 / 20 untuk prior 0 / −1 / −2) (H-30, opsi skema S-1).
4. **Dari 322 hard constraint, 249 dapat dipertahankan, 65 meragukan, 8 tidak konsisten;** 26 di antaranya berkeyakinan sedang. Pada 193 kasus v1–v4, 7 entitas rujukan tersingkir oleh 9 klaim −5 (H-06 sampai H-18).
5. **Satu ketukan dapat menghapus sebagian besar banding.** `matrix:ground_glass` menyingkirkan 27 dari 37 entitas (73%); `periosteal:spiculated` dan `matrix:chondroid` 20; `margin_lodwick:III` dan `transverse:juxtacortical_continuous` 18. Sebanyak 318 dari 322 hard constraint tidak punya teks alasan (`note_id`) (H-27, opsi S-3).
6. **Aturan "massa jaringan lunak tanpa destruksi" (Ewing, limfoma) menyala pada `cortex:focal_breach`.** Pada v1–v4 aturan ini menyala 15 kali, semuanya lewat `focal_breach`; 3 kali rujukannya memang Ewing/limfoma, 8 kali Ewing/limfoma menjadi peringkat 1 yang salah (H-05).
7. **Beberapa fitur hanya menaikkan, tidak pernah menurunkan.** `multiplicity:multiple` punya 13 klaim positif dan 0 negatif; `night_pain_nsaid_relief` hanya dinilai untuk Osteoid osteoma; `fever_or_infection_signs` hanya untuk dua entitas infeksi; ukuran hanya dinilai pada 10 entitas (H-19, H-20).
8. **Osteomyelitis tidak punya satu pun bobot −2 dan bobot usianya selalu positif** (rata-rata +1,7). Dalam konteks tulang panjang tanpa flag klinis, Osteomyelitis dapat unggul 22 poin atas Conventional OS, sedangkan sebaliknya paling banyak 9 (H-04).
9. **Pada input jarang, prior dan seri menentukan hasil.** Selisih skor peringkat 1 dan entitas ke-5 bermedian 2–3 poin; prior mengubah himpunan 3 besar pada 56–73% kombinasi; rata-rata 1,4–1,7 entitas berbagi peringkat 1 dan 6,1–6,8 entitas berperingkat ≤5.
10. **Sumber sangat terpusat pada S-01.** 41,7% klaim hanya mengutip S-01 dan 99,3% mengutipnya; 14 entitas seluruhnya hanya S-01, padahal S-01 tidak memuat gambaran radiografik Chordoma, Skeletal TB, atau Vertebral haemangioma. 44 dari 46 klaim CMF mengutip S-06, yang tidak membahas CMF. Dari 50 klaim yang diuji petik: 22 didukung, 10 sebagian, 12 tidak ditemukan, 6 bertentangan dengan sumbernya (H-26, H-28).
11. **Ada ketidakkonsistenan internal yang dapat diperbaiki tanpa data baru:** `10-19_unknown` sama dengan nilai paling menguntungkan pada 10 dari 11 entitas yang membedakan status fisis (H-22); Metastasis −2 pada `0-9` tetapi −5 pada seluruh 10–19 (H-06); ekspansi dihitung dua kali lewat `cortex:expansion_shell` + `periosteal:shell` (ABC +6) (H-21).
12. **Vinyet buatan peninjau:** entitas yang diharapkan berperingkat 1 pada 40 dari 48 vinyet (36 tanpa seri) dan masuk 3 besar pada 47. Yang gagal: Enchondroma dan lipoma (kalah dari Bone infarct), Desmoplastic fibroma (kalah dari SBC pada usia 24 tahun), OFD anak (peringkat 4), Ewing pelvis dewasa (kalah dari Lymphoma), abses Brodie (kalah dari SBC), fraktur insufisiensi sakrum (kalah dari Enostosis), Paget vertebra (kalah dari hemangioma).

---

## 2. Metode dan batasan

**Yang dikerjakan.** Satu skrip baca-saja (`tools/review_scoring.py`, pustaka standar Python) memuat KB, mereproduksi logika skor normatif (`docs/SKEMA-DIAGNOSIS.md` §4, `tools/score_smoke.py`), dan menghitung: (1) semua hard constraint, jumlah per nilai dan per entitas, "tebing" pada fitur berurutan, serta kasus v1–v4 yang rujukannya tersingkir; (2) jumlah klaim, skor maksimum yang dapat dicapai di bawah aturan isian UI (dengan aturan khusus, tanpa memicu −5 sendiri), dan simulasi semua kombinasi input jarang yang dapat diisi; (3) cakupan klaim per nilai, klaim tak terjangkau, dan klaim yang diharapkan; (4) jarak profil 666 pasangan entitas dan selisih skor maksimum antar-pasangan; (5) 48 vinyet tipikal buatan peninjau; (6) pemusatan sumber.

Hitungan dasar cocok dengan `tools/build_matrix.py`: 37 entitas, 62 nilai fitur, 1584 klaim (termasuk 4 `not_applicable`), 322 hard constraint, 5 aturan; +3/+2/+1/0/−2/−5 = 192/248/382/179/257/322. Tidak ada bobot di luar skala.

**Kasus uji.** `cases_v1.json`–`cases_v4.json` hanya ada di Project, bukan di repo. Fitur dan entitas rujukan 193 kasus ditranskripsi ke `tools/review_cases_v1_v4.txt`. Transkripsi diverifikasi dengan menghitung ulang: skor dan peringkat rujukan cocok dengan hasil tersimpan pada 193 dari 193 kasus, dan Top-3 yang diperoleh (26/31, 52/74, 25/52, 25/36) sama dengan laporan validasi. Kasus dipakai hanya sebagai bukti deskriptif; tidak ada bobot yang dicoba-ubah terhadapnya.

**Uji petik sumber.** S-01 dibaca teks lengkapnya lewat PubMed/PMC ([DOI](https://doi.org/10.1007/s00256-024-04854-6)). S-04, S-06, S-15, S-16, S-19, S-22, S-23, dan S-25 dibaca lewat halaman penerbit dengan WebFetch; S-10 hanya abstraknya.

**Batasan.**

- Ini tinjauan konsistensi dan kewajaran, **bukan validasi**. Tidak ada angka akurasi yang dihasilkan.
- Klasifikasi hard constraint, daftar klaim yang diharapkan, dan vinyet adalah penilaian peninjau (model AI) dari pengetahuan radiologi MSK umum. Kelas "a" tidak diverifikasi satu per satu ke sumber. Pernyataan "dilaporkan" pada kelas "b" berasal dari ingatan literatur, tanpa rujukan per butir; semuanya perlu dinilai pemilik.
- Vinyet ditulis setelah peninjau melihat bobot, sehingga dapat tanpa sengaja selaras dengan KB; kegagalannya lebih informatif daripada keberhasilannya.
- Simulasi input jarang memberi bobot sama pada setiap kombinasi yang dapat diisi, termasuk kombinasi yang jarang secara klinis. Frekuensi 3 besar di sana adalah sifat struktur bobot, bukan perkiraan kinerja.
- Jawaban WebFetch dihasilkan model kecil dari 100.000 karakter pertama halaman; kurang andal dibanding membaca teks lengkap. S-18 (sumber kedua untuk 90 klaim kondroid) tidak dapat diakses. S-05, S-20, S-21, S-24, S-26 tidak diperiksa.
- Dokumen Project yang dibaca: `SKEMA-DIAGNOSIS.md`, `score_smoke.py`, `validate_cases.py`, `VALIDASI-INTERNAL-v3.md`, `-v4.md`, `cases_v1..v4.json`. Tidak dibaca: `VALIDASI-INTERNAL-v1.md`, `-v2.md`, `results_*.md`, protokol v3/v4.
- Sumbu A tidak ditinjau.

**Pemeriksaan ulang oleh sesi utama (2026-11-21).** Tinjauan ini dikerjakan oleh satu agen terpisah; sesi utama memeriksa hasilnya sebelum laporan disimpan:

- Skrip dijalankan ulang dari awal; keluarannya identik dengan `docs/tinjauan-skor-v0.6-keluaran.txt`. Tidak ada berkas di `data/` atau `schema/` yang berubah.
- Angka pokok dihitung ulang secara terpisah dari berkas entitas dan cocok: 16 bobot +3 pada temuan normal; `ground_glass` menyingkirkan 27 entitas; 318 dari 322 hard constraint tanpa `note_id`; 41,7% klaim hanya S-01; 14 entitas seluruhnya S-01; 44 dari 46 klaim CMF mengutip S-06; `multiple` 13 positif dan 0 negatif; `long_bone` +3 pada 14 entitas.
- Semua bobot yang disebut di tabel hipotesis (H-06 sampai H-25, H-33) dicek ke berkas entitas dan sesuai.
- S-06 dibaca teks lengkapnya lewat PubMed/PMC ([DOI](https://doi.org/10.3390/jcm11030699)): benar tidak ada bagian tentang CMF (CMF hanya disebut sekali, dalam daftar banding kondroblastoma), dan benar S-06 menyebut CT dapat menunjukkan perluasan kondroblastoma ke jaringan lunak.
- **Tidak diperiksa ulang:** klasifikasi a/b/c tiap hard constraint, 48 vinyet, simulasi input jarang, dan 49 butir uji petik sumber lainnya.

---

## 3. Temuan per bagian

### 3.1 Hard constraint

**Klasifikasi.** a = dapat dipertahankan (bertentangan dengan definisi atau pada dasarnya tidak dilaporkan); b = meragukan (jarang tetapi dilaporkan, atau wajar pada kasus atipikal, lanjut, atau dengan fraktur); c = tidak konsisten dengan nilai tetangga atau entitas kerabat.

| Fitur | −5 | a | b | c |
|---|---|---|---|---|
| `age_group` | 32 | 14 | 15 | 3 |
| `bone_class` | 16 | 16 | 0 | 0 |
| `longitudinal` | 9 | 7 | 2 | 0 |
| `transverse` | 51 | 50 | 1 | 0 |
| `density` | 14 | 10 | 4 | 0 |
| `margin_lodwick` | 47 | 36 | 11 | 0 |
| `cortex` | 21 | 15 | 6 | 0 |
| `soft_tissue_mass` | 12 | 6 | 6 | 0 |
| `periosteal` | 54 | 45 | 5 | 4 |
| `matrix` | 64 | 50 | 14 | 0 |
| `size_cm` | 2 | 0 | 1 | 1 |
| **Jumlah** | **322** | **249** | **65** | **8** |

Dari 73 butir b/c, 26 berkeyakinan sedang dan 47 rendah. Yang berkeyakinan rendah sebagian besar adalah batas usia 60+ untuk tumor usia muda dan pola matriks yang dapat salah dibaca; menurut saya ini tidak mendesak. Butir berkeyakinan sedang menjadi H-06 sampai H-18 di bagian 4.

**Bukti langsung dari kasus uji.** Entitas rujukan tersingkir pada 7 dari 193 kasus:

| Kasus | Rujukan | Klaim −5 | Penilaian |
|---|---|---|---|
| V2-15 | BPOP | `transverse:juxtacortical_continuous` | b — kesan kontinuitas pada BPOP dilaporkan |
| V2-74 | Geode/ganglion | `margin_lodwick:IC`; `soft_tissue_mass:present` | b — keduanya |
| V3-06 | Chondroblastoma | `cortex:destruction`; `soft_tissue_mass:present` | b — S-06 sendiri menyebut perluasan jaringan lunak |
| V3-09 | Conventional OS | `margin_lodwick:IA` | b |
| V3-22 | Chordoma | `bone_class:long_bone` | a — kordoma ekstra-aksial; eksklusi wajar |
| V3-34 | SBC | `age_group:60+` | b |
| V3-46 | BPOP | `density:lytic` | b |

Ketujuh kasus ini atipikal menurut pengodenya. Itu tidak membatalkan temuan: hard constraint dimaksudkan untuk "hampir mustahil", dan kombinasi ini terbukti terjadi; hanya eksklusi V3-22 yang menurut saya tetap wajar.

**Pola yang patut diperhatikan.**

- **Usia.** Metastasis: `0-9` = −2, tetapi `10-19_open/closed/unknown` = −5. Remaja dengan lesi multipel dan riwayat keganasan tidak dapat memperoleh Metastasis walau flag `known_primary_malignancy` (+3) diisi. Sembilan entitas diberi −5 pada `60+`; pada delapan di antaranya `40-59` hanya −2. Hanya SBC yang punya bukti langsung.
- **Fraktur patologis.** Definisi SBC menyebut fraktur sebagai presentasi tersering dan pitfalls NOF menyebut fraktur pada lesi besar, tetapi `periosteal:lamellated` = −5 pada SBC, NOF, dan Fibrous dysplasia. v0.6 melonggarkan nilai yang sama menjadi −2 hanya untuk CMF. S-22 menyatakan reaksi periosteal pada displasia fibrosa muncul bila ada fraktur, dan fraktur sering.
- **Matriks yang dapat salah dibaca.** `matrix:osteoid` = −5 pada Osteomyelitis: pembaca yang memilih "osteoid (padat)" untuk sekuestrum atau sklerosis reaktif menyingkirkan infeksi dari banding osteosarkoma. Hal serupa berlaku pada Central CS (kalsifikasi kondroid padat; komponen dediferensiasi) dan Brown tumour (`ground_glass` adalah deskriptor klasik tulang hiperparatiroid).
- **Ukuran osteoid osteoma.** KB menilai densitas dari sklerosis reaktif (`sclerotic` +3) tetapi ukuran dari nidus (`>5` = −5). Pembaca yang mengukur zona sklerosis menyingkirkan diagnosis yang benar.
- **Temuan sama, bobot beda.** Conventional OS: `cortex:expansion_shell` −2 tetapi `periosteal:shell` −5.
- **Telangiectatic OS `margin_lodwick:IA` = −5** bertentangan dengan definisinya sebagai peniru ABC; S-15 menyebut tepi sklerotik ireguler kadang dijumpai.
- **"Tebing".** Ada 28 tempat nilai −5 bersebelahan dengan nilai ≥0 pada fitur berurutan, misalnya CMF `IB` 0 → `IC` −5, SBC `IB` +2 → `IC` −5, Fibrous dysplasia `IB` +1 → `IC` −5, Geode `<2`/`2-5` → `>5`. Batas Lodwick IB/IC adalah batas yang kesepakatan antar-pembacanya terbatas.

**Nilai yang menyingkirkan paling banyak entitas** ada di Lampiran B. Kombinasi agresif `margin III + destruction + massa + spiculated` menyisakan 14 entitas; `ground_glass` saja menyisakan 10.

### 3.2 Keseimbangan struktural

**Plafon.** Tabel lengkap di Lampiran A.

| Ukuran | Min | Median | Maks |
|---|---|---|---|
| Skor maksimum, semua fitur | 14 | 22 | 26 |
| Skor maksimum, 6 fitur inti (usia, tulang, longitudinal, transversal, densitas, margin) | 9 | 14 | 18 |
| Skor maksimum, usia + tulang + densitas | 5 | 7 | 9 |
| Jumlah klaim | 32 | 44 | 49 |
| Jumlah +3 | 0 | 5 | 10 |

- **Diuntungkan:** Ewing dan Osteoid osteoma (26); ABC, Fibrous dysplasia, Myeloma, Lymphoma (25). Pada 6 fitur inti: GCTB 18; CMF, NOF, SBC 17; ABC, Fibrous dysplasia 16.
- **Dirugikan:** BPOP (14), Clear cell CS dan Osteoblastoma (17), Desmoplastic fibroma, Parosteal OS, Paget, Periosteal chondroma (18). Skeletal TB tidak punya satu pun +3.
- Korelasi jumlah +3 dengan skor maksimum 0,63; prior dengan skor maksimum 0,68. Artinya entitas jarang sudah lebih rendah plafonnya sebelum prior dikurangkan.

**"Ciri khas" yang tidak khas.** Tujuh nilai diberi +3 oleh tujuh entitas atau lebih: `long_bone` (14), `10-19_open` dan `10-19_unknown` (13), `lytic` (11), `metaphysis` (9), `matrix:none` (8), `IA` (7). Hanya 14 nilai yang +3-nya dimiliki tepat satu entitas.

**Temuan negatif.** Skor dari `cortex:intact` + `periosteal:none` + `matrix:none` + `soft_tissue_mass:absent`:

| Tertinggi | Jumlah | Terendah | Jumlah |
|---|---|---|---|
| Enostosis, Geode/ganglion | +8 | Conventional OS | −6 |
| Bone infarct, Vertebral haemangioma | +7 | Telangiectatic OS | −4 |
| Brown tumour, Intraosseous lipoma, SBC | +6 | Periosteal OS | −3 |

Pemisahan jinak–agresif memang diinginkan. Masalahnya ada di dalam kelompok jinak: selisih +8 vs +3 (misalnya Enostosis vs Chondroblastoma) berasal dari tidak adanya temuan, bukan dari temuan yang spesifik.

**Prior tersembunyi.** Osteomyelitis, Skeletal TB, dan Stress fracture punya bobot usia ≥ +1 pada semua kelompok usia. Rata-rata bobot usia tertinggi: Osteomyelitis, Stress fracture, Conventional OS +1,7; Fibrous dysplasia +1,6; OFD–adamantinoma +1,4 (meski prior −2). Osteomyelitis punya 0 klaim −2 dan 3 klaim −5 (semuanya matriks).

**Penghitungan ganda.** `cortex:expansion_shell` + `periosteal:shell` memberi ABC +6 dan GCTB +4 untuk satu temuan; `SKEMA-DIAGNOSIS.md` §2 sendiri mengakui kedua nilai tumpang-tindih makna.

**Simulasi input jarang** (bobot seragam per kombinasi yang dapat diisi):

| Simulasi | Kombinasi | Paling sering di 3 besar | Jarang/tidak pernah | Seri di peringkat 1 (rata-rata) | Entitas berperingkat ≤5 (rata-rata) | Prior mengubah 3 besar |
|---|---|---|---|---|---|---|
| usia × tulang × densitas | 210 | Fibrous dysplasia 34%, Osteoid osteoma 34%, Stress fracture 27%, Enostosis 26%, Ewing 26%, Metastasis 26% | Clear cell CS, Periosteal OS, Periosteal chondroma 0%; Lymphoma 1 kombinasi | 1,66 | 6,76 | 73% |
| + longitudinal/transversal | 1274 | Stress fracture 44%, Osteoid osteoma 43%, Osteomyelitis 32%, Metastasis 24%, Osteochondroma 23% | Desmoplastic fibroma, Clear cell CS, Telangiectatic OS, Lymphoma, Intraosseous lipoma ≈1% | 1,43 | 6,05 | 56% |
| remaja 10–19, tulang panjang, litik, intrameduler/kortikal | 36 | **CMF 58%**, NOF 50%, ABC 50% | Conventional OS 0% di 3 besar | 1,44 | 6,03 | 53% |
| dewasa 20–59, tulang panjang, litik, intrameduler/kortikal | 24 | **GCTB 46%, CMF 42%**, Stress fracture 33% | — | 1,92 | 6,25 | 67% |

- CMF dan GCTB muncul persis seperti dugaan over-calling yang sudah tercatat. Pada kasus v1–v4, entitas yang paling sering menjadi peringkat 1 yang salah adalah Metastasis (17), GCTB (16), Ewing (13), CMF (9), SBC (7).
- Conventional OS tidak pernah masuk 3 besar pada subset remaja litik tulang panjang sebelum margin, korteks, periosteal, atau matriks diisi. Ini wajar secara logika, tetapi perlu disadari pengguna.
- Selisih peringkat 1 dan entitas ke-5 bermedian 2–3 poin, sama besar dengan prior maksimum (−2). Pada input jarang prior adalah penentu; pada input lengkap (rentang plafon 14–26) pengaruhnya kecil.
- Daftar "5 teratas + seri" melebihi 10 entitas pada 8 dari 210 dan 7 dari 1274 kombinasi.

### 3.3 Klaim hilang, tak terjangkau, dan mencurigakan

**(a) Klaim hilang dan asimetri.**

| Fitur | Rata-rata entitas dengan klaim per nilai (dari 37) |
|---|---|
| `age_group`, `density` | 37,0 |
| `transverse` / `longitudinal` | 33,2 / 32,8 |
| `margin_lodwick` / `matrix` / `periosteal` | 30,6 / 30,4 / 29,1 |
| `soft_tissue_mass` / `cortex` | 25,0 / 24,7 |
| `bone_class` | 15,7 |
| `size_cm` | 10,0 |
| `multiplicity` | 7,0 |
| `clinical_flags` | 1,7 |

- `multiplicity:solitary` hanya punya satu klaim (Metastasis 0). `multiple` menaikkan 13 entitas dan tidak menurunkan satu pun, padahal teks bantuan menyebut lesi multipel "mempersempit banding secara drastis". Myeloma mendapat +3 untuk `multiple` tetapi tidak dinilai untuk `solitary`.
- `night_pain_nsaid_relief` hanya untuk Osteoid osteoma (+3). Osteoblastoma dan abses Brodie tidak dinilai, dan tidak ada entitas yang turun.
- `fever_or_infection_signs` hanya untuk Osteomyelitis (+3) dan Skeletal TB (+2). Ewing, LCH, dan limfoma, yang juga dapat disertai demam, tidak dinilai, sehingga flag ini bekerja sebagai +3 murni untuk infeksi.
- `soft_tissue_mass:absent` dinilai pada 13 entitas; dari 12 entitas yang −5 pada `present`, hanya Stress fracture yang juga dinilai untuk `absent`.
- `periosteal:shell` dinilai pada 9 entitas; lesi ekspansil lain (SBC, Fibrous dysplasia, plasmasitoma) tidak.
- Metastasis tidak punya klaim untuk `endosteal_scalloping` (S-01 menyebut metastasis ginjal/tiroid) maupun `spine_posterior`.

**Kelas tulang batch 3 berperilaku buruk.** `clavicle`, `calcaneus`, `patella`, `craniofacial`, dan `sacrum` hanya punya klaim positif (2, 3, 1, 9, 12 entitas) dan tidak ada klaim negatif. Delapan entitas punya −5 pada sebagian kelas tulang tetapi tanpa klaim pada kelas lain yang sama mustahilnya. Contoh: Chordoma −5 pada `long_bone` dan `flat_bone`, tetapi tanpa klaim pada tangan/kaki, klavikula, kalkaneus, patela; pada V3-46 (BPOP jari kaki) Chordoma menjadi peringkat 1. Untuk lesi litik usia 20–39 di klavikula, kalkaneus, atau patela, GCTB berada di peringkat 1 (skor 6; seri dengan SBC di kalkaneus) hanya karena usia dan densitas.

**(b) Klaim tak terjangkau.** Hanya 4 klaim `longitudinal:not_applicable` (bobot 0) yang benar-benar mati. Yang terbuang pada presentasi khasnya: klaim margin Osteoid osteoma (`IA` +1; `IC/II/III` −5) dan Stress fracture, karena densitas terbaik keduanya `sclerotic` dan margin tidak dapat diisi untuk lesi sklerotik. Periosteal OS dan Periosteal chondroma masih punya klaim `endosteal_scalloping` (−2) yang diblokir bila transversalnya permukaan.

**(c) Kontradiksi internal.**

- `10-19_unknown` = nilai tertinggi di antara open/closed pada 10 dari 11 entitas yang membedakannya (mis. Chondroblastoma 3/1/**3**, SBC 3/1/**3**); hanya GCTB yang di tengah (−5/2/**1**). Teks bantuan menyebut nilai ini "netral terhadap status fisis".
- OFD–adamantinoma: pitfalls menyebut destruksi korteks dan komponen jaringan lunak mendukung adamantinoma, tetapi `cortex:destruction` = −2 dan `soft_tissue_mass:present` = 0. Bobot menggambarkan OFD, bukan ujung ganas spektrum.
- Stress fracture: pitfalls menyebut kalus agresif meniru osteosarkoma, tetapi `periosteal:spiculated` = −5 dan `soft_tissue_mass:present` = −5.
- Tidak ada aturan khusus yang memuat nilai yang sendiri −5.
- `SKEMA-DIAGNOSIS.md` §2 menulis `flat_bone` mencakup kalvaria, sedangkan `features.json` memisahkan `craniofacial`.

**(d) Bobot yang tampak keliru arah atau besarnya** (perlu penilaian pemilik).

- Conventional OS dan Ewing `periosteal:solid_thin` = −2, sedangkan S-01 menyebut reaksi tipis dapat dijumpai pada keduanya. V3-10 (osteosarkoma dengan reaksi solid) berperingkat 20.
- Conventional OS `60+` = +1 lebih tinggi daripada `40-59` = 0; S-15 meragukan puncak kedua usia lanjut.
- Bone infarct `density:lytic` = 0 dengan `cortex:intact` +3, `periosteal:none` +3, `central` +3, `metaphysis` +3, `long_bone` +3: lesi lusen sentral metafisis dewasa tanpa ciri apa pun memberi Bone infarct peringkat 1.
- Osteoblastoma `long_bone` = +1. Dalam konteks tulang panjang kortikal, Osteoblastoma paling banyak unggul 5 poin atas Osteoid osteoma atau Stress fracture.
- ABC `transverse:eccentric` +3 sesuai ajaran umum, tetapi S-01 mencantumkan ABC sebagai lesi sentral dan S-06 tidak menyebutnya. Ini masalah sumber, bukan arah.

**(e) Higiene data.** Tidak ada bobot di luar skala, tidak ada klaim tanpa `source_ids`, tidak ada id sumber tak terdaftar. 239 dari 1584 klaim punya `note_id`; 318 dari 322 hard constraint tidak, sehingga daftar "disingkirkan karena…" tidak dapat menampilkan alasan klinis.

### 3.4 Pasangan mimic

Diskriminator lengkap tiap pasangan ada di berkas keluaran. sep(A>B) = selisih skor maksimum A atas B tanpa menyingkirkan keduanya; sep_ctx = hal yang sama di dalam konteks kelompok dan tanpa flag klinis.

| Pasangan (konteks) | Diskriminator (nilai berselisih ≥2) | sep_ctx A>B / B>A | Catatan |
|---|---|---|---|
| GCTB vs Chondroblastoma (epifisis tulang panjang) | 23 | 16 / 13 | Terpisah baik lewat usia–fisis dan matriks |
| Clear cell CS vs Geode (epifisis) | 19 | 8 / 11 | Clear cell CS sulit unggul |
| Ewing vs Osteomyelitis (tulang panjang) | 22 | 12 / 22 | Asimetris |
| Conventional OS vs Osteomyelitis | 23 | 9 / 22 | Asimetris; lihat H-04 |
| Conventional OS vs Ewing | 12 | 16 / 16 | Seimbang |
| Ewing vs Lymphoma | 16 | 10 / 14 | Terutama usia |
| Enchondroma vs Bone infarct (sentral tulang panjang) | 16 | 9 / 13 | Infark menang pada vinyet enkondroma (19 vs 18) |
| Enchondroma vs Central CS | 26 | 15 / 20 | Terpisah baik |
| ABC vs SBC (tulang panjang litik) | 20 | 9 / 8 | Dekat |
| ABC vs GCTB | 15 | 8 / 14 | ABC sulit unggul di luar usia |
| NOF vs CMF | 18 | 10 / 12 | Seri pada vinyet NOF (22 vs 22) |
| Osteoid osteoma vs Osteoblastoma (kortikal) | 17 | 16 / 5 | Osteoblastoma sulit unggul |
| Osteoid osteoma vs Stress fracture | 13 | 9 / 11 | Seri pada vinyet stress fracture (19 vs 19); pemisahnya hanya ukuran dan nyeri malam |
| Parosteal OS vs BPOP (permukaan tulang panjang) | 13 | 9 / 9 | Pasangan terdekat (L1 = 42) |
| BPOP vs Periosteal chondroma | 13 | 8 / 11 | Dekat |
| Osteochondroma vs Parosteal OS | 17 | 11 / 9 | Parosteal menang 17 vs 16 pada vinyetnya |
| Metastasis vs Myeloma (korpus vertebra) | 15 | 8 / 7 | Hampir tak terpisah tanpa multiplisitas/riwayat; wajar secara klinis |
| Paget vs Vertebral haemangioma (korpus vertebra) | 18 | 5 / 11 | Paget kalah pada vinyetnya (11 vs 12) |
| Enostosis vs Metastasis (sklerotik) | 31 | 18 / 10 | Terpisah baik |
| Osteomyelitis vs Skeletal TB (korpus vertebra) | 11 | 12 / 8 | Hanya 1 pemisah keras; TB tanpa +3 |
| Chordoma vs Central CS (sakrum) | 21 | 11 / 12 | Cukup |
| Chordoma vs GCTB (sakrum) | 31 | 20 / 12 | Terpisah baik |

**Pasangan terdekat menurut data** (Lampiran C): Bone infarct–Intraosseous lipoma dan BPOP–Parosteal OS (L1 = 42; median semua pasangan 112), Metastasis–Myeloma dan Desmoplastic fibroma–GCTB (51), BPOP–Periosteal chondroma (52). Tidak ada pasangan yang sama sekali tidak dapat dibedakan: nilai terkecil dari max(sep) adalah 9 (Enostosis–Geode), dan 15 pasangan punya max(sep) ≤ 12. Entitas yang paling sering sulit dikalahkan pasangannya adalah Osteomyelitis, Stress fracture, Enostosis, dan Skeletal TB, yaitu entitas dengan sedikit bobot negatif.

**Vinyet buatan peninjau** (Lampiran D; bukan validasi). 48 vinyet dengan 8–12 fitur, minimal satu per entitas. Peringkat 1: 40 (36 tanpa seri); 3 besar: 47; tidak ada rujukan tersingkir. Dari 167 perbandingan A-vs-mimic, A tidak di atas B pada 7: Enchondroma vs Bone infarct, NOF vs CMF (seri), OFD anak vs NOF dan vs CMF, Ewing pelvis dewasa vs Lymphoma, Stress fracture vs Osteoid osteoma (seri), Paget vertebra vs hemangioma. Selisih kemenangan sering tipis: CMF 22 vs ABC 20, NOF 19, GCTB 18 pada vinyet CMF; Parosteal OS 17 vs Osteochondroma 16.

### 3.5 Uji petik sumber

**Pemusatan.**

| Ukuran | Nilai |
|---|---|
| Klaim yang hanya mengutip S-01 | 661 dari 1584 (41,7%) |
| Klaim yang mengutip S-01 (sendiri atau bersama) | 1573 (99,3%) |
| Entitas yang semua klaimnya hanya S-01 | 14 dari 37 |
| Hard constraint yang hanya mengutip S-01 | 134 dari 322 |
| +3 yang hanya mengutip S-01 | 56 dari 192 |
| Klaim `bone_class` aksial/kraniofasial yang hanya mengutip S-01 | 28 dari 58 |
| Sumber terdaftar yang tidak dipakai klaim mana pun | 15 dari 30 |

S-01 adalah review skeleton apendikular. Isinya berupa daftar lesi per lokasi, per tipe margin, per pola periosteal. S-01 tidak pernah menyatakan suatu kombinasi mustahil, dan tidak memuat gambaran radiografik Chordoma, Skeletal TB, atau Vertebral haemangioma; ketiganya hampir seluruhnya hanya mengutip S-01.

**Hasil 50 klaim** (tabel lengkap di berkas keluaran, bagian 5):

| Kelompok | n | Didukung | Sebagian (arah ya, kekuatan tidak) | Tidak ditemukan | Sumber menyatakan lain |
|---|---|---|---|---|---|
| Hard constraint (−5) | 21 | 2 | 7 | 9 | 3 |
| +3 | 22 | 17 | 3 | 1 | 1 |
| Lainnya | 7 | 3 | 0 | 2 | 2 |
| **Jumlah** | **50** | **22** | **10** | **12** | **6** |

Sampel sengaja memprioritaskan hard constraint yang sudah ditandai, jadi proporsi ini tidak mewakili seluruh KB. Polanya tetap jelas: klaim +3 umumnya didukung; kekuatan "hampir mustahil" hampir tidak pernah.

Enam klaim yang bertentangan dengan sumbernya sendiri:

| Klaim | Bobot | Sumber menyatakan |
|---|---|---|
| Telangiectatic OS `margin_lodwick:IA` | −5 | S-15: kadang berbatas tegas dengan tepi sklerotik ireguler |
| Chondroblastoma `soft_tissue_mass:present` | −5 | S-06: CT dapat menunjukkan perluasan ke jaringan lunak |
| Fibrous dysplasia `margin_lodwick:IC` | −5 | S-22: lesi kraniofasial biasanya tidak berbatas tegas |
| ABC `transverse:eccentric` | +3 | S-01: ABC dicantumkan sebagai lesi sentral |
| Conventional OS `periosteal:solid_thin` | −2 | S-01: reaksi tipis dapat dijumpai pada osteosarkoma dan Ewing |
| Conventional OS `age_group:60+` | +1 | S-15: puncak kedua usia lanjut diragukan data baru |

Temuan sumber lain: S-06 tidak punya bagian tentang CMF, padahal 44 dari 46 klaim CMF mengutip "S-01, S-06". S-04 hanya memuat pasien 3–18 tahun, jadi tidak dapat mendukung Ewing `60+` = −5; serinya (n = 28) mencatat Ewing metafisis 36% lebih sering daripada diafisis 21%, berlawanan dengan urutan bobot (diafisis +3, metafisis +1). S-19 hanya menggambarkan hemangioma kalvaria.

---

## 4. Daftar hipotesis v0.7

Urut menurut perkiraan dampak. "Usul uji" adalah nilai yang diuji pada set praktik, bukan rekomendasi untuk langsung diterapkan. Kolom terakhir: apakah butir ini terutama bergantung pada penilaian klinis pemilik.

| ID | Entitas | Fitur:nilai | Kini | Usul uji | Jenis | Bukti | Keyakinan | Penilaian pemilik |
|---|---|---|---|---|---|---|---|---|
| H-01 | Semua (terutama Enostosis, Geode, Bone infarct, Vertebral haemangioma, Fibrous dysplasia, lipoma) | `cortex:intact`, `periosteal:none`, `matrix:none` | 16 bobot +3 | Batasi pada +1 (paling tinggi +2); biarkan −2 pada entitas agresif | keseimbangan | Rentang −6…+8; Bone infarct menang pada vinyet C08 dan C27 | sedang | ya |
| H-02 | CMF | `transverse:eccentric`, `longitudinal:metadiaphysis`, `margin_lodwick:IA`, `age_group:10-19_open/unknown` | +3 semua | +2 semua (hipotesis tercatat, dirinci) | keseimbangan / mimic | 7 bobot +3 pada entitas prior −1; 58% 3 besar pada subset remaja litik; seri dengan NOF di vinyet C19; 9× peringkat 1 salah di v1–v4 | sedang | ya |
| H-03 | GCTB | `bone_class:long_bone`; `transverse:eccentric` | +3; +3 | +2; +2 (hipotesis tercatat, dirinci) | keseimbangan | Plafon 6 fitur inti tertinggi (18); 46% 3 besar pada subset dewasa litik; 16× peringkat 1 salah | sedang | ya |
| H-04 | Osteomyelitis, Skeletal TB, Stress fracture | `age_group` (semua nilai) | selalu ≥ +1 | Nilai usia yang tidak informatif menjadi 0; pertimbangkan satu-dua bobot −2 untuk Osteomyelitis | keseimbangan | Rata-rata bobot usia +1,7 / +1,3 / +1,7; Osteomyelitis 0 klaim −2; sep_ctx OS>OM 9 vs OM>OS 22 | rendah | ya (konteks endemik) |
| H-05 | Ewing, Lymphoma | aturan `*_soft_tissue_without_destruction` | `cortex ∈ {intact, focal_breach}` | Hanya `intact` | mimic | 15 penyalaan di v1–v4, semuanya `focal_breach`; 8 kali Ewing/limfoma peringkat 1 yang salah; S-01 menyebut "tanpa destruksi korteks berarti" | sedang | ya |
| H-06 | Metastasis | `age_group:10-19_*` | −5 ×3 | −2 | hard constraint (c) | `0-9` = −2; flag riwayat keganasan tidak dapat menolong | sedang | ya |
| H-07 | GCTB | `age_group:10-19_open` | −5 | −2 | hard constraint (b) | S-01 hanya menyatakan "biasanya"; S-16 tidak membahas | sedang | ya (aturan desain) |
| H-08 | Osteomyelitis; Central CS | `matrix:osteoid` | −5 | −2 | hard constraint (b) | Risiko salah baca sekuestrum/kalsifikasi padat; S-01 tidak mendukung | sedang | ya |
| H-09 | Chondroblastoma | `cortex:destruction`; `soft_tissue_mass:present`; `age_group:40-59` | −5 | −2 | hard constraint (b) | V3-06; S-06 menyebut perluasan jaringan lunak; KB memberi kalkaneus/patela +1 | sedang | ya |
| H-10 | SBC; NOF; Fibrous dysplasia | `periosteal:lamellated` | −5 | −2 (seperti CMF di v0.6) | hard constraint (c) | Definisi/pitfalls menyebut fraktur; S-22 | sedang | ya |
| H-11 | SBC | `age_group:60+`; `longitudinal:epiphysis_apophysis` | −5 | −2 | hard constraint (b) | V3-34; nilai mencakup apofisis (trokanter mayor) | sedang | ya |
| H-12 | Conventional OS; Telangiectatic OS | `margin_lodwick:IA`; Conventional OS `periosteal:shell` | −5 | −2 | hard constraint (b/c) | V3-09; S-15; `expansion_shell` sudah −2 | sedang | ya |
| H-13 | BPOP | `density:lytic`; `transverse:juxtacortical_continuous` | −5 | −2 | hard constraint (b) | V3-46; V2-15 | sedang | ya |
| H-14 | Geode/ganglion | `margin_lodwick:IC`; `soft_tissue_mass:present`; `size_cm:>5` | −5 | −2 | hard constraint (b) | V2-74 | sedang | ya |
| H-15 | Osteoid osteoma | `size_cm:>5` | −5 | −2, dan teks bantuan "ukur nidus" | hard constraint (c) | Densitas dinilai dari sklerosis, ukuran dari nidus | sedang | tidak |
| H-16 | Fibrous dysplasia | `margin_lodwick:IC` | −5 | −2 | hard constraint (b) | S-22 (kraniofasial tidak berbatas tegas); `craniofacial` +3 | sedang | ya |
| H-17 | Chordoma; Ewing | Chordoma `density:sclerotic`; Ewing `cortex:expansion_shell` | −5 | −2 | hard constraint (b) | Kordoma vertebra sklerotik dan Ewing ekspansil dilaporkan (dari ingatan literatur) | sedang | ya |
| H-18 | Brown tumour | `matrix:ground_glass` | −5 | −2 | hard constraint (b) | Deskriptor klasik tulang hiperparatiroid | sedang | ya |
| H-19 | Entitas yang soliter menurut sifatnya; Myeloma | `multiplicity:multiple`; `multiplicity:solitary` | tanpa klaim | −2 untuk `multiple` pada entitas soliter; Myeloma `solitary` 0 (eksplisit) | klaim hilang | 13 positif, 0 negatif | sedang | ya |
| H-20 | Osteoblastoma, Osteomyelitis; Ewing, LCH, Lymphoma | `night_pain_nsaid_relief`; `fever_or_infection_signs` | tanpa klaim | +1 | klaim hilang | Flag kini bekerja sebagai +3 murni untuk satu-dua entitas | rendah | ya |
| H-21 | ABC; GCTB | `periosteal:shell` | +3; +2 | +1; +1 | keseimbangan | Penghitungan ganda dengan `expansion_shell` (ABC +6, GCTB +4) | sedang | tidak |
| H-22 | 10 entitas (ABC, Chondroblastoma, CMF, Clear cell CS, Ewing, LCH, NOF, Osteochondroma, Osteomyelitis, SBC) | `age_group:10-19_unknown` | = nilai tertinggi open/closed | Nilai di antara open dan closed | konsistensi | Teks bantuan menyebut "netral" | tinggi | tidak |
| H-23 | Bone infarct | `density:lytic` | 0 | −2 | arah bobot | Vinyet C27: lesi lusen bertepi sklerotik memberi infark peringkat 1 | rendah | ya |
| H-24 | OFD–adamantinoma | `cortex:destruction`; `soft_tissue_mass:present` | −2; 0 | 0; +1 | kontradiksi internal | Pitfalls entitas sendiri | sedang | ya |
| H-25 | Conventional OS; Ewing | `periosteal:solid_thin` | −2 | 0 | arah bobot / sumber | S-01; V3-10 | rendah | ya |
| H-26 | CMF; Chordoma; Skeletal TB; Vertebral haemangioma (dan 10 entitas lain yang hanya S-01) | `source_ids` | S-06 / S-01 | Ganti atau tambah sumber terbuka yang benar-benar memuat entitas | sumber | S-06 tanpa CMF; S-01 tanpa ketiga entitas | tinggi | tidak |
| H-27 | Semua | `note_id` pada hard constraint | 4 dari 322 terisi | Isi alasan satu kalimat untuk setiap −5 | higiene data | 318 kosong | tinggi | tidak |
| H-28 | ABC | `transverse:eccentric` (sumber) | S-01, S-06 | Tambah sumber yang mendukung; bobot tetap | sumber | S-01 mencantumkan sentral | tinggi | tidak |
| H-29 | Chordoma (kini); 7 entitas lain saat batch 3 | `bone_class` tangan/kaki, klavikula, kalkaneus, patela | tanpa klaim | −5 untuk Chordoma; lengkapi eksklusi lain bersama batch 3 | klaim hilang | Chordoma peringkat 1 pada V3-46; GCTB peringkat 1 pada contoh klavikula/kalkaneus/patela | sedang | tidak |
| H-30 | Osteoblastoma; Skeletal TB; BPOP; Clear cell CS | bobot positif inti | plafon 17 / 21 / 14 / 17 | Tinjau apakah ada ciri yang layak +3 (mis. Osteoblastoma `long_bone` +1 → +2) | keseimbangan | Lampiran A | rendah | ya |
| H-31 | Semua | +3 pada `long_bone` (14 entitas), `10-19` (13), `lytic` (11), `metaphysis` (9), `IA` (7) | +3 | Batasi nilai lokasi/usia/densitas generik pada +2 kecuali benar-benar khas | keseimbangan | Tabel "ciri khas yang tidak khas" | rendah | ya |
| H-32 | Metastasis | `cortex:endosteal_scalloping`; `bone_class:spine_posterior` | tanpa klaim | +1; +1 | klaim hilang | S-01 (ginjal/tiroid); tanda pedikel | rendah | ya |
| H-33 | Conventional OS | `age_group:60+` | +1 | 0 (sama dengan `40-59`) | arah bobot / sumber | S-15 | rendah | ya |
| H-34 | — | `docs/SKEMA-DIAGNOSIS.md` §2 | `flat_bone` mencakup kalvaria | Samakan dengan `features.json` | higiene data | — | tinggi | tidak |

Catatan interaksi: H-02 dan H-03 harus diuji sebelum atau bersama pelonggaran hard constraint CMF (kelas b, keyakinan rendah di CSV), karena melonggarkan −5 CMF tanpa menurunkan bobot positifnya akan menambah over-calling. H-01 dan H-31 mengubah banyak bobot sekaligus; sebaiknya diuji terpisah dari hipotesis per entitas agar efeknya dapat dibaca.

### Memerlukan persetujuan pemilik — perubahan skema

Butir berikut adalah **opsi**, bukan rekomendasi untuk diterapkan.

- **S-1 Normalisasi skor.** Menampilkan skor sebagai proporsi dari maksimum yang dapat dicapai entitas pada fitur yang diisi. Menjawab rentang plafon 14–26, tetapi mengubah arti skor dan interaksi dengan prior.
- **S-2 Batas per fitur.** Batas atas kontribusi per fitur atau per kelompok fitur (misalnya temuan negatif), sebagai alternatif H-01 dan H-31 yang tidak perlu mengubah banyak bobot.
- **S-3 Eksklusi dua tingkat.** Memisahkan "eksklusi definisional" dari "penalti kuat" (misalnya −4 tanpa menyingkirkan), atau menyingkirkan hanya bila ada dua klaim −5. Menjawab risiko satu ketukan keliru (ground_glass, IC vs IB).
- **S-4 Status fisis tidak diketahui dihitung saat skor**, sebagai rata-rata open dan closed, alih-alih disimpan sebagai bobot tersendiri (alternatif H-22).
- **S-5 Aturan anti-hitung-ganda.** Jenis aturan yang menghitung `cortex:expansion_shell` dan `periosteal:shell` satu kali (alternatif H-21), atau menggabungkan kedua nilai di UI.
- **S-6 Kekuatan dukungan sumber per klaim.** Kolom yang membedakan "sumber mendukung arah" dari "sumber mendukung kekuatan", agar aturan "setiap klaim punya sumber yang mendukungnya" dapat diaudit.
- **S-7 Prior bergantung usia.** Memisahkan prevalensi per kelompok usia dari tipikalitas, agar bobot usia yang selalu positif tidak bekerja sebagai prior kedua (alternatif H-04).

Dua usulan non-bobot dari laporan v3/v4 (seri ditampilkan eksplisit; peringatan input jarang) dikuatkan oleh angka di 3.2 dan tidak memerlukan perubahan skema.

---

## 5. Lampiran

### Lampiran A — Keseimbangan per entitas

Urut menurut skor maksimum semua fitur. "fitur ber-+3" = jumlah fitur (dari 13) yang punya setidaknya satu nilai +3; "rata-rata bobot/nilai" = rata-rata atas 62 nilai (tanpa klaim = 0).

| Entitas | prior | klaim | +3 | fitur ber-+3 | +2 | +1 | 0 | -2 | -5 | rata-rata bobot/nilai | maks semua fitur | maks tanpa prior | maks 6 fitur inti | maks usia+tulang+densitas |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Ewing sarcoma | 0 | 47 | 8 | 5 | 8 | 12 | 2 | 11 | 6 | +0.00 | 26 | 26 | 15 | 7 |
| Osteoid osteoma | 0 | 43 | 10 | 8 | 2 | 11 | 6 | 2 | 12 | -0.31 | 26 | 26 | 15 | 9 |
| ABC | 0 | 44 | 9 | 8 | 4 | 8 | 8 | 10 | 5 | -0.03 | 25 | 25 | 16 | 9 |
| Fibrous dysplasia | 0 | 45 | 9 | 7 | 7 | 8 | 4 | 7 | 10 | -0.24 | 25 | 25 | 16 | 9 |
| Myeloma | 0 | 42 | 7 | 6 | 5 | 9 | 2 | 12 | 7 | -0.31 | 25 | 25 | 14 | 9 |
| Lymphoma | -1 | 46 | 5 | 4 | 10 | 11 | 8 | 4 | 8 | -0.03 | 25 | 26 | 13 | 6 |
| Bone infarct | 0 | 43 | 5 | 5 | 7 | 3 | 6 | 10 | 12 | -0.77 | 24 | 24 | 15 | 7 |
| Metastasis | 0 | 46 | 5 | 4 | 11 | 9 | 10 | 7 | 4 | +0.19 | 24 | 24 | 12 | 8 |
| CMF | -1 | 46 | 7 | 6 | 6 | 9 | 8 | 7 | 9 | -0.27 | 24 | 25 | 17 | 8 |
| Central CS | 0 | 49 | 4 | 4 | 11 | 12 | 8 | 11 | 3 | +0.15 | 24 | 24 | 14 | 8 |
| GCTB | 0 | 46 | 6 | 6 | 4 | 10 | 9 | 8 | 9 | -0.40 | 24 | 24 | 18 | 9 |
| Geode/ganglion | 0 | 45 | 5 | 5 | 5 | 4 | 5 | 6 | 20 | -1.34 | 24 | 24 | 14 | 7 |
| Osteomyelitis | 0 | 42 | 4 | 4 | 11 | 19 | 5 | 0 | 3 | +0.61 | 24 | 24 | 15 | 7 |
| Conventional OS | 0 | 46 | 7 | 4 | 9 | 10 | 5 | 12 | 3 | +0.16 | 24 | 24 | 14 | 7 |
| SBC | 0 | 44 | 9 | 6 | 4 | 4 | 3 | 5 | 19 | -1.06 | 24 | 24 | 17 | 9 |
| LCH | 0 | 44 | 5 | 5 | 9 | 15 | 6 | 5 | 4 | +0.29 | 23 | 23 | 15 | 9 |
| Telangiectatic OS | -1 | 42 | 6 | 4 | 6 | 13 | 4 | 6 | 7 | -0.06 | 23 | 24 | 14 | 8 |
| Enostosis | 0 | 43 | 3 | 3 | 10 | 9 | 3 | 5 | 13 | -0.60 | 22 | 22 | 11 | 7 |
| NOF | 0 | 45 | 9 | 5 | 4 | 6 | 4 | 8 | 14 | -0.73 | 22 | 22 | 17 | 8 |
| Periosteal OS | -2 | 38 | 7 | 5 | 7 | 5 | 5 | 8 | 6 | -0.10 | 21 | 23 | 12 | 6 |
| Skeletal TB | 0 | 45 | 0 | 0 | 12 | 18 | 5 | 6 | 4 | +0.16 | 21 | 21 | 11 | 6 |
| Chondroblastoma | -1 | 44 | 5 | 4 | 3 | 15 | 4 | 3 | 14 | -0.65 | 20 | 21 | 15 | 7 |
| Chordoma | -1 | 32 | 5 | 4 | 5 | 6 | 3 | 4 | 9 | -0.35 | 20 | 21 | 12 | 8 |
| Enchondroma | 0 | 48 | 2 | 2 | 9 | 13 | 4 | 12 | 8 | -0.44 | 20 | 20 | 11 | 7 |
| Osteochondroma | 0 | 38 | 6 | 4 | 5 | 9 | 3 | 5 | 10 | -0.37 | 20 | 20 | 14 | 8 |
| OFD-adamantinoma | -2 | 42 | 5 | 5 | 6 | 12 | 3 | 8 | 8 | -0.27 | 19 | 21 | 15 | 7 |
| Brown tumour | -1 | 46 | 3 | 3 | 6 | 15 | 7 | 5 | 10 | -0.39 | 19 | 20 | 9 | 6 |
| Intraosseous lipoma | -1 | 41 | 4 | 4 | 5 | 6 | 8 | 8 | 10 | -0.61 | 19 | 20 | 13 | 7 |
| Stress fracture | 0 | 44 | 3 | 3 | 12 | 11 | 7 | 3 | 8 | -0.03 | 19 | 19 | 12 | 7 |
| Vertebral haemangioma | 0 | 32 | 3 | 3 | 6 | 7 | 1 | 10 | 5 | -0.27 | 19 | 19 | 10 | 7 |
| Desmoplastic fibroma | -2 | 43 | 3 | 3 | 11 | 9 | 7 | 5 | 8 | -0.16 | 18 | 20 | 12 | 6 |
| Parosteal OS | -2 | 36 | 5 | 5 | 1 | 9 | 3 | 10 | 8 | -0.55 | 18 | 20 | 12 | 6 |
| Paget | -1 | 44 | 4 | 3 | 8 | 11 | 1 | 8 | 12 | -0.60 | 18 | 19 | 12 | 8 |
| Periosteal chondroma | -2 | 43 | 4 | 4 | 7 | 13 | 1 | 9 | 9 | -0.39 | 18 | 20 | 10 | 5 |
| Clear cell CS | -2 | 40 | 3 | 3 | 4 | 11 | 3 | 8 | 11 | -0.69 | 17 | 19 | 12 | 6 |
| Osteoblastoma | -1 | 40 | 4 | 2 | 6 | 17 | 3 | 6 | 4 | +0.15 | 17 | 18 | 10 | 7 |
| BPOP | -2 | 36 | 3 | 3 | 2 | 13 | 5 | 3 | 10 | -0.48 | 14 | 16 | 9 | 6 |

### Lampiran B — Nilai fitur yang menyingkirkan paling banyak entitas

Nilai dengan ≥ 9 entitas berbobot −5. Daftar semua nilai ada di berkas keluaran, bagian 1.

| Fitur:nilai | Entitas disingkirkan | % dari 37 | juga -2 | positif (>=1) |
|---|---|---|---|---|
| `matrix:ground_glass` | 27 | 73% | 7 | 2 |
| `periosteal:spiculated` | 20 | 54% | 7 | 4 |
| `matrix:chondroid` | 20 | 54% | 4 | 8 |
| `margin_lodwick:III` | 18 | 49% | 2 | 8 |
| `transverse:juxtacortical_continuous` | 18 | 49% | 8 | 2 |
| `matrix:osteoid` | 17 | 46% | 11 | 7 |
| `periosteal:codman` | 17 | 46% | 10 | 5 |
| `margin_lodwick:II` | 16 | 43% | 4 | 11 |
| `cortex:destruction` | 16 | 43% | 8 | 11 |
| `transverse:juxtacortical_surface` | 14 | 38% | 8 | 6 |
| `soft_tissue_mass:present` | 12 | 32% | 5 | 13 |
| `periosteal:lamellated` | 12 | 32% | 7 | 9 |
| `age_group:60+` | 9 | 24% | 10 | 18 |
| `density:sclerotic` | 9 | 24% | 8 | 17 |
| `transverse:cortical` | 9 | 24% | 13 | 9 |
| `margin_lodwick:IC` | 9 | 24% | 5 | 14 |

### Lampiran C — Pasangan entitas terdekat

L1 = jumlah selisih mutlak bobot atas 62 nilai; diskriminator = nilai dengan selisih ≥ 2; pemisah keras = nilai yang −5 hanya pada salah satu; sep(A>B) = selisih skor maksimum A atas B tanpa menyingkirkan keduanya (semua fitur, termasuk flag klinis).

| A | B | L1 | diskriminator | pemisah keras | sep(A>B) | sep(B>A) |
|---|---|---|---|---|---|---|
| Bone infarct | Intraosseous lipoma | 42 | 12 | 2 | 14 | 14 |
| BPOP | Parosteal OS | 42 | 13 | 4 | 10 | 9 |
| Metastasis | Myeloma | 51 | 15 | 3 | 14 | 8 |
| Desmoplastic fibroma | GCTB | 51 | 14 | 5 | 8 | 12 |
| BPOP | Periosteal chondroma | 52 | 13 | 5 | 9 | 11 |
| Brown tumour | Desmoplastic fibroma | 54 | 16 | 4 | 15 | 11 |
| LCH | Osteomyelitis | 54 | 15 | 1 | 10 | 18 |
| Osteomyelitis | Skeletal TB | 54 | 11 | 1 | 16 | 8 |
| Enchondroma | Intraosseous lipoma | 55 | 14 | 4 | 16 | 12 |
| ABC | LCH | 56 | 16 | 1 | 12 | 21 |
| Ewing sarcoma | Conventional OS | 56 | 12 | 3 | 16 | 16 |
| Conventional OS | Telangiectatic OS | 56 | 18 | 6 | 12 | 12 |
| Bone infarct | Enchondroma | 57 | 16 | 6 | 13 | 17 |
| Fibrous dysplasia | Intraosseous lipoma | 57 | 18 | 0 | 20 | 12 |
| ABC | Desmoplastic fibroma | 58 | 17 | 5 | 13 | 13 |
| Desmoplastic fibroma | LCH | 58 | 14 | 6 | 5 | 17 |
| Enchondroma | Fibrous dysplasia | 58 | 18 | 4 | 12 | 18 |
| Ewing sarcoma | Lymphoma | 58 | 16 | 4 | 10 | 14 |
| LCH | Skeletal TB | 58 | 13 | 2 | 16 | 13 |
| Metastasis | Chordoma | 60 | 16 | 5 | 16 | 9 |
| Brown tumour | Intraosseous lipoma | 60 | 16 | 6 | 18 | 10 |
| Desmoplastic fibroma | Skeletal TB | 60 | 13 | 4 | 8 | 19 |
| ABC | Osteoblastoma | 61 | 16 | 5 | 18 | 14 |
| Bone infarct | Fibrous dysplasia | 61 | 16 | 2 | 10 | 19 |
| CMF | Fibrous dysplasia | 62 | 17 | 5 | 13 | 19 |

### Lampiran D — Vinyet buatan peninjau dan peringkatnya

**Bukan kasus validasi.** Ditulis peninjau dari pengetahuan umum; kode fiturnya ada di `tools/review_scoring.py` (`VIGNETTES`). "seri" = jumlah entitas yang berskor sama dengan entitas yang diharapkan; "disingkirkan" = jumlah entitas yang terkena hard constraint.

| ID | Entitas diharapkan | fitur | peringkat | seri | selisih vs pesaing terbaik | 4 teratas | disingkirkan | Deskripsi |
|---|---|---|---|---|---|---|---|---|
| C01 | Conventional OS | 12 | 1 | 1 | 4 | Conventional OS 23; Telangiectatic OS 19; Ewing sarcoma 15 | 34 | 14 th, femur distal metafisis, campuran moth-eaten, destruksi, massa, Codman, osteoid |
| C02 | Telangiectatic OS | 12 | 1 | 1 | 6 | Telangiectatic OS 22; ABC 16; Conventional OS 16; GCTB 14 | 26 | 16 th, tibia proksimal metafisis, litik ekspansil tepi tidak tegas, massa, Codman |
| C03 | Parosteal OS | 10 | 1 | 1 | 1 | Parosteal OS 17; Osteochondroma 16; BPOP 10; Osteoblastoma 9 | 25 | 32 th, femur distal posterior, massa permukaan padat terosifikasi, korteks utuh |
| C04 | Periosteal OS | 11 | 1 | 1 | 11 | Periosteal OS 21; Conventional OS 10; Central CS 8; BPOP 2 | 32 | 17 th, tibia diafisis, massa permukaan, saucerization, spikula tegak lurus |
| C05 | Osteoid osteoma | 12 | 1 | 1 | 6 | Osteoid osteoma 25; Stress fracture 19; OFD-adamantinoma 14; Osteomyelitis 12 | 15 | 22 th, femur diafisis, sklerosis kortikal, periosteal solid, nidus <2 cm, nyeri malam |
| C06 | Osteoblastoma | 10 | 1 | 1 | 4 | Osteoblastoma 16; Fibrous dysplasia 12; Osteochondroma 7; OFD-adamantinoma 6 | 26 | 18 th, elemen posterior vertebra, ekspansil campuran dengan osteoid, 3 cm |
| C07 | Osteochondroma | 11 | 1 | 1 | 5 | Osteochondroma 19; Stress fracture 14; NOF 13; Osteoid osteoma 11 | 23 | 12 th, femur distal metafisis, eksostosis dengan kontinuitas korteks-meduler |
| C08 | Enchondroma | 12 | 2 | 1 | -1 | Bone infarct 19; Enchondroma 18; Fibrous dysplasia 15; Central CS 13 | 27 | 45 th, humerus proksimal metafisis, sentral, kalsifikasi ring-and-arc, tanpa scalloping |
| C09 | Enchondroma | 11 | 1 | 1 | 5 | Enchondroma 17; Fibrous dysplasia 12; Clear cell CS 10; CMF 9 | 27 | 30 th, falang proksimal, litik sentral ekspansil dengan kalsifikasi kondroid |
| C10 | Periosteal chondroma | 11 | 1 | 1 | 10 | Periosteal chondroma 18; CMF 8; Central CS 7; Periosteal OS 7 | 29 | 25 th, humerus proksimal, lesi permukaan dengan saucerization dan penyangga, kalsifikasi kondroid |
| C11 | Chondroblastoma | 12 | 1 | 1 | 4 | Chondroblastoma 20; CMF 16; Fibrous dysplasia 11; Enchondroma 9 | 30 | 15 th fisis terbuka, epifisis tibia proksimal, litik eksentrik tepi sklerotik, kalsifikasi halus |
| C12 | CMF | 12 | 1 | 1 | 2 | CMF 22; ABC 20; NOF 19; GCTB 18 | 13 | 22 th, tibia proksimal metafisis, litik eksentrik berlobus tepi sklerotik, ekspansi |
| C13 | Central CS | 12 | 1 | 1 | 10 | Central CS 21; Clear cell CS 11; Enchondroma 11; Metastasis 10 | 32 | 58 th, femur proksimal metadiafisis, sentral, scalloping dalam, kondroid, >5 cm |
| C14 | Central CS | 11 | 1 | 1 | 10 | Central CS 22; Metastasis 12; Conventional OS 8; Clear cell CS 3 | 33 | 55 th, ilium, campuran dengan kalsifikasi kondroid, destruksi korteks, massa besar |
| C15 | Clear cell CS | 12 | 1 | 1 | 2 | Clear cell CS 16; Chondroblastoma 14; Enchondroma 13; Bone infarct 11 | 27 | 38 th, kaput femur, litik berbatas tegas tanpa tepi sklerotik, kalsifikasi |
| C16 | Desmoplastic fibroma | 12 | 3 | 2 | -3 | SBC 21; ABC 19; Desmoplastic fibroma 18; GCTB 18 | 13 | 24 th, femur distal metafisis, litik sentral ekspansil dengan pseudotrabekulasi, tanpa matriks |
| C17 | Vertebral haemangioma | 10 | 1 | 1 | 4 | Vertebral haemangioma 17; Paget 13; Bone infarct 11; Fibrous dysplasia 10 | 11 | 50 th, korpus vertebra, trabekula vertikal kasar, korteks utuh |
| C18 | ABC | 12 | 1 | 1 | 7 | ABC 25; CMF 18; NOF 18; SBC 17 | 19 | 13 th fisis terbuka, femur distal metafisis, litik eksentrik blow-out dengan cangkang tipis |
| C19 | NOF | 12 | 1 | 2 | 0 | CMF 22; NOF 22; ABC 19; SBC 18 | 16 | 11 th fisis terbuka, tibia distal metafisis, litik eksentrik tepi sklerotik berlobus |
| C20 | GCTB | 12 | 1 | 1 | 7 | GCTB 23; ABC 16; Clear cell CS 16; Brown tumour 14 | 16 | 30 th, radius distal epi-metafisis sampai subkondral, litik eksentrik tanpa tepi sklerotik |
| C21 | Chordoma | 11 | 1 | 1 | 3 | Chordoma 20; Metastasis 17; Central CS 16; Myeloma 16 | 22 | 62 th, sakrum garis tengah, litik destruktif dengan massa presakral besar |
| C22 | SBC | 12 | 1 | 1 | 4 | SBC 24; ABC 20; LCH 18; Fibrous dysplasia 17 | 18 | 9 th, humerus proksimal metafisis, litik sentral, korteks menipis |
| C23 | Fibrous dysplasia | 12 | 1 | 1 | 11 | Fibrous dysplasia 23; OFD-adamantinoma 12; CMF 12; NOF 11 | 28 | 20 th, femur proksimal metadiafisis, ground-glass dengan rind sklerotik, ekspansi |
| C24 | OFD-adamantinoma | 12 | 1 | 1 | 3 | OFD-adamantinoma 19; Fibrous dysplasia 16; NOF 15; CMF 14 | 17 | 28 th, tibia diafisis anterior, kortikal, multilokuler campuran, ekspansi |
| C25 | OFD-adamantinoma | 12 | 4 | 1 | -3 | NOF 19; CMF 17; LCH 17; OFD-adamantinoma 16 | 19 | 6 th (OFD), tibia diafisis anterior, kortikal, litik tepi sklerotik, bowing |
| C26 | Intraosseous lipoma | 11 | 1 | 1 | 2 | Intraosseous lipoma 18; Geode/ganglion 16; SBC 15; Bone infarct 14 | 11 | 48 th, kalkaneus, lusen tepi sklerotik tipis, korteks utuh |
| C27 | Intraosseous lipoma | 12 | 2 | 1 | -1 | Bone infarct 20; Intraosseous lipoma 19; Geode/ganglion 18; SBC 18 | 12 | 45 th, femur intertrokanter, lusen sentral tepi sklerotik |
| C28 | BPOP | 10 | 1 | 1 | 2 | BPOP 14; Osteoid osteoma 12; Parosteal OS 12; Osteochondroma 11 | 26 | 30 th, falang proksimal, massa termineralisasi menempel di permukaan, korteks utuh, tanpa kontinuitas |
| C29 | Myeloma | 10 | 1 | 1 | 6 | Myeloma 24; Brown tumour 18; Metastasis 16; Paget 14 | 16 | 66 th, pelvis, lesi litik punched-out multipel dengan scalloping |
| C30 | Myeloma | 9 | 1 | 1 | 4 | Myeloma 18; Chordoma 14; Metastasis 13; GCTB 13 | 19 | 55 th, plasmasitoma soliter korpus vertebra, litik ekspansil dengan massa |
| C31 | Lymphoma | 12 | 1 | 1 | 4 | Lymphoma 23; Ewing sarcoma 19; Metastasis 15; Central CS 15 | 25 | 50 th, femur metadiafisis, permeatif, korteks relatif utuh, massa besar, lamelar |
| C32 | LCH | 12 | 1 | 1 | 6 | LCH 21; Osteomyelitis 15; Desmoplastic fibroma 12; ABC 11 | 22 | 6 th, femur diafisis, litik sentral berbatas tegas, scalloping, periosteal lamelar |
| C33 | Ewing sarcoma | 12 | 1 | 1 | 6 | Ewing sarcoma 26; LCH 20; Lymphoma 20; Telangiectatic OS 18 | 27 | 12 th, femur diafisis, moth-eaten, korteks terputus fokal, massa besar, onion-skin |
| C34 | Ewing sarcoma | 11 | 2 | 1 | -2 | Lymphoma 19; Ewing sarcoma 17; Central CS 15; LCH 13 | 25 | 24 th, ilium, permeatif dengan massa jaringan lunak besar |
| C35 | Metastasis | 12 | 1 | 1 | 2 | Metastasis 24; Lymphoma 22; Myeloma 20; Central CS 15 | 26 | 66 th, riwayat karsinoma, femur proksimal, litik moth-eaten destruktif, lesi multipel |
| C36 | Metastasis | 10 | 1 | 1 | 2 | Metastasis 18; Enostosis 16; Paget 15; Bone infarct 14 | 20 | 70 th, riwayat karsinoma prostat, pelvis, fokus sklerotik multipel |
| C37 | Osteomyelitis | 12 | 1 | 1 | 2 | Osteomyelitis 21; LCH 19; Ewing sarcoma 15; Telangiectatic OS 15 | 23 | 7 th, demam, tibia proksimal metafisis, litik tidak tegas, periosteal lamelar |
| C38 | Osteomyelitis | 12 | 2 | 1 | -2 | SBC 21; Osteomyelitis 19; CMF 17; ABC 16 | 17 | 14 th (abses Brodie), tibia distal metafisis, litik lonjong tepi sklerotik tebal, periosteal solid |
| C39 | Skeletal TB | 10 | 1 | 1 | 2 | Skeletal TB 17; Chordoma 15; LCH 13; Osteomyelitis 13 | 18 | 30 th, korpus vertebra, destruksi litik dengan massa paravertebral, demam subfebris |
| C40 | Skeletal TB | 12 | 1 | 2 | 0 | LCH 14; Skeletal TB 14; ABC 12; Osteomyelitis 12 | 24 | 8 th, femur distal epi-metafisis melintasi fisis, litik dengan penembusan korteks |
| C41 | Geode/ganglion | 12 | 1 | 1 | 8 | Geode/ganglion 24; Clear cell CS 16; GCTB 16; CMF 14 | 15 | 55 th, subkondral tibia proksimal, kista kecil tepi sklerotik |
| C42 | Bone infarct | 11 | 1 | 1 | 4 | Bone infarct 23; Fibrous dysplasia 19; Intraosseous lipoma 17; Enchondroma 16 | 13 | 52 th, femur distal metadiafisis, sentral, sklerosis serpiginosa, multipel |
| C43 | Stress fracture | 10 | 1 | 2 | 0 | Osteoid osteoma 19; Stress fracture 19; OFD-adamantinoma 14; Osteomyelitis 12 | 15 | 22 th pelari, tibia diafisis, sklerosis kortikal dengan periosteal solid |
| C44 | Stress fracture | 8 | 2 | 2 | -3 | Enostosis 14; Bone infarct 11; Stress fracture 11; Metastasis 10 | 15 | 72 th (insufisiensi), sakrum, pita sklerotik |
| C45 | Paget | 12 | 1 | 1 | 3 | Paget 16; Clear cell CS 13; Central CS 12; Skeletal TB 11 | 20 | 70 th, tibia proksimal mulai subartikular, campuran, trabekula kasar, tulang membesar |
| C46 | Paget | 8 | 2 | 1 | -1 | Vertebral haemangioma 12; Paget 11; Metastasis 7; Myeloma 5 | 23 | 68 th, korpus vertebra, sklerotik membesar dengan trabekula kasar |
| C47 | Brown tumour | 12 | 1 | 2 | 0 | Brown tumour 19; Myeloma 19; GCTB 16; ABC 15 | 14 | 45 th, lesi litik ekspansil multipel tulang panjang, tanpa matriks |
| C48 | Enostosis | 11 | 1 | 1 | 1 | Enostosis 21; Bone infarct 20; Stress fracture 14; Metastasis 13 | 14 | 40 th, femur proksimal metafisis, fokus sklerotik homogen <2 cm |

---

*Berkas terkait:* `tools/review_scoring.py` (skrip analisis, baca-saja), `tools/review_cases_v1_v4.txt` (transkripsi fitur kasus v1–v4), `docs/tinjauan-skor-v0.6-keluaran.txt` (keluaran lengkap skrip), `docs/tinjauan-skor-v0.6-hard-constraints.csv` (klasifikasi 322 hard constraint). Menjalankan ulang: `python3 tools/review_scoring.py > docs/tinjauan-skor-v0.6-keluaran.txt` (± 2 menit).

