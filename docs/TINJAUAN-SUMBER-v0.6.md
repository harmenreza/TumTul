# Tinjauan Sumber Basis Pengetahuan TumTul v0.6.0 (teks lengkap)

**Tanggal:** 2026-11-22 · **Objek:** `data/entities/*.json`, `data/sources.json` (KB 0.6.0) · **Status:** pemeriksaan sumber; **tidak ada bobot, entitas, fitur, sumber, atau skema yang diubah**.

Tinjauan ini mengulang "uji petik sumber" pada `docs/TINJAUAN-SKOR-v0.6.md` §3.5, kali ini dengan membaca teks lengkap setiap sumber. Semua angka berasal dari `tools/review_sources.py`; keluaran lengkapnya ada di `docs/tinjauan-sumber-v0.6-keluaran.txt`, vonis per klaim di `docs/tinjauan-sumber-v0.6.csv`, dan temuan mentah per klaim per sumber di `tools/review_source_evidence.tsv`.

**Yang dijawab tinjauan ini:** apakah sumber yang DIKUTIP sebuah klaim memang mendukung klaim itu. **Yang tidak dijawab:** apakah klaim itu benar secara klinis. Vonis "tidak ditemukan" berarti sumbernya salah atau kurang, bukan bahwa bobotnya salah.

---

## 1. Ringkasan

1. **Satu-satunya sampel tak bias (set D, 40 klaim acak dari sisa KB): 9 didukung (22%), 11 sebagian (28%), 20 tidak ditemukan (50%), 0 bertentangan.** Dengan n = 40, selang 95% untuk "didukung" adalah 12%–38% dan untuk "tidak ditemukan" 35%–65%. Set A–C sengaja bias dan tidak boleh dipakai sebagai perkiraan untuk seluruh KB.
2. **Klaim +3 (set B, 192): 107 didukung (56%), 51 sebagian, 34 tidak ditemukan, 0 bertentangan.** Dari 34 yang tidak ditemukan, 27 hanya mengutip S-01. Bila keanggotaan daftar di S-01 dianggap cukup untuk +3, 24 klaim "sebagian" naik menjadi "didukung" (131 dari 192).
3. **Hard constraint yang sudah ditandai (set A, 73): 3 didukung, 28 sebagian, 39 tidak ditemukan, 3 bertentangan.** Kekuatan "hampir mustahil" hampir tidak pernah dinyatakan sumber; yang ada paling jauh "biasanya" untuk nilai sebaliknya.
4. **Tiga klaim bertentangan dengan sumbernya sendiri, ketiganya terkonfirmasi pada teks lengkap:** Chondroblastoma `soft_tissue_mass:present` −5 (S-06), Fibrous dysplasia `margin_lodwick:IC` −5 (S-22), Telangiectatic osteosarcoma `margin_lodwick:IA` −5 (S-15). Empat klaim lain memuat konflik dengan satu sumber tetapi didukung (penuh atau sebagian) oleh sumber lain.
5. **Masalah utamanya adalah sumber, bukan isi.** Klaim yang hanya mengutip S-01 jauh lebih jarang didukung: pada set B 11 dari 56 didukung, dibanding 96 dari 136 bila ada sumber kedua; pada set D 0 dari 15 dibanding 9 dari 25. S-01 diam pada 54% klaim A–D yang mengutipnya.
6. **Tiga entitas tidak punya sumber radiografik sama sekali** (Chordoma, Desmoplastic fibroma of bone, Skeletal tuberculosis: S-01 hanya menyebut namanya). **Dua hanya punya data lokasi** (Vertebral haemangioma, Periosteal osteosarcoma). **Tiga hanya muncul di daftar S-01** (Brown tumour, Geode, Intraosseous lipoma).
7. **Beberapa sumber kedua tidak memuat gambaran radiografik entitasnya:** S-06 untuk Chondromyxoid fibroma (44 klaim), S-24 untuk myeloma (41 klaim; ulasan MRI), S-15 untuk Periosteal osteosarcoma (37 klaim), S-04 untuk Ewing sarcoma (46) dan Osteochondroma (33) yang hanya memuat usia dan lokasi. Jumlahnya 208 kutipan klaim.
8. **S-18 (kini terbaca) memuat bagian tersendiri tentang Chondromyxoid fibroma**, tetapi hanya 1 dari 46 klaim CMF yang mengutipnya. Mengganti S-06 dengan S-18 pada klaim CMF adalah perbaikan sumber termurah di KB ini.
9. **Terhadap uji petik lama:** 46 dari 50 butir dinilai ulang; 31 sama, 15 berubah (8 lebih mendukung, 7 kurang). Dari 6 "bertentangan" lama, 3 bertahan, 2 menjadi "sebagian", 1 menjadi "tidak ditemukan".

---

## 2. Metode dan batasan

**Sumber yang dibaca teks lengkapnya.** Empat belas artikel diambil dari PubMed/PubMed Central (konektor PubMed, teks lengkap PMC), satu per satu, dan dibaca seluruhnya termasuk tabel dan keterangan gambar:

| Kode | Artikel | DOI |
|---|---|---|
| S-01 | Matcuk dkk. 2025, radiografi konvensional lesi tulang fokal | [10.1007/s00256-024-04854-6](https://doi.org/10.1007/s00256-024-04854-6) |
| S-04 | Breden dkk. 2024, tumor tulang pediatrik 420 kasus | [10.3390/diagnostics14222513](https://doi.org/10.3390/diagnostics14222513) |
| S-05 | Yang dkk. 2024, tren kanker tulang primer (SEER) | [10.1016/j.jbo.2024.100607](https://doi.org/10.1016/j.jbo.2024.100607) |
| S-06 | De Salvo dkk. 2022, tumor tulang jinak | [10.3390/jcm11030699](https://doi.org/10.3390/jcm11030699) |
| S-10 | Erhardt dkk. 2019, akurasi radiograf polos | [10.4102/sajr.v23i1.1768](https://doi.org/10.4102/sajr.v23i1.1768) |
| S-15 | Cè dkk. 2025, pencitraan osteosarkoma | [10.3390/cancers17040599](https://doi.org/10.3390/cancers17040599) |
| S-16 | Parmeggiani dkk. 2021, giant cell tumour of bone | [10.3390/cancers13246298](https://doi.org/10.3390/cancers13246298) |
| S-19 | Pons Escoda dkk. 2020, tumor kalvaria dewasa | [10.1186/s13244-019-0820-9](https://doi.org/10.1186/s13244-019-0820-9) |
| S-20 | Liu dkk. 2020, osteoblastoma spinal | [10.1186/s13244-020-00934-y](https://doi.org/10.1186/s13244-020-00934-y) |
| S-22 | Kushchayeva dkk. 2018, fibrous dysplasia | [10.1007/s13244-018-0666-6](https://doi.org/10.1007/s13244-018-0666-6) |
| S-23 | Khung dkk. 2013, Langerhans cell histiocytosis | [10.1007/s13244-013-0271-7](https://doi.org/10.1007/s13244-013-0271-7) |
| S-24 | Dutoit & Verstraete 2016, MRI multiple myeloma | [10.1007/s13244-016-0492-7](https://doi.org/10.1007/s13244-016-0492-7) |
| S-25 | Chaturvedi dkk. 2016, lesi permukaan tulang pada anak | [10.1007/s13244-016-0527-0](https://doi.org/10.1007/s13244-016-0527-0) |
| S-26 | Rueda-de-Eusebio dkk. 2025, hereditary multiple exostoses | [10.1186/s13244-025-01899-6](https://doi.org/10.1186/s13244-025-01899-6) |

**S-18** (Gómez-León dkk. 2023, tumor kondroid; [10.1067/j.cpradiol.2023.01.005](https://doi.org/10.1067/j.cpradiol.2023.01.005)) tidak ada di PMC. Sumber ini dibaca seluruhnya dari PDF yang diberikan pemilik (teks hasil ekstraksi, 15 halaman), bukan dari PubMed.

**Tidak dapat dibaca:** S-21 (tumor klavikula). Hanya 1 klaim di seluruh KB yang mengutipnya dan klaim itu tidak termasuk set mana pun, jadi tidak ada vonis "sumber tidak dapat diakses" dalam hasil.

**Klaim yang diperiksa (312 klaim unik, 19,7% dari 1584 bobot fitur; 520 baris bukti, ditambah 6 baris untuk aturan).**

- **Set A** — 73 hard constraint (−5) yang pada tinjauan pertama berkelas b atau c.
- **Set B** — seluruh 192 klaim +3.
- **Set C** — 18 butir uji petik lama yang hasilnya "tidak ditemukan" atau "bertentangan" (9 ada di A, 2 di B, 7 di luar keduanya).
- **Set D** — 40 klaim yang diambil acak dengan benih tetap (20261121) dari 1308 klaim di luar A, B, C (bobot +2, +1, 0, −2, dan −5 kelas a). **Hanya set D yang tak bias.**
- **Set R** — 5 aturan (`rules[]`), diperiksa sebagai tambahan dan dilaporkan terpisah di §9.

**Cara kerja.** Sumber dibaca satu per satu. Untuk setiap klaim dan setiap sumber yang dikutipnya dicatat satu temuan (mendukung / sebagian / diam / konflik), lokasi di sumber (judul bagian, tabel, atau gambar), dan catatan singkat dengan kata-kata sendiri. Skrip menolak baris yang tidak cocok dengan klaim, bobot, atau sumber yang dikutip, lalu menggabungkan: temuan terbaik di antara sumber yang dikutip menentukan vonis; konflik selalu dilaporkan dan menjadi vonis "bertentangan" hanya bila tidak ada sumber lain yang mendukung.

**Aturan penilaian (ketat, diterapkan seragam).**

- *Didukung* hanya bila sumber menyatakan temuan itu untuk entitas tersebut dengan kekuatan yang sesuai: untuk +3 kata seperti khas, klasik, predileksi, terutama, atau angka mayoritas; untuk −5 pernyataan atau definisi yang menyingkirkan.
- *Sebagian* bila arahnya didukung tetapi kekuatannya tidak. Tiga pola utama: (a) entitas hanya tercantum dalam daftar banding S-01 untuk nilai itu, tanpa kata penanda kekhasan; (b) untuk bobot negatif, sumber menyebut nilai lain sebagai yang lazim atau khas; (c) untuk usia, puncak atau rentang yang disebut sumber berada jauh dari kelompok yang diklaim.
- *Tidak ditemukan* bila sumber tidak mengatakan apa pun yang dapat dipakai. Ketiadaan penyebutan tidak pernah dihitung sebagai dukungan. Untuk bobot negatif, tercantum di daftar nilai LAIN tidak dihitung sebagai arah, karena daftar S-01 tidak saling menyingkirkan.
- Pernyataan tingkat kelompok ("tumor jinak memuncak pada dua dekade pertama", "osteosarkoma" untuk subtipenya) tidak dihitung untuk entitas yang tidak disebut namanya, atau diturunkan satu tingkat untuk subtipe.
- Bila ragu di antara dua vonis, dipilih yang lebih rendah dan alasannya ditulis di catatan.

**Seberapa besar pengaruh aturan ketat ini** (dihitung skrip dari penanda di catatan):

| Pelonggaran | Set A | Set B | Set D |
|---|---|---|---|
| Keanggotaan daftar dianggap cukup untuk +3/+2: "sebagian" → "didukung" | 0 | 24 (107 → 131) | 1 (9 → 10) |
| Tercantum pada nilai lain dianggap memberi arah untuk bobot negatif: "tidak ditemukan" → "sebagian" | 7 (28 → 35) | 0 | 1 (11 → 12) |
| Pernyataan tingkat kelompok dianggap memberi arah: "tidak ditemukan" → "sebagian" | 0 | 2 | 1 |

**Batasan.**

- Penilai tunggal (model AI). Tidak ada penilai kedua; batas antara "didukung" dan "sebagian" bergantung pada pembacaan kata penanda kekhasan.
- Konektor PubMed memberi teks, tabel, dan keterangan gambar, **bukan isi gambarnya**. S-01 Fig. 1 dan Fig. 3 adalah ilustrasi predileksi tumor menurut tulang, lokasi, dan usia yang isinya tidak terbaca. Klaim usia atau lokasi yang mengutip S-01 dan kini "tidak ditemukan" (set A 5, set B 14, set D 6) atau "sebagian" (14, 25, 6) mungkin naik bila gambar itu diperiksa pemilik.
- S-18 dibaca dari teks hasil ekstraksi dua kolom; keterangan gambar terbaca, gambar tidak dilihat.
- Set D hanya 40 klaim; proporsinya bersifat kasar. Sebanyak 15 dari 40 hanya mengutip S-01 (38%; di seluruh KB 41,7%), jadi komposisinya mirip KB.
- Tingkat cakupan (§4) adalah penggolongan peninjau atas isi tiap sumber, bukan hitungan otomatis.

**Pemeriksaan ulang oleh sesi utama (2026-11-22).** Pemeriksaan sumber ini dikerjakan oleh satu agen terpisah (effort tinggi; sempat terhenti oleh batas pemakaian dan dilanjutkan dari berkas kerjanya). Sesi utama memeriksa hasilnya sebelum disimpan:

- Skrip dijalankan ulang dari awal; keluarannya identik dengan berkas keluaran. Tidak ada berkas di `data/` atau `schema/` yang berubah.
- Hitungan vonis per set dihitung ulang dari CSV dan cocok dengan tabel §3; seluruh 328 baris CSV cocok dengan klaim dan bobot di berkas entitas.
- 14 baris bukti S-06 yang diambil acak dibandingkan dengan teks lengkap S-06 yang dibaca sesi utama lewat PubMed/PMC: semuanya sesuai, termasuk vonis bertentangan untuk Chondroblastoma `soft_tissue_mass:present`, ukuran nidus osteoid osteoma, dan tipe eksentrik pada klasifikasi Capanna.
- Pada teks S-18: benar ada bagian tersendiri tentang Chondromyxoid fibroma (dewasa muda; lesi litik eksentrik metafisis bertepi sklerotik, sering ekspansil, tanpa reaksi periosteal, kalsifikasi matriks biasanya tidak ada), dan benar clear cell chondrosarcoma diuraikan sebagai lesi osteolitik epifisis.
- **Tidak diperiksa ulang:** vonis yang bersandar pada 12 sumber lainnya (termasuk S-01, S-15, S-22), jadi dua dari tiga vonis bertentangan (Fibrous dysplasia `margin_lodwick:IC`, Telangiectatic osteosarcoma `margin_lodwick:IA`) hanya diperiksa oleh agen; penggolongan cakupan §4; dan petunjuk "sudah terdaftar" di §6.

---

## 3. Hasil per set

**Vonis per set.**

| Set | n | Didukung | Sebagian | Tidak ditemukan | Bertentangan |
|---|---|---|---|---|---|
| A — hard constraint kelas b/c | 73 | 3 (4%) | 28 (38%) | 39 (53%) | 3 (4%) |
| B — semua +3 | 192 | 107 (56%) | 51 (27%) | 34 (18%) | 0 |
| C — butir lama N/X | 18 | 0 | 6 (33%) | 9 (50%) | 3 (17%) |
| **D — sampel acak (tak bias)** | **40** | **9 (22%)** | **11 (28%)** | **20 (50%)** | **0** |
| Gabungan A–D (klaim unik) | 312 | 119 | 91 | 99 | 3 |

Set A menurut kelas: kelas b (65) = 2 / 22 / 38 / 3; kelas c (8) = 1 / 6 / 1 / 0.

**Set D menurut bobot** (n kecil per baris; hanya untuk gambaran):

| Bobot | n | Didukung | Sebagian | Tidak ditemukan |
|---|---|---|---|---|
| +2 | 4 | 0 | 1 | 3 |
| +1 | 12 | 4 | 1 | 7 |
| 0 | 4 | 1 | 0 | 3 |
| −2 | 9 | 3 | 4 | 2 |
| −5 (kelas a) | 11 | 1 | 5 | 5 |

Hard constraint kelas a — yang pada tinjauan pertama dinilai "dapat dipertahankan" — pun jarang punya sumber yang menyatakan penyingkiran: 1 dari 11 di sampel.

**Hanya S-01 dibanding ada sumber kedua.**

| Kelompok | n | Didukung | Sebagian | Tidak ditemukan | Bertentangan |
|---|---|---|---|---|---|
| Set A — hanya S-01 | 26 | 0 | 3 | 23 | 0 |
| Set A — ada sumber lain | 47 | 3 | 25 | 16 | 3 |
| Set B — hanya S-01 | 56 | 11 | 18 | 27 | 0 |
| Set B — ada sumber lain | 136 | 96 | 33 | 7 | 0 |
| Set D — hanya S-01 | 15 | 0 | 1 | 14 | 0 |
| Set D — ada sumber lain | 25 | 9 | 10 | 6 | 0 |

**Per fitur (gabungan A–D).**

| Fitur | n | Didukung | Sebagian | Tidak ditemukan | Bertentangan |
|---|---|---|---|---|---|
| `age_group` | 78 | 35 | 26 | 17 | 0 |
| `multiplicity` | 3 | 2 | 1 | 0 | 0 |
| `bone_class` | 36 | 19 | 9 | 8 | 0 |
| `longitudinal` | 26 | 20 | 3 | 3 | 0 |
| `transverse` | 21 | 12 | 8 | 1 | 0 |
| `density` | 25 | 11 | 8 | 6 | 0 |
| `margin_lodwick` | 33 | 3 | 17 | 11 | 2 |
| `cortex` | 13 | 2 | 1 | 10 | 0 |
| `soft_tissue_mass` | 10 | 0 | 2 | 7 | 1 |
| `periosteal` | 30 | 6 | 6 | 18 | 0 |
| `matrix` | 31 | 6 | 9 | 16 | 0 |
| `size_cm` | 3 | 2 | 0 | 1 | 0 |
| `clinical_flags` | 3 | 1 | 1 | 1 | 0 |

Lokasi (`longitudinal`, `transverse`, `bone_class`) dan usia paling sering didukung. Fitur tampilan paling lemah: `cortex`, `soft_tissue_mass`, `periosteal`, dan `matrix` lebih sering tidak ditemukan daripada didukung, dan `margin_lodwick` hampir selalu hanya "sebagian" karena dukungannya berupa keanggotaan daftar Lodwick di S-01. Tabel per fitur untuk tiap set ada di berkas keluaran, bagian 3.

**Per sumber (gabungan A–D; satu baris bukti = satu klaim × satu sumber).**

| Sumber | Klaim A–D yang mengutip | Mendukung | Sebagian | Diam | Konflik | % diam |
|---|---|---|---|---|---|---|
| S-01 | 310 | 51 | 91 | 166 | 2 | 54% |
| S-04 | 19 | 3 | 2 | 13 | 1 | 68% |
| S-05 | 4 | 3 | 1 | 0 | 0 | 0% |
| S-06 | 88 | 32 | 27 | 28 | 1 | 32% |
| S-15 | 29 | 22 | 4 | 2 | 1 | 7% |
| S-16 | 7 | 4 | 2 | 1 | 0 | 14% |
| S-18 | 12 | 4 | 7 | 1 | 0 | 8% |
| S-19 | 1 | 0 | 1 | 0 | 0 | 0% |
| S-20 | 2 | 0 | 1 | 1 | 0 | 50% |
| S-22 | 12 | 4 | 6 | 0 | 2 | 0% |
| S-23 | 12 | 7 | 3 | 2 | 0 | 17% |
| S-24 | 7 | 3 | 2 | 2 | 0 | 29% |
| S-25 | 16 | 8 | 7 | 1 | 0 | 6% |
| S-26 | 1 | 1 | 0 | 0 | 0 | 0% |

Sumber khusus entitas (S-15, S-25, S-23, S-18, S-22) hampir selalu punya sesuatu untuk dikatakan. Pada klaim dua sumber, sumber kedua lebih kuat daripada S-01 pada 23 dari 29 klaim S-15, 15 dari 16 klaim S-25, 9 dari 12 klaim S-23, 8 dari 12 klaim S-18, dan 38 dari 88 klaim S-06; S-04 justru lebih lemah daripada S-01 pada 9 dari 19 klaim, karena hanya memuat usia dan lokasi pasien di bawah 18 tahun.

---

## 4. Cakupan entitas × sumber

Tingkat: **1** = sumber memuat gambaran radiografik entitas (*uraian* = pernyataan tersendiri; *daftar* = hanya keanggotaan daftar per fitur); **2** = hanya usia atau lokasi; **3** = hanya disebut sekilas; **4** = tidak ada. Angka dalam kurung = jumlah klaim entitas yang mengutip sumber itu. Kolom terakhir = klaim set A–D yang tidak ditemukan atau bertentangan, dibanding yang diperiksa. Tabel rinci dengan catatan per pasangan ada di berkas keluaran, bagian 8, dan di `tools/review_source_coverage.tsv`.

| Entitas | S-01 | Sumber lain | Tanpa dukungan / diperiksa |
|---|---|---|---|
| Osteofibrous dysplasia – adamantinoma spectrum | 1-uraian (42) | – | 3/8 |
| Aneurysmal bone cyst | 1-daftar (43) | S-06 1-uraian (42); S-20 3 (1) | 4/14 |
| Medullary bone infarct | 1-uraian (43) | – | 4/6 |
| Bone metastasis (carcinoma) | 1-uraian (46) | – | 1/9 |
| BPOP (Nora lesion) | 2 (37) | S-25 1-uraian (36) | 2/10 |
| Brown tumour of hyperparathyroidism | 1-daftar (46) | – | 5/7 |
| Chondroblastoma | 1-daftar (44) | S-06 1-uraian (43) | 3/10 |
| Chondromyxoid fibroma | 1-daftar (45) | S-06 3 (44); S-18 1-uraian (1) | 5/10 |
| Central chondrosarcoma | 1-daftar (49) | S-05 2 (1); S-18 1-uraian (47) | 0/6 |
| **Chordoma** | **3 (33)** | – | **13/13** |
| Clear cell chondrosarcoma | 2 (40) | S-18 1-uraian (39) | 1/7 |
| **Desmoplastic fibroma of bone** | **3 (43)** | – | **4/4** |
| Enchondroma | 1-daftar (46) | S-06 1-uraian (44); S-18 1-uraian (2) | 1/6 |
| Enostosis (bone island) | 1-uraian (43) | – | 4/5 |
| Ewing sarcoma | 1-uraian (47) | S-04 2 (46) | 4/12 |
| Fibrous dysplasia | 1-uraian (45) | S-22 1-uraian (44) | 1/12 |
| Giant cell tumour of bone | 1-daftar (46) | S-16 1-uraian (45) | 0/7 |
| Intraosseous ganglion / geode | 1-daftar (45) | – | 6/9 |
| Intraosseous lipoma | 1-daftar (42) | – | 3/5 |
| Langerhans cell histiocytosis | 1-daftar (42) | S-23 1-uraian (41); S-21 belum dibaca (1) | 2/12 |
| Non-ossifying fibroma / FCD | 1-uraian (45) | S-06 1-uraian (44) | 1/14 |
| Osteoblastoma | 1-daftar (39) | S-06 1-uraian (38); S-20 1-uraian (1) | 0/6 |
| Osteochondroma | 2 (36) | S-04 2 (33); S-26 1-uraian (3) | 1/8 |
| Osteoid osteoma | 1-uraian (43) | S-06 1-uraian (42) | 2/14 |
| Osteomyelitis (incl. Brodie abscess) | 1-uraian (42) | – | 5/6 |
| Conventional osteosarcoma | 1-uraian (46) | S-15 1-uraian (41); S-05 2 (3) | 1/11 |
| Parosteal osteosarcoma | 2 (36) | S-15 1-uraian (35) | 0/5 |
| **Periosteal osteosarcoma** | **2 (38)** | **S-15 2 (37)** | 2/10 |
| Telangiectatic osteosarcoma | 3 (42) | S-15 1-uraian (41) | 1/7 |
| Paget disease of bone | 1-uraian (44) | – | 1/4 |
| Periosteal (juxtacortical) chondroma | 2 (42) | S-25 1-uraian (41); S-18 1-uraian (1) | 0/7 |
| Plasma cell myeloma / plasmacytoma | 1-uraian (42) | S-24 2 (41) | 1/7 |
| Primary lymphoma of bone | 1-uraian (46) | – | 3/7 |
| Simple (unicameral) bone cyst | 1-daftar (44) | S-06 1-uraian (43) | 3/16 |
| **Skeletal tuberculosis** | **3 (45)** | – | **6/6** |
| Stress / insufficiency fracture | 1-uraian (44) | – | 5/7 |
| **Vertebral haemangioma** | **3 (32)** | **S-19 2 (2)** | 4/5 |

**Yang perlu dibaca dari tabel ini.**

- Menurut cakupan terbaik di antara sumber yang dikutip: 29 entitas punya paling sedikit satu uraian radiografik, 3 hanya keanggotaan daftar, 2 hanya lokasi, 3 hanya penyebutan nama.
- Dari 29 itu, **10 hanya bersandar pada uraian S-01** yang umumnya satu sampai tiga kalimat: OFD–adamantinoma, Bone infarct, Metastasis, Enostosis, Ewing sarcoma, Osteomyelitis, Paget, myeloma, Lymphoma, Stress fracture.
- "1-uraian" untuk S-01 sering sangat tipis. Contoh: Stress fracture satu kalimat; Bone infarct dua fase tanpa korteks, tepi, atau periosteal; Paget tanpa vertebra dan tengkorak (S-01 membatasi diri pada skeleton apendikular).
- Di seluruh KB, 227 dari 848 klaim fitur tampilan (densitas, tepi, korteks, jaringan lunak, periosteal, matriks, ukuran) tidak mengutip satu pun sumber yang memuat uraian tersendiri tentang entitasnya; 124 di antaranya tidak mengutip sumber yang memuat gambaran radiografik dalam bentuk apa pun.
- Terkonfirmasi: S-06 tidak punya bagian Chondromyxoid fibroma (satu penyebutan, sebagai banding chondroblastoma); seluruh 10 klaim CMF di set A–D mendapat "diam" dari S-06.

---

## 5. Klaim yang bertentangan dengan sumbernya

**Vonis bertentangan (3).** Tidak ada sumber lain yang dikutip klaim ini yang mendukungnya.

| Klaim | Bobot | Sumber, lokasi | Yang dinyatakan sumber |
|---|---|---|---|
| Chondroblastoma `soft_tissue_mass:present` | −5 | S-06, 3.3.5 Imaging dan 3.3.7 | CT dipakai antara lain untuk menilai perluasan ke jaringan lunak, dan tujuan terapi mencakup pencegahan penyebaran ke jaringan lunak sekitar. Perluasan itu diperlakukan sebagai hal yang dapat terjadi. |
| Fibrous dysplasia `margin_lodwick:IC` | −5 | S-22, Craniofacial FD dan Radiographs | Lesi kraniofasial umumnya tidak berbatas tegas, dan tepi sklerotik lesi dapat terputus atau tidak lengkap. KB sendiri memberi `bone_class:craniofacial` +3. |
| Telangiectatic osteosarcoma `margin_lodwick:IA` | −5 | S-15, 3.1.3 | Lesi kadang berbatas tegas dengan tepi sklerotik yang ireguler; pola permeatif klasik malah jarang. |

**Konflik yang dicatat tetapi tidak menjadi vonis bertentangan (4).**

| Klaim | Bobot | Vonis | Konflik |
|---|---|---|---|
| Aneurysmal bone cyst `transverse:eccentric` | +3 | sebagian | S-01 menggolongkan ABC sebagai lesi intrameduler sentral. S-06 (klasifikasi Capanna, Table 2) memuat tipe sentral dan tipe eksentrik tanpa menyebut mana yang tersering. |
| Ewing sarcoma `longitudinal:diaphysis` | +3 | didukung (S-01) | Seri S-04 (28 kasus anak): metafisis 36%, diafisis 21%; penulisnya menyebut ini berlawanan dengan aturan umum. |
| Fibrous dysplasia `transverse:central` | +3 | sebagian | Satu kalimat S-22 (bagian Radiographs) berbunyi bahwa lesi khas TIDAK terletak sentral di medula. Kalimat itu janggal dan mungkin salah ketik; perlu dibaca pemilik. |
| Conventional osteosarcoma `periosteal:solid_thin` | −2 | sebagian | S-01 menyebut reaksi tipis dapat dijumpai pada osteosarkoma, tetapi pada paragraf yang sama menyebut pola solid jarang berpenyebab ganas. Konflik ringan. |

**Hampir konflik (dicatat "tidak ditemukan").** Chondroblastoma `cortex:destruction` −5: S-06 menyebut erosi korteks sebagai hal yang mungkin tampak pada CT; kata destruksi tidak dipakai.

---

## 6. Kebutuhan sumber per entitas

Urut dari yang paling mendesak. "Sudah terdaftar" berarti sumber itu ada di `data/sources.json` dan memuat pernyataannya, tetapi tidak dikutip pada klaim yang bersangkutan; ini saya temukan saat membaca dan belum saya periksa klaim demi klaim.

**a. Perlu sumber baru: tidak ada gambaran radiografik sama sekali di sumber yang dikutip.**

- **Chordoma** — 13 dari 13 klaim yang diperiksa tidak ditemukan. S-01 menyebut namanya sekali, dalam konteks derajat histologis.
- **Desmoplastic fibroma of bone** — 4 dari 4. Satu penyebutan sebagai contoh tumor intermediat.
- **Skeletal tuberculosis** — 6 dari 6. Satu penyebutan sebagai kategori infeksi. S-10 (sudah terdaftar) memuat jumlah kasus dan porsi tulang belakang, tanpa gambaran radiografik.
- **Vertebral haemangioma** — 4 dari 5. S-01 tidak membahas vertebra; S-19 menguraikan hemangioma kalvaria dan hanya menyebut vertebra sebagai lokasi tersering.
- **Periosteal osteosarcoma** — usia dan lokasi didukung S-15, tetapi bagian subtipe ini di S-15 tidak memuat gambaran radiografik. `periosteal:spiculated` +3 dan `cortex:saucerization` +2 tidak ditemukan. S-25 (sudah terdaftar) juga hanya menyebut lokasi diafisis.

**b. Perlu sumber tambahan: hanya daftar S-01 atau uraian S-01 yang tipis.**

- **Brown tumour** (5/7), **Geode** (6/9), **Intraosseous lipoma** (3/5) — hanya keanggotaan daftar; tidak ada usia, ukuran, matriks, periosteal.
- **Osteomyelitis** (5/6) — `age_group:0-9`, `longitudinal:metaphysis`, dan `clinical_flags:fever_or_infection_signs` (semua +3) tidak ditemukan. S-01 mencantumkan abses Brodie di daftar lesi epifisis, bukan metafisis.
- **Stress fracture** (5/7), **Enostosis** (4/5), **Bone infarct** (4/6) — bobot +3 pada `cortex:intact`, `periosteal:none`, `transverse:central`, `bone_class:long_bone` tidak punya dasar di S-01.
- **Primary lymphoma of bone** (3/7), **Paget** (`bone_class:spine_body` +3), **Metastasis** (`bone_class:spine_body` hanya tersirat) — S-01 tidak membahas skeleton aksial. S-19 (sudah terdaftar) memuat usia dan pola untuk lymphoma, Paget, dan myeloma di kalvaria.
- **OFD–adamantinoma** — lokasi didukung; usia (`20-39` +3) tidak disebut.

**c. Sumber kedua perlu diganti atau ditambah.**

- **Chondromyxoid fibroma** — ganti S-06 dengan **S-18** (sudah terdaftar; memuat usia, lokasi, densitas, tepi, ekspansi, periosteal, matriks). Catatan: S-18 menyebut dewasa muda, sehingga `age_group:10-19_*` +3 tetap tidak akan didukung.
- **Plasma cell myeloma** — S-24 adalah ulasan MRI; `margin_lodwick:IB` hanya sebagian dan `matrix:none` tidak ditemukan. Perlu sumber radiografik.
- **Ewing sarcoma** — S-04 tidak memuat tampilan. `periosteal:lamellated` +3 tidak ditemukan: S-01 mengaitkan pola berlapis dengan sarkoma secara umum dan menyebut Ewing khas untuk spikula *hair-on-end*. Tiga hard constraint (IA, `expansion_shell`, `shell`) juga tanpa sumber.
- **Osteochondroma** — S-26 memuat uraian radiografik tetapi hanya dikutip 3 klaim; S-04 (33 klaim) hanya usia dan lokasi.
- **Aneurysmal bone cyst** `bone_class:spine_posterior` +3 — mengutip S-20 saja, yang hanya menyebut ABC sebagai komponen sekunder. S-06 (sudah terdaftar) menyebut elemen posterior tulang belakang.
- **Osteoblastoma** `bone_class:spine_posterior` +3 — S-20 adalah seri khusus tulang belakang. S-06 (sudah terdaftar) menyatakannya langsung. Seluruh 6 klaim osteoblastoma yang diperiksa hanya "sebagian"; S-06 menyebut rerata usia 20 tahun, di batas kelompok `10-19`.

**d. Klaim tunggal tanpa dukungan pada entitas yang sumbernya baik.** Daftar lengkap per entitas ada di berkas keluaran, bagian 5. Yang menonjol: ABC `matrix:none` +3; Simple bone cyst `margin_lodwick:IC`, `periosteal:lamellated`, `soft_tissue_mass:present` (−5); Osteoid osteoma `periosteal:lamellated` dan `margin_lodwick:IC` (−5); LCH `matrix:osteoid` dan `matrix:ground_glass` (−5); NOF `soft_tissue_mass:present` (−5); Enchondroma `periosteal:lamellated` (−5).

---

## 7. Perubahan terhadap uji petik lama

Dari 50 butir lama, 46 termasuk set A, B, atau D dan dinilai ulang: **31 sama, 15 berubah** (8 lebih mendukung, 7 kurang mendukung). Empat butir lama yang "didukung" dan berada di luar set tidak dinilai ulang.

**Set C (18 butir N/X lama):** bertentangan → bertentangan 3; bertentangan → sebagian 2; bertentangan → tidak ditemukan 1; tidak ditemukan → sebagian 4; tidak ditemukan → tidak ditemukan 8.

| Klaim | Bobot | Lama | Baru | Sebab perubahan |
|---|---|---|---|---|
| ABC `transverse:eccentric` | +3 | bertentangan | sebagian | Teks lengkap S-06 memuat tipe eksentrik (Capanna); konflik dengan S-01 tetap dicatat. |
| Conventional OS `periosteal:solid_thin` | −2 | bertentangan | sebagian | S-15 menguraikan reaksi periosteal yang agresif; S-01 ambivalen. |
| Conventional OS `age_group:60+` | +1 | bertentangan | tidak ditemukan | Klaim ini hanya mengutip S-01, yang tidak membahas usia lanjut. Vonis lama memakai S-15, yang tidak dikutip klaim ini. |
| Chondroblastoma `age_group:40-59` | −5 | tidak ditemukan | sebagian | Sumber menyebut usia khas; itu arah, bukan penyingkiran. |
| Ewing sarcoma `age_group:60+` | −5 | tidak ditemukan | sebagian | Sama: puncak usia disebut S-01. |
| LCH `age_group:60+` | −5 | tidak ditemukan | sebagian | Sama (S-23). |
| Simple bone cyst `age_group:60+` | −5 | tidak ditemukan | sebagian | Sama (S-06: 80% remaja atau usia 20-an). |
| Ewing sarcoma `longitudinal:diaphysis` | +3 | sebagian | didukung | S-01 menyatakannya khas; angka S-04 dicatat sebagai konflik. |
| Ewing sarcoma `margin_lodwick:IA` | −5 | sebagian | tidak ditemukan | Hanya tercantum pada daftar nilai lain; aturan ketat. |
| LCH `matrix:osteoid` | −5 | sebagian | tidak ditemukan | S-23 hanya menyebut sekuestrum dan fragmen tulang; itu bukan pernyataan tentang matriks. |
| ABC `periosteal:shell` | +3 | didukung | sebagian | S-01 hanya mencontohkan; S-06 tidak menamai pola shell. |
| GCTB `margin_lodwick:IB` | +3 | didukung | sebagian | Keanggotaan daftar (S-01); S-16 tidak memberi frekuensi derajat Campanacci. |
| Intraosseous lipoma `margin_lodwick:IA` | +3 | didukung | sebagian | Keanggotaan daftar. |
| Osteomyelitis `margin_lodwick:IA` | +3 | didukung | sebagian | Keanggotaan daftar (abses Brodie). |
| Simple bone cyst `bone_class:calcaneus` | +3 | didukung | sebagian | S-01 hanya daftar banding. Vonis lama memakai angka S-04 (25% di kalkaneus), yang tidak dikutip klaim ini; S-06 yang dikutip tidak menyebut kalkaneus. |

Lima penurunan "didukung → sebagian" berasal dari satu aturan: keanggotaan daftar tidak dihitung sebagai kekhasan. Dua butir lama dinilai dengan sumber yang ternyata tidak dikutip klaimnya.

---

## 8. Kaitan dengan hipotesis tinjauan pertama

"Dikuatkan" berarti sumber yang dikutip tidak mendukung kekuatan −5 (atau justru menyatakan sebaliknya); itu mendukung alasan hipotesis, bukan nilai usulnya. Tidak ada usulan bobot baru di sini.

| ID | Klaim | Vonis teks lengkap | Hipotesis |
|---|---|---|---|
| H-06 | Metastasis `age_group:10-19_*` −5 | sebagian ×3 (S-01: terutama dewasa dan lansia) | **Dikuatkan**: arah saja. |
| H-07 | GCTB `age_group:10-19_open` −5 | sebagian (S-01 "khas setelah fisis menutup"; S-16 tidak membahas pasien imatur) | **Tetap**: sama dengan penilaian lama. |
| H-08 | Osteomyelitis `matrix:osteoid` −5; Central chondrosarcoma `matrix:osteoid` −5 | tidak ditemukan; sebagian (S-18: mineralisasi kondroid) | **Dikuatkan** untuk Osteomyelitis; **tetap** untuk Central chondrosarcoma. |
| H-09 | Chondroblastoma `cortex:destruction`, `soft_tissue_mass:present`, `age_group:40-59` −5 | tidak ditemukan (erosi korteks disebut); bertentangan; sebagian | **Dikuatkan**, terutama jaringan lunak (terkonfirmasi). |
| H-10 | Simple bone cyst, NOF, Fibrous dysplasia `periosteal:lamellated` −5 | tidak ditemukan; sebagian (S-06: biasanya tanpa reaksi); sebagian (S-22: tak ada kecuali fraktur, dan fraktur sering) | **Dikuatkan**. |
| H-11 | Simple bone cyst `age_group:60+`, `longitudinal:epiphysis_apophysis` −5 | sebagian; sebagian | **Dikuatkan**: arah saja pada keduanya. |
| H-12 | Conventional OS `margin_lodwick:IA` −5; Telangiectatic OS `margin_lodwick:IA` −5; Conventional OS `periosteal:shell` −5 | sebagian; bertentangan; sebagian | **Dikuatkan** untuk Telangiectatic OS (terkonfirmasi). **Tetap** untuk tepi Conventional OS. **Sedikit dilemahkan** untuk `periosteal:shell`: S-15 menyebut pertumbuhan cepat mencegah ekspansi korteks. |
| H-13 | BPOP `density:lytic` −5; `transverse:juxtacortical_continuous` −5 | sebagian; **didukung** (S-25: tanpa kontinuitas medula adalah pembeda utama) | **Tetap** untuk `lytic`. **Dilemahkan** untuk `juxtacortical_continuous`: sumbernya mendukung −5. |
| H-14 | Geode `margin_lodwick:IC`, `soft_tissue_mass:present`, `size_cm:>5` −5 | tidak ditemukan ×3 | **Dikuatkan**: tidak ada dasar sumber. |
| H-15 | Osteoid osteoma `size_cm:>5` −5 | **didukung** (S-06: lesi di atas sekitar 1,5 cm digolongkan osteoblastoma) | **Dilemahkan** untuk bobotnya; **dikuatkan** untuk teks bantuan, karena angka S-06 merujuk pada nidus. |
| H-16 | Fibrous dysplasia `margin_lodwick:IC` −5 | bertentangan (terkonfirmasi) | **Dikuatkan**. |
| H-17 | Chordoma `density:sclerotic` −5; Ewing `cortex:expansion_shell` −5 | tidak ditemukan; tidak ditemukan | **Tak berubah**: tidak ada sumber untuk kedua arah. |
| H-18 | Brown tumour `matrix:ground_glass` −5 | tidak ditemukan | **Tak berubah**: tidak ada sumber untuk kedua arah. |
| H-26 | Sumber CMF, Chordoma, Skeletal TB, Vertebral haemangioma, entitas hanya-S-01 | terkonfirmasi dan diperluas (§4, §6) | **Dikuatkan dan dipertajam**: tambah Desmoplastic fibroma, Periosteal osteosarcoma (S-15), myeloma (S-24), Ewing dan Osteochondroma (S-04); untuk CMF sumber penggantinya sudah ada (S-18). |
| H-28 | ABC `transverse:eccentric` +3, sumber | sebagian, dengan konflik S-01 | **Tetap, dengan koreksi**: S-06 tidak sepenuhnya diam (memuat tipe eksentrik), tetapi tidak ada sumber yang dikutip menyebut eksentrik sebagai yang khas. |

Dua catatan di luar daftar yang diminta. H-25 dan H-33 (Conventional OS `periosteal:solid_thin` dan `age_group:60+`) kehilangan sebagian dasar sumbernya, lihat §7; untuk usia lanjut, S-05 (sudah terdaftar) melaporkan dua puncak insidens sedangkan S-15 meragukan puncak kedua — kedua sumber berbeda pendapat. H-05 (aturan massa jaringan lunak tanpa destruksi): S-01 berbicara tentang ketiadaan destruksi korteks yang berarti dan tidak membahas `focal_breach` tersendiri.

---

## 9. Aturan (set R)

| Aturan | Bobot | Dikutip | Vonis | Catatan |
|---|---|---|---|---|
| Ewing `ewing_adult_flat_bone` | +1 | S-01 | didukung | Pergeseran ke tulang pipih di atas 20 tahun dinyatakan. |
| Ewing `ewing_soft_tissue_without_destruction` | +2 | S-01 | sebagian | Pola disebut dapat terjadi, bukan khas. |
| Lymphoma `lymphoma_soft_tissue_without_destruction` | +2 | S-01 | sebagian | Sama. |
| Osteomyelitis `om_all_four_aggressive_signs` | +1 | S-10 | didukung | Empat tanda mayor bersama memberi nilai prediksi 100% untuk keganasan atau infeksi (88 lesi). |
| Telangiectatic OS `tos_abc_mimic_aggressive` | +1 | S-01, S-15 | didukung | S-15 menguraikan kemiripan dengan ABC; S-01 diam. |

---

## 10. Berkas

- `tools/review_sources.py` — skrip (pustaka standar): memuat KB, memeriksa berkas bukti, menarik set D, menggabungkan vonis, menulis CSV, mencetak semua tabel.
- `tools/review_source_evidence.tsv` — 526 baris temuan per klaim per sumber (520 untuk set A–D, 6 untuk aturan).
- `tools/review_source_coverage.tsv` — 68 baris cakupan entitas × sumber.
- `docs/tinjauan-sumber-v0.6.csv` — vonis per klaim per set (328 baris; klaim yang ada di dua set muncul dua kali).
- `docs/tinjauan-sumber-v0.6-keluaran.txt` — keluaran lengkap skrip, termasuk daftar seluruh vonis (bagian 10).

Menjalankan ulang: `python3 tools/review_sources.py > docs/tinjauan-sumber-v0.6-keluaran.txt`.
