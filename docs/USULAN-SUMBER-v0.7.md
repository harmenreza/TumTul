# Usulan Perbaikan Sumber untuk v0.7 (belum diterapkan)

**Tanggal:** 2026-11-22 · **Dasar:** `docs/TINJAUAN-SUMBER-v0.6.md` (H-26) · **Status:** bagian A **disetujui pemilik dan diterapkan pada 2026-11-22 sebagai KB 0.6.1 (sumber saja)**; bagian B2 (S-31, S-32) juga **disetujui dan diterapkan pada hari yang sama**; bagian B lainnya dan C masih usulan (lihat "Pembaruan" di akhir dokumen).

Tiga bagian: (A) pengutipan ulang klaim Chondromyxoid fibroma ke S-18, lengkap klaim demi klaim; (B) kandidat sumber berlisensi terbuka untuk lima entitas tanpa sumber radiografik — **bagian B belum selesai**; (C) poster EPOS yang disarankan pemilik.

Kedua usulan hanya menyentuh `source_ids`, bukan bobot. Skor dan peringkat tidak berubah, sehingga tidak bertentangan dengan pembekuan bobot dalam protokol validasi. Bagian A diterapkan lewat `tools/apply_source_overrides.py`, yang dijalankan setelah generator dan membuktikan bahwa selain `source_ids` tidak ada yang berubah. Generator sendiri tidak diubah (berkasnya hanya ada di proyek, tidak di repo).

---

## A. Chondromyxoid fibroma: ganti S-06 dengan S-18 (diterapkan, KB 0.6.1)

**Keadaan sebelum perubahan (KB 0.6.0).** 46 klaim CMF; 44 mengutip S-01 dan S-06, 1 hanya S-01, 1 hanya S-18. S-06 tidak punya bagian tentang CMF: ia hanya disebut sekali, dalam daftar banding chondroblastoma (dibaca pada teks lengkap, [DOI](https://doi.org/10.3390/jcm11030699)).

**Yang dikatakan S-18** (bagian *Chondromyxoid Fibroma*; Gómez-León dkk. 2023, [DOI](https://doi.org/10.1067/j.cpradiol.2023.01.005), dibaca dari PDF kiriman pemilik; dinyatakan ulang dengan kata sendiri): tumor jarang yang khas pada dewasa muda; kebanyakan mengenai rongga medula di metafisis tulang panjang, dapat juga di tangan dan kaki; pada usia lanjut diagnosis lain harus disingkirkan. Pada radiograf: lesi litik eksentrik dengan tepi sklerotik berbatas tegas, sering ekspansil, tanpa reaksi periosteal, dengan destruksi geografik dan septasi; kalsifikasi matriks biasanya tidak ada. Tipe permukaan (jukstakortikal) lebih jarang lagi dan lebih sering berkalsifikasi.

**Usulan.**
1. Hapus S-06 dari seluruh 44 klaim CMF yang mengutipnya, dan dari `source_ids` entitas.
2. Tambahkan S-18 pada 19 klaim yang isinya dinyatakan atau diarahkan oleh S-18 (kolom "Sumber usulan").
3. Klaim yang tetap hanya S-01 ditandai "perlu sumber" untuk tahap berikutnya.

**Hasil bila diterapkan:** 20 dari 46 klaim CMF mengutip sumber yang memang membahas temuannya (sekarang 1): 13 didukung, 7 arah saja. 23 klaim tidak dibahas S-18 dan tetap hanya mengutip S-01 (satu di antaranya, `longitudinal:metadiaphysis`, didukung S-01; status S-01 untuk yang lain baru diperiksa pada 10 klaim), dan 3 klaim usia tidak sesuai dengan S-18.

| Klaim | Bobot | Sumber sekarang | S-18 | Sumber usulan | Catatan |
|---|---|---|---|---|---|
| `age_group:0-9` | +1 | S-01, S-06 | diam | S-01 |  |
| `age_group:20-39` | +2 | S-01, S-06 | didukung | S-01, S-18 | khas pada dewasa muda |
| `age_group:40-59` | +0 | S-01, S-06 | diam | S-01 |  |
| `age_group:60+` | -2 | S-01, S-06 | didukung | S-01, S-18 | pada usia lanjut diagnosis lain harus disingkirkan |
| `age_group:10-19_unknown` | +3 | S-01, S-06 | tidak sesuai | S-01 | sama |
| `age_group:10-19_open` | +3 | S-01, S-06 | tidak sesuai | S-01 | S-18 menyebut dewasa muda, bukan remaja; terkait H-02 |
| `age_group:10-19_closed` | +2 | S-01, S-06 | tidak sesuai | S-01 | sama |
| `bone_class:long_bone` | +3 | S-01, S-06 | didukung | S-01, S-18 | kebanyakan di metafisis tulang panjang |
| `bone_class:flat_bone` | +1 | S-01, S-06 | diam | S-01 |  |
| `bone_class:small_tubular_hand_foot` | +1 | S-01, S-06 | didukung | S-01, S-18 | dapat muncul di tangan dan kaki |
| `bone_class:spine_body` | -2 | S-01, S-06 | diam | S-01 |  |
| `longitudinal:metadiaphysis` | +3 | S-01, S-06 | diam | S-01 | S-18 menyebut metafisis; S-01 yang mendukung metadiafisis |
| `longitudinal:metaphysis` | +2 | S-01, S-06 | didukung | S-01, S-18 | daerah metafisis |
| `longitudinal:diaphysis` | +0 | S-01, S-06 | diam | S-01 |  |
| `longitudinal:epiphysis_apophysis` | -2 | S-01, S-06 | diam | S-01 |  |
| `transverse:eccentric` | +3 | S-01, S-06 | didukung | S-01, S-18 | digambarkan sebagai lesi eksentrik |
| `transverse:central` | +0 | S-01, S-06 | diam | S-01 |  |
| `transverse:cortical` | +1 | S-01, S-06 | diam | S-01 |  |
| `transverse:juxtacortical_surface` | -2 | S-01, S-06 | didukung | S-01, S-18 | tipe permukaan ada tetapi lebih jarang lagi |
| `transverse:juxtacortical_continuous` | -2 | S-01, S-06 | diam | S-01 |  |
| `density:lytic` | +3 | S-01, S-06 | didukung | S-01, S-18 | lesi litik |
| `density:mixed` | +0 | S-01, S-06 | diam | S-01 |  |
| `density:sclerotic` | -5 | S-01, S-06 | sebagian (arah saja) | S-01, S-18 | digambarkan litik; sklerotik tidak dibahas |
| `margin_lodwick:IA` | +3 | S-01, S-06 | didukung | S-01, S-18 | tepi sklerotik berbatas tegas |
| `margin_lodwick:IB` | +0 | S-01, S-06 | diam | S-01 |  |
| `margin_lodwick:IC` | -5 | S-01, S-06 | sebagian (arah saja) | S-01, S-18 | destruksi geografik bertepi tegas; tepi tidak tegas tidak dibahas |
| `margin_lodwick:II` | -5 | S-01, S-06 | sebagian (arah saja) | S-01, S-18 | sama |
| `margin_lodwick:III` | -5 | S-01, S-06 | sebagian (arah saja) | S-01, S-18 | sama |
| `cortex:expansion_shell` | +2 | S-01, S-06 | didukung | S-01, S-18 | sering ekspansil |
| `cortex:intact` | +1 | S-01, S-06 | diam | S-01 |  |
| `cortex:endosteal_scalloping` | +1 | S-01, S-06 | diam | S-01 |  |
| `cortex:destruction` | -5 | S-01, S-06 | diam | S-01 |  |
| `soft_tissue_mass:present` | -5 | S-01, S-06 | diam | S-01 |  |
| `periosteal:none` | +2 | S-01, S-06 | didukung | S-01, S-18 | tanpa reaksi periosteal |
| `periosteal:shell` | +1 | S-01, S-06 | diam | S-01 |  |
| `periosteal:lamellated` | -2 | S-01, S-06 | sebagian (arah saja) | S-01, S-18 | disebut tanpa reaksi periosteal; pola lamelar tidak dibahas |
| `periosteal:spiculated` | -5 | S-01, S-06 | sebagian (arah saja) | S-01, S-18 | sama |
| `periosteal:codman` | -5 | S-01, S-06 | sebagian (arah saja) | S-01, S-18 | sama |
| `periosteal:present_unspecified` | +1 | S-01 | diam | S-01 | S-18 menyebut tanpa reaksi periosteal; +1 tidak punya dasar di S-18 |
| `matrix:none` | +2 | S-18 | didukung | S-18 | kalsifikasi matriks biasanya tidak ada (sudah mengutip S-18) |
| `matrix:chondroid` | +0 | S-01, S-06 | didukung | S-01, S-18 | kalsifikasi dapat ada, lebih sering pada tipe permukaan |
| `matrix:osteoid` | -5 | S-01, S-06 | diam | S-01 |  |
| `matrix:ground_glass` | -2 | S-01, S-06 | diam | S-01 |  |
| `size_cm:<2` | +0 | S-01, S-06 | diam | S-01 |  |
| `size_cm:2-5` | +1 | S-01, S-06 | diam | S-01 |  |
| `size_cm:>5` | +0 | S-01, S-06 | diam | S-01 |  |

**Tiga hal untuk diputuskan pemilik.**
- **Usia 10–19 (+3, +3, +2).** S-18 menyebut dewasa muda. Tidak ada sumber yang dikutip mendukung puncak pada remaja. Ini menguatkan H-02 (menurunkan `10-19_open` dan `10-19_unknown` ke +2) tetapi itu perubahan bobot, jadi tetap menunggu uji kasus praktik. Dalam usulan ini klaim usia 10–19 dibiarkan hanya S-01 dan ditandai.
- **Tujuh hard constraint dan bobot negatif yang hanya "arah saja".** S-18 menggambarkan pola khas, bukan menyingkirkan pola lain. Mengutip S-18 di sini jujur sejauh arah; kekuatan −5 tetap tidak bersumber (lihat H-10 untuk preseden pelonggaran `periosteal:lamellated`).
- **`periosteal:present_unspecified` +1.** S-18 menyatakan tanpa reaksi periosteal. Bobot +1 berasal dari aturan turunan umum v0.5.0; untuk CMF tidak ada dasar sumbernya.

Sumber lanjutan yang dirujuk S-18 untuk CMF (belum diperiksa lisensinya): seri pencitraan CMF oleh Cappelle dkk. dan seri CMF jukstakortikal oleh Baker dkk.

---

## B. Kandidat sumber untuk lima entitas tanpa sumber radiografik (belum selesai)

Pencarian dilakukan di PubMed dengan penyaring akses terbuka PMC; lisensi diperiksa lewat metadata PMC. **Belum ada kandidat yang dibaca teks lengkapnya.** Sebelum satu klaim pun dikutip ulang, setiap kandidat harus melalui pemeriksaan teks lengkap klaim demi klaim seperti pada `docs/TINJAUAN-SUMBER-v0.6.md`.

| Entitas | Kandidat | Lisensi | Yang diketahui | Penilaian |
|---|---|---|---|---|
| Chordoma | Ariyaratne dkk. 2023, *Primary Osseous Malignancies of the Spine*, Diagnostics 13(10):1801 — [DOI](https://doi.org/10.3390/diagnostics13101801) | CC BY 4.0 (metadata PMC) | Ulasan dengan penekanan pada gambaran pencitraan, termasuk radiografi; kata kunci memuat chordoma, chondrosarcoma, Ewing sarcoma, osteosarcoma, plasmacytoma, lymphoma. Hanya abstrak yang dibaca. | **Kandidat utama.** Dapat sekaligus menjadi sumber kedua untuk myeloma/plasmacytoma dan lymphoma di tulang belakang. |
| Chordoma | Santegoeds dkk. 2018, *State-of-the-Art Imaging in Human Chordoma of the Skull Base*, Curr Radiol Rep 6:16 — [DOI](https://doi.org/10.1007/s40134-018-0275-7) | CC BY 4.0 | CT dan MRI basis kranii saja; tidak memuat radiografi polos. Menyebut lesi litik destruktif dengan perluasan jaringan lunak; kalsifikasi pada varian kondroid. Dibaca lewat ringkasan halaman (100.000 karakter pertama). | Pelengkap terbatas; di luar cakupan v1 (klivus). |
| Vertebral haemangioma | Ariyaratne dkk. 2023, *Primary Benign Neoplasms of the Spine*, Diagnostics 13(12):2006 — [DOI](https://doi.org/10.3390/diagnostics13122006) | CC BY 4.0 (metadata PMC) | Ulasan dengan penekanan pada gambaran pencitraan, termasuk radiografi; menyebut haemangioma dan enostosis sebagai yang tersering; kata kunci memuat osteoid osteoma, osteoblastoma, ABC, GCT, osteochondroma, eosinophilic granuloma. Hanya abstrak yang dibaca. | **Kandidat utama.** Dapat menambah sumber untuk enostosis dan lokasi spinal osteoblastoma serta ABC. |
| Desmoplastic fibroma of bone | Kang dkk. 2014, laporan kasus klavikula dengan tinjauan pustaka, Korean J Radiol 15:130 — [DOI](https://doi.org/10.3348/kjr.2014.15.1.130); Kim dkk. 2013, laporan kasus jari kaki, Korean J Radiol 14:963 — [DOI](https://doi.org/10.3348/kjr.2013.14.6.963) | CC BY-NC 3.0 | Keduanya laporan kasus di lokasi tidak lazim; abstrak Kim dkk. menyebut lokasi tersering mandibula, tulang panjang besar, dan iliaka. | **Belum memadai.** Belum ditemukan ulasan atau seri radiografik berlisensi terbuka. |
| Skeletal tuberculosis | — | — | Dua hasil yang diperiksa (sitologi aspirasi pada anak; tata laksana TB osteoartikular anak) tidak memuat gambaran radiografik. | **Belum ditemukan.** |
| Periosteal osteosarcoma | — | — | Dua hasil yang diperiksa (osteosarkoma permukaan derajat tinggi di iga; kohort osteosarkoma parosteal) bukan tentang gambaran radiografik osteosarkoma periosteal. | **Belum ditemukan.** |

Artikel pada tabel ini diambil dari PubMed; metadata dan abstraknya menjadi dasar kolom "Yang diketahui".

**Mengapa belum selesai.** Pencarian PubMed hanya mengembalikan nomor artikel, sehingga tiap kandidat harus dibuka satu per satu; halaman PMC menolak pembacaan otomatis setelah permintaan pertama. Dalam satu sesi hanya sebagian kecil hasil yang dapat disaring (17 hasil chordoma, 21 desmoplastic fibroma, 27 tuberkulosis, 57 haemangioma, 22 osteosarkoma permukaan; sekitar 30 diperiksa lisensinya, 9 dibaca abstraknya).

**Langkah berikutnya yang diusulkan.**
1. Membaca teks lengkap kedua ulasan Ariyaratne dkk. dan memeriksa klaim Chordoma serta Vertebral haemangioma terhadapnya.
2. Pencarian khusus untuk Skeletal tuberculosis, Desmoplastic fibroma dan Periosteal osteosarcoma, dikerjakan sebagai satu putaran terpisah. Bila pemilik mengenal ulasan radiografik berlisensi terbuka untuk ketiganya, judulnya mempercepat pekerjaan.
3. Bila untuk suatu entitas tidak ada sumber CC BY, pilihan yang sesuai aturan proyek: sumber CC BY-NC (aplikasi harus tetap gratis dan tanpa iklan), Radiopaedia dengan atribusi CC BY-NC-SA, atau sumber tertutup sebagai `cite_only` untuk fakta yang dinyatakan ulang.

---

## C. Poster EPOS (saran pemilik, 2026-11-22)

Pemilik menyarankan mencari di EPOS (poster elektronik ESR), dengan dua contoh dari ESSR 2013: P-0118 (tuberkulosis muskuloskeletal ekstraspinal, [DOI](https://dx.doi.org/10.1594/essr2013/P-0118)) dan P-0053 (ragam tampilan osteosarkoma, [DOI](https://dx.doi.org/10.1594/essr2013/P-0053)).

**Lisensi (halaman disclaimer EPOS, dibaca lewat ringkasan).** Hak cipta EPOS dipegang ESR; pemakaian ulang di luar *fair use* memerlukan izin tertulis. Untuk poster **ECR 2014 dan sesudahnya** berlaku lisensi terbuka: boleh dibagikan dan diolah dengan atribusi, non-komersial, dan berbagi-serupa (nama lisensi Creative Commons tidak disebut; poster yang tercakup memuat tulisan bahwa ia terbit dengan lisensi terbuka). Akibatnya:

- poster sebelum 2014, termasuk kedua contoh, hanya dapat masuk sebagai `cite_only` (fakta dinyatakan ulang, dikutip secara bibliografis);
- poster ECR 2014+ setara kelas non-komersial berbagi-serupa: aplikasi harus tetap gratis dan tanpa iklan, seperti untuk sumber CC BY-NC-SA;
- untuk poster kongres lain (mis. ESSR) setelah 2014, status lisensi harus dicek per poster.

**Catatan mutu.** Poster kongres tidak melalui telaah sejawat seperti artikel jurnal. Bila dipakai, `evidence_level` sebaiknya menyatakannya, dan artikel jurnal tetap diutamakan bila ada.

**Kandidat** (dari pencarian di epos.myesr.org; baru judul, jenis, dan cuplikan yang terbaca — **belum ada yang dibaca penuh**).

| Entitas | Poster | Jenis | Catatan |
|---|---|---|---|
| Skeletal tuberculosis | ECR 2019 C-1421, *A dicey encounter: Musculoskeletal tuberculosis* — [DOI](https://dx.doi.org/10.26044/ecr2019/C-1421) | Educational exhibit | Kata kunci memuat radiografi konvensional; cuplikan gambar memuat lesi litik berbatas tidak tegas di humerus, dengan dan tanpa reaksi periosteal. **Kandidat utama.** |
| Skeletal tuberculosis | ECR 2015 C-0939, *Imaging features of extra spinal musculoskeletal tuberculosis*; ECR 2025 C-19105, *Unveiling Musculoskeletal Tuberculosis: Radiological Insights*; ESSR 2019 P-0086, *Tuberculosis and the musculoskeletal system* | Poster edukasi | Pelengkap. ECR 2025 mencakup bahu, siku, tangan, tulang belakang, iga, panggul, lutut, pergelangan kaki. Lisensi ESSR 2019 perlu dicek. |
| Skeletal tuberculosis | ECR 2013 C-2088, *Imaging spectrum of musculoskeletal tuberculosis: Pictorial essay* — [DOI](https://dx.doi.org/10.1594/ecr2013/C-2088); ESSR 2012 P-0099; ESSR 2013 P-0118 (contoh pemilik) | Educational / scientific exhibit | Sebelum 2014: `cite_only`. C-2088 memuat radiograf spina ventosa. |
| Periosteal osteosarcoma | ECR 2022 C-13882, *Imaging review of Surface Osteosarcomas* — [DOI](https://dx.doi.org/10.26044/ecr2022/C-13882) | Educational exhibit | Tujuannya menyoroti temuan pencitraan yang membedakan osteosarkoma parosteal, periosteal, dan permukaan derajat tinggi; kata kunci memuat radiografi konvensional. **Kandidat utama**; juga berguna untuk Parosteal osteosarcoma. |
| Periosteal osteosarcoma | ECR 2022 C-13985, *Surface osteosarcomas: imaging and histological characteristics* | Scientific exhibit | Seri 21 tumor: 14 parosteal, 2 periosteal, 5 derajat tinggi. |
| Desmoplastic fibroma | ECR 2016 C-1707, *Benign bone lesions with eccentric expansion…*; ECR 2018 C-3069, *Non-traumatic knee pathology in adults*; ECR 2017 C-1434, *…Fibrous Lesions of Bone* | Poster edukasi | Tidak ada poster khusus. Ketiganya memuat bagian singkat: lesi litik ekspansil, destruksi geografik, pseudotrabekulasi, penipisan atau terputusnya korteks. **Masih lemah**; lebih baik dicari seri kasus jurnal. |

**Langkah berikutnya untuk bagian C:** membuka bagian *Findings and procedure details* dari C-1421 dan C-13882, memastikan tulisan lisensi terbuka ada di halamannya, lalu memeriksa klaim Skeletal tuberculosis dan Periosteal osteosarcoma terhadapnya.

---

## B2. Hasil pembacaan teks lengkap dua ulasan Ariyaratne dkk. (2026-11-22)

Kedua ulasan dibaca seluruhnya lewat PubMed Central oleh sesi utama (satu penilai; aturan penilaian sama ketatnya dengan `docs/TINJAUAN-SUMBER-v0.6.md`). Keduanya CC BY 4.0. **Belum ada yang diterapkan**: sumbernya belum didaftarkan di `data/sources.json` dan belum dikutip klaim mana pun. Keduanya menekankan CT dan MRI; radiografi disebut bernilai terbatas di tulang belakang, jadi dukungannya untuk klaim radiograf polos bersifat tidak langsung.

### Chordoma — *Primary Osseous Malignancies of the Spine* ([DOI](https://doi.org/10.3390/diagnostics13101801)), bagian 3.4, Table 2, Fig. 6

Isi (kata sendiri): tumor tumbuh lambat dan invasif lokal dari sisa notokord; puncak insidens dekade keempat sampai ketujuh; di garis tengah, berasal dari korpus vertebra dengan arkus neural biasanya bebas; lebih dari separuh di sakrum, sisanya di korpus vertebra tulang belakang mobil; tumor primer sakrum tersering. Pencitraan: massa destruktif besar di garis tengah dengan perluasan jaringan lunak ekstraoseus; daerah beratenuasi rendah dan destruksi pada radiograf dan CT; kalsifikasi berbintik dan perdarahan sering; kolaps vertebra.

| Vonis | Jumlah (dari 32 klaim) | Klaim |
|---|---|---|
| Didukung | 11 | `age_group:40-59` +3, `60+` +3, `20-39` +1; `bone_class:sacrum` +3, `spine_body` +2, `long_bone` −5 dan `flat_bone` −5 (asal notokord, garis tengah aksial), `spine_posterior` −2; `density:lytic` +3; `cortex:destruction` +2; `soft_tissue_mass:present` +3 |
| Sebagian (arah saja) | 9 | `age_group:0-9` dan tiga nilai `10-19` (−5; sumber hanya memberi puncak usia); `transverse:central` +2 (garis tengah); `density:sclerotic` −5; `cortex:intact` −2; `soft_tissue_mass:absent` −2; `matrix:chondroid` 0 |
| Tidak dibahas | 11 | `bone_class:craniofacial`; `density:mixed`; kelima nilai `margin_lodwick`; `cortex:focal_breach`; `periosteal:none`; `matrix:osteoid`, `matrix:ground_glass` |
| Konflik ringan | 1 | `matrix:none` +2 — sumber menyebut kalsifikasi berbintik di dalam lesi sering dijumpai |

Dengan sumber ini Chordoma berubah dari 0 menjadi 20 klaim yang punya sumber yang membahasnya (dari 13 klaim yang diperiksa sebelumnya, semuanya "tidak ditemukan").

### Vertebral haemangioma — *Primary Benign Neoplasms of the Spine* ([DOI](https://doi.org/10.3390/diagnostics13122006)), bagian 3.7, Table 2, Fig. 13, 16, 17

Isi (kata sendiri): tumor jinak primer tulang belakang tersering (sekitar 11% pada autopsi); biasanya di korpus vertebra, elemen posterior jarang, sakrum jarang; kebanyakan tanpa gejala. Pada CT: terbatas pada korpus, trabekula menebal berorientasi vertikal (*corduroy*), tampilan sarang lebah, pola *polka dot* pada potongan aksial. Hemangioma agresif (jarang): ekspansil, tampak litik, dengan destruksi tulang dan komponen jaringan lunak ekstraoseus. **Usia tidak disebut.**

| Vonis | Jumlah (dari 32 klaim) | Klaim |
|---|---|---|
| Didukung | 3 | `bone_class:spine_body` +3; `matrix:coarse_trabeculae` +3; `soft_tissue_mass:present` −2 (ada pada bentuk agresif yang jarang) |
| Sebagian (arah saja) | 5 | `transverse:central` +2; `density:mixed` +2; `density:lytic` +1 (bentuk agresif); `cortex:intact` +2; `cortex:focal_breach` −2 |
| Tidak dibahas | 23 | ketujuh nilai `age_group`; `bone_class:craniofacial`, `long_bone`, `flat_bone`; `density:sclerotic`; kelima nilai `margin_lodwick`; `periosteal:none`, `present_unspecified`; `matrix:none`, `osteoid`, `chondroid`, `ground_glass`; `multiplicity:multiple` |
| Bertentangan | 1 | `cortex:destruction` **−5** — sumber menguraikan hemangioma agresif dengan destruksi tulang dan massa jaringan lunak. Jarang, tetapi bukan mustahil; kandidat hipotesis baru (−5 → −2) untuk dinilai pemilik |

Sumber ini menopang dua ciri khas hemangioma, tetapi usia, tepi, dan periosteal tetap tanpa sumber; masih perlu satu sumber radiografik lagi.

### Yang juga dimuat kedua ulasan (terlihat saat membaca, belum diperiksa klaim demi klaim)

- **Enostosis:** predileksi skeleton aksial dan korpus vertebra; sklerotik padat berbatas tegas, umumnya 2–10 mm, tepi berspikula; multipel pada sekitar seperlima kasus; ambang atenuasi CT.
- **Osteoid osteoma dan osteoblastoma:** predileksi elemen posterior (osteoid osteoma 75–90%); usia muda; batas ukuran nidus 1,5–2 cm; osteoblastoma litik ekspansil dengan tepi sklerotik, destruksi korteks dan perluasan ekstraoseus pada kasus agresif.
- **ABC:** elemen posterior; dua dekade pertama; lusen ekspansil seperti balon; destruksi korteks fokal sering; zona transisi sempit.
- **GCTB:** 90% kasus spinal di sakrum; dekade ketiga dan keempat; lusen dengan cangkang tulang tipis.
- **LCH (eosinophilic granuloma):** di bawah 10 tahun; korpus vertebra; vertebra plana pada sekitar 40%; litik dengan destruksi; komponen jaringan lunak dapat ada.
- **Chondroblastoma vertebra:** dilaporkan tampil agresif dengan massa jaringan lunak — sejalan dengan H-09.
- **Lymphoma:** infiltrasi permeatif tanpa destruksi korteks dengan massa jaringan lunak pada kebanyakan kasus — sumber untuk aturan jaringan lunak tanpa destruksi.
- **Plasmacytoma:** litik destruktif, tampilan gelembung sabun, komponen jaringan lunak sering. **Ewing sarcoma spinal:** sakrum tersering, 93% litik, komponen jaringan lunak biasanya ada. **Chondrosarcoma:** kalsifikasi *rings-and-arcs*, usia rerata sekitar 52 tahun.

**Usulan:** daftarkan keduanya sebagai sumber baru (S-31 dan S-32, CC BY 4.0), kutip pada klaim Chordoma dan Vertebral haemangioma yang didukung atau diarahkan, lalu perluas ke entitas lain setelah diperiksa klaim demi klaim. Menambah entri ke `data/sources.json` mengikuti skema yang ada dan tidak mengubah skema.

---

## Pembaruan 2026-11-22 (setelah persetujuan pemilik atas ketiga butir)

**B2 diterapkan (masih KB 0.6.1, sumber saja).** S-31 (*Primary Osseous Malignancies of the Spine*) dan S-32 (*Primary Benign Neoplasms of the Spine*) didaftarkan di `data/sources.json` (registri 0.3.0, 32 entri). S-31 ditambahkan pada 20 klaim Chordoma (11 didukung, 9 arah saja); S-32 pada 8 klaim Vertebral haemangioma (3 dan 5). Tidak dikutip: Chordoma `matrix:none` dan Vertebral haemangioma `cortex:destruction`, karena sumbernya menyatakan lain. Bobot identik; prototipe publik dan matriks diterbitkan ulang.

**C2. Dua poster EPOS utama diperiksa** — lewat ringkasan halaman per bagian, **bukan pembacaan teks kata demi kata**; anggap sebagai penyaringan.

*Lisensi:* pada kedua halaman yang dibuka tidak terlihat tulisan lisensi terbuka, hanya hak cipta ESR dan tautan ke disclaimer. Sampai dipastikan di halaman posternya, keduanya diperlakukan sebagai `cite_only`.

*Periosteal osteosarcoma vs ECR 2022 C-13882 (bagian Findings and procedure details).* Isi: puncak insidens dekade kedua; tersering di diafisis femur dan tibia; mengenai sekitar separuh lingkar korteks; reaksi periosteal agresif dengan spikula tegak lurus dan/atau segitiga Codman; khas lusen, fusiform, mineralisasi bervariasi dengan komponen kartilago; ada massa jaringan lunak; keterlibatan medula jarang tetapi tidak menyingkirkan.

| Vonis | Jumlah (dari 38) | Klaim |
|---|---|---|
| Didukung | 10 | ketiga `age_group:10-19` +3; `bone_class:long_bone` +3; `longitudinal:diaphysis` +3; `transverse:juxtacortical_surface` +3; `density:lytic` +1; `soft_tissue_mass:present` +2; `periosteal:spiculated` +3; `periosteal:codman` +2 |
| Sebagian | 11 | `age_group:40-59`, `60+`; `longitudinal:epiphysis_apophysis`; `transverse:central`, `eccentric`; `density:mixed`; `soft_tissue_mass:absent`; `periosteal:none`, `present_unspecified`; `matrix:chondroid`, `matrix:none` |
| Tidak dibahas | 17 | antara lain `cortex:saucerization` +2 dan seluruh nilai `cortex`; `age_group:20-39`; `matrix:osteoid` |

`periosteal:spiculated` +3, yang pada pemeriksaan sumber berstatus "tidak ditemukan", kini punya sumber. `cortex:saucerization` masih belum.

*Skeletal tuberculosis vs ECR 2019 C-1421 (bagian Findings and procedure details).* Isi: keterlibatan metafisis; sklerosis dan reaksi periosteal tidak lazim, dapat muncul pada tahap lanjut; sekuestrum tidak lazim; bayangan jaringan lunak relatif kecil (abses dingin); kalsifikasi jaringan lunak khas; lesi kortikal permeatif. Usia, tulang belakang, multiplisitas, dan demam tidak dibahas pada bagian itu.

| Vonis | Jumlah (dari 45) | Klaim |
|---|---|---|
| Didukung | 4 | `longitudinal:metaphysis` +2; `periosteal:none` +2; `density:sclerotic` −2; `soft_tissue_mass:present` +1 |
| Sebagian | 14 | `density:lytic`; `margin_lodwick:IA`, `IB`, `IC`, `II`; `cortex:destruction`; `periosteal:lamellated`, `codman`, `spiculated`, `present_unspecified`, `solid_thin`; `bone_class:long_bone`, `small_tubular_hand_foot`, `flat_bone` (tiga yang terakhir hanya dari keterangan gambar) |
| Tidak dibahas | 27 | seluruh `age_group`; `bone_class:spine_body`, `sacrum`; seluruh `transverse`; seluruh `matrix`; `multiplicity`; `clinical_flags:fever_or_infection_signs` |

Poster ini lemah untuk Skeletal tuberculosis: tulang belakang, usia, dan tanda klinis tetap tanpa sumber. Perlu sumber lain, terutama untuk spondilitis.

**Masih terbuka:** Desmoplastic fibroma (tanpa sumber memadai); spondilitis TB; `cortex:saucerization` osteosarkoma periosteal; usia dan tepi hemangioma vertebra; kepastian lisensi kedua poster.
