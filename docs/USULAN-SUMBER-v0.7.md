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

---

## Pembaruan 2026-11-22 (b): kandidat sumber dari pemilik untuk Periosteal osteosarcoma

**Revell MP, Deshmukh N, Grimer RJ, Carter SR, Tillman RM. Periosteal osteosarcoma: a review of 17 cases with mean follow-up of 52 months. Sarcoma 2002;6(4):123–130.** doi 10.1080/1357714021000066368, PMID 18521348, PMC2395495. PDF dari pemilik dibaca penuh (9 halaman).

*Lisensi:* metadata PMC menyebut Creative Commons Attribution (tautan `creativecommons.org/licenses/by/`, tanpa nomor versi), hak cipta Hindawi. PDF yang dilampirkan memuat baris lama "© Taylor & Francis Ltd". Dapat didaftarkan sebagai CC BY (versi tidak disebut) dengan catatan itu. **Belum didaftarkan; menunggu pemilik.**

*Jenis bukti:* seri bedah satu pusat, 17 pasien (1983–1999). Radiologi hanya dua kalimat; kekuatannya pada usia dan lokasi per pasien (Tabel 2).

*Catatan data:* Tabel 1 (usia per dekade) berjumlah 21 dan memuat empat pasien 40–49 tahun, bertentangan dengan teks (17 pasien, 10–35 tahun, median 18) dan Tabel 2. Angka di bawah dihitung dari Tabel 2.

*Isi yang relevan:* usia 10–19: 11 dari 17; 20–29: 5; 30–39: 1; tidak ada di bawah 10 atau di atas 35. Lokasi: tibia 8 (proksimal 5, tengah 3), femur 7 (proksimal 4, tengah 2, distal 1), humerus tengah 1, skapula 1. Semua di permukaan periosteal dengan pusat massa di luar tulang dan kalsifikasi berbintik yang khas; tumor kaya kartilago. Keterlibatan medula 4 dari 17. Lingkar korteks yang terkena 5–100%. Ukuran 4–13,5 cm.

| Vonis | Jumlah (dari 38) | Klaim |
|---|---|---|
| Didukung | 8 | ketiga `age_group:10-19` +3; `age_group:20-39` +2; `bone_class:long_bone` +3; `bone_class:flat_bone` −2 (1 dari 17, skapula); `transverse:juxtacortical_surface` +3; `matrix:chondroid` +2 |
| Sebagian | 8 | `longitudinal:diaphysis` +3 dan `metadiaphysis` +2 (lihat catatan); `age_group:0-9`, `40-59`, `60+`; `transverse:central`, `eccentric`; `soft_tissue_mass:present` |
| Tidak dibahas | 22 | seluruh `cortex` (termasuk `saucerization`), seluruh `periosteal`, seluruh `density`, `matrix:osteoid` (hanya histologi), lainnya |

*Catatan lokasi longitudinal:* hanya 6 dari 17 berlabel "tengah" (diafisis); 10 berlabel proksimal atau distal tanpa keterangan metafisis atau metadiafisis. Seri ini tidak menunjukkan diafisis sebagai mayoritas yang jelas; bobot `diaphysis` +3 berbanding `metaphysis` 0 layak ditinjau sebagai kandidat hipotesis (tidak diterapkan; bobot dibekukan).

*Dibanding poster C-13882:* tambahan dukungan untuk `age_group:20-39`, `bone_class:flat_bone`, dan `matrix:chondroid`. `cortex:saucerization` +2 tetap tanpa sumber.

---

## Pembaruan 2026-11-22 (c): pencarian SciSpace untuk tiga celah yang tersisa

Keputusan pemilik: Revell dkk. 2002 **tidak didaftarkan** (tetap tercatat di bagian (b) sebagai bahan pembanding saja).

Tiga pencarian SciSpace (akses terbuka), lisensi diperiksa lewat metadata PubMed/PMC. **Hanya abstrak yang dibaca; belum ada klaim yang diperiksa terhadap teks penuh.**

| Celah | Kandidat | Lisensi (metadata PMC) | Catatan |
|---|---|---|---|
| Desmoplastic fibroma | Nedopil AJ dkk. 2013, Open Orthop J 7:40. doi 10.2174/1874325001307010040, PMC3583030 | CC BY-NC 3.0 | Laporan kasus dengan tinjauan pustaka; lokasi tersering mandibula dan metafisis tulang panjang; CT untuk korteks. Kandidat utama. Non-komersial (bendera yang sama dengan S-13, S-23). |
| Desmoplastic fibroma | Stefanidis K dkk. 2011, J Med Case Rep 5:28. doi 10.1186/1752-1947-5-28, PMC3033348 | CC BY 2.0 | Satu kasus (pria 56 tahun, dua lokasi), CT dan MRI. Terbuka penuh. |
| Desmoplastic fibroma | Kim OH dkk. 2013, Korean J Radiol 14(6):963. doi 10.3348/kjr.2013.14.6.963, PMC3835646 | CC BY-NC 3.0 | Satu kasus di falang distal kaki; radiograf dan MRI. Lokasi tidak lazim. |
| Desmoplastic fibroma | Kinoshita H dkk. 2020, Case Rep Orthop. doi 10.1155/2020/5380598, PMC7148584 | tidak tercantum di metadata (Hindawi; perlu dipastikan) | Satu kasus ilium. |
| Spondilitis TB | Rivas-Garcia A dkk. 2013, Eur Spine J 22 Suppl 4:567. doi 10.1007/s00586-012-2333-9, PMC3691403 | tanpa CC (© Springer) → `cite_only` | Isi terbaik: temuan pencitraan penyakit Pott. |
| Spondilitis TB | Garg RK, Somvanshi DS 2011, J Spinal Cord Med 34(5):440. doi 10.1179/2045772311Y.0000000023, PMC3184481 | tanpa CC → `cite_only` | Ulasan umum, termasuk usia dan regio. |
| Spondilitis TB | Mittal S dkk. 2016, Asian Spine J 10(4):734. doi 10.4184/asj.2016.10.4.734, PMC4995258 | CC BY-NC 3.0 | 40 pasien, TB atipikal vs metastasis; MRI, bukan radiograf. |
| Periosteal OS, `cortex:saucerization` | Liu XW dkk. 2015, Int J Clin Exp Med 8(1):37. PMID 25784972, PMC4358427 | tanpa CC (© IJCEM) → `cite_only` | Ulasan; abstrak menyebut erosi ekstrinsik pada korteks diafisis yang menebal dan reaksi periosteal tegak lurus; usia rata-rata sekitar 28. Tepat untuk klaim sauserisasi. |
| Periosteal OS, `cortex:saucerization` | Kitajima K dkk. 2018, Cureus 10(11):e3655. doi 10.7759/cureus.3655, PMC6351107 | CC BY 3.0 | Satu kasus (anak 10 tahun): radiograf menunjukkan penebalan korteks yang tererosi massa berdasar lebar. Terbuka penuh, tetapi satu kasus. |
| Periosteal OS | Assi T dkk. 2021, J Bone Oncol 30:100389. doi 10.1016/j.jbo.2021.100389, PMC8449265 | tidak tercantum di metadata (perlu dipastikan) | Ulasan naratif, memuat ciri radiologis. |

**Kesimpulan sementara.** Tidak ada ulasan radiografik ber-CC BY penuh untuk ketiga celah. Pilihan realistis: (1) Desmoplastic fibroma: Nedopil (CC BY-NC) ditambah Stefanidis (CC BY); (2) spondilitis TB: Rivas-Garcia sebagai `cite_only` ditambah Mittal (CC BY-NC); (3) sauserisasi: Liu sebagai `cite_only` ditambah Kitajima (CC BY). Semua perlu dibaca penuh sebelum didaftarkan. Menunggu keputusan pemilik.

---

## Pembaruan 2026-11-22 (d): enam kandidat dibaca dan dicocokkan dengan bobot (usulan; tidak ada yang diterapkan)

**Yang benar-benar dibaca.** Teks penuh lewat PubMed/PMC: Nedopil 2013, Stefanidis 2011, Kitajima 2018, Mittal 2016. **Hanya abstrak**: Liu 2015 dan Rivas-Garcia 2013 (PMC tidak menyediakan teks penuhnya; percobaan membuka halaman PMC tidak berhasil). Gambar tidak dapat dilihat lewat konektor; hanya keterangan gambar.

### D1. Desmoplastic fibroma (43 klaim) vs Nedopil 2013 + Stefanidis 2011

*Isi:* usia rata-rata 23 tahun, rentang 15 bulan sampai 75 tahun (tinjauan 184 kasus yang dikutip Nedopil); tersering pada tiga dekade pertama, kedua jenis kelamin setara. Lokasi: metafisis tulang panjang 56%, mandibula 22%, pelvis 12–13%; femur 15%, radius 12%, tibia 9%. Lesi litik; pada kedua kasus (CT) tampak sklerosis tepi, pseudotrabekulasi ringan, dan pada satu kasus ekspansi tulang. Terobosan korteks hanya pada 29% dari 83 kasus pustaka. Pertumbuhan ekstraoseus dapat terjadi tetapi tidak pada kasus Nedopil.

| Vonis | Jumlah | Klaim |
|---|---|---|
| Didukung | 10 | `age_group:20-39` +3; ketiga `age_group:10-19` +2; `bone_class:long_bone` +2, `flat_bone` +2, `craniofacial` +2; `longitudinal:metaphysis` +2; `density:lytic` +3; `cortex:focal_breach` +1 |
| Sebagian | 10 | `age_group:0-9`, `40-59`, `60+`; `transverse:juxtacortical_surface`, `juxtacortical_continuous`; `density:sclerotic`; `cortex:expansion_shell`, `destruction`, `intact`; `soft_tissue_mass:present` |
| Tidak dibahas | 22 | seluruh `periosteal`; seluruh `matrix`; `transverse:central`, `eccentric`, `cortical`; `margin_lodwick` selain IA; `longitudinal` selain metafisis; lainnya |
| Ketegangan ringan | 1 | `margin_lodwick:IA` 0 berbanding `IB` +2: kedua kasus menunjukkan sklerosis tepi (pada CT, dua kasus saja) |

Kandidat hipotesis (tidak diterapkan): `cortex:intact` 0 dapat dinaikkan, karena sekitar 71% kasus pustaka tanpa terobosan korteks; `margin_lodwick:IA` 0 ditinjau. Definisi entitas ("litik ekspansil dengan pseudotrabekulasi") sejalan dengan kedua sumber.

### D2. Skeletal tuberculosis (45 klaim) vs Mittal 2016 (teks penuh) + Rivas-Garcia 2013 (abstrak)

*Isi:* tulang belakang adalah lokasi tersering TB muskuloskeletal (sekitar separuh), disusul panggul dan lutut; torakal tersering; korpus vertebra bagian anterior-inferior sebagai lokasi awal; pola paradiskal, anterior, sentral; diskus relatif bertahan dibanding infeksi piogenik; abses paraspinal, intraoseus, dan epidural khas dan pada seri Mittal hanya ditemukan pada TB, tidak pada metastasis; keterlibatan beberapa segmen berurutan, lesi loncat 16–20%; vertebra sklerotik tergolong atipikal; kolaps dengan kifosis; kalsifikasi dalam abses (abstrak Rivas-Garcia). Usia rata-rata 40 tahun (11–67; Mittal, 20 pasien) dan 53 tahun (Rivas-Garcia, 48 pasien).

| Vonis | Jumlah | Klaim |
|---|---|---|
| Didukung | 4 | `age_group:40-59` +2; `bone_class:spine_body` +2; `soft_tissue_mass:present` +1; `multiplicity:multiple` +1 |
| Sebagian | 9 | `age_group:20-39`, `60+`, ketiga `10-19`; `bone_class:sacrum`; `density:lytic`, `sclerotic`; `cortex:destruction` |
| Tidak dibahas | 32 | `age_group:0-9`; tulang panjang, tangan-kaki, pipih; seluruh `longitudinal`, `transverse`, `margin_lodwick`, `periosteal`, `matrix`; `clinical_flags:fever_or_infection_signs` |

*Catatan penting:* (1) Mittal adalah studi MRI pada TB spinal **atipikal**, bukan radiograf; angka persentase pola vertebra di teksnya tidak konsisten satu sama lain, jadi tidak dipakai. (2) Ciri pembeda spondilitis TB yang disebut kedua sumber (diskus, segmen berurutan, abses paraspinal berkalsifikasi, penyebaran subligamen) **tidak ada dalam skema fitur kita**; ini pengamatan untuk opsi skema, bukan perubahan (skema hanya diubah atas persetujuan pemilik). (3) Kandidat hipotesis: `bone_class:spine_body` +2 dan `soft_tissue_mass:present` +1 mungkin terlalu rendah untuk TB.

### D3. Periosteal osteosarcoma (38 klaim) vs Kitajima 2018 (teks penuh) + Liu 2015 (abstrak)

*Isi:* dekade kedua sampai ketiga (Kitajima); usia rata-rata sekitar 28 (Liu). Femur dan tibia 85–95%, ulna dan humerus 5–10%. Gambaran radiologis: massa jaringan lunak berdasar lebar di permukaan yang mengerosi dari luar korteks diafisis yang menebal, dengan reaksi periosteal tegak lurus yang masuk ke komponen jaringan lunak. CT: matriks kondroid hipodens dengan kalsifikasi berbintik. Invasi medula jarang. Liu: semua lesi di diafisis; sepertiga proksimal femur tersering. Kasus Kitajima: anak 10 tahun, tibia; radiograf menunjukkan penebalan korteks yang tererosi massa berdasar lebar.

| Vonis | Jumlah | Klaim |
|---|---|---|
| Didukung | 11 | **`cortex:saucerization` +2**; ketiga `age_group:10-19` +3; `age_group:20-39` +2; `bone_class:long_bone` +3; `longitudinal:diaphysis` +3; `transverse:juxtacortical_surface` +3; `soft_tissue_mass:present` +2; `periosteal:spiculated` +3; `matrix:chondroid` +2 |
| Sebagian | 12 | `age_group:40-59`, `60+`; `bone_class:flat_bone`; `longitudinal:metadiaphysis`, `metaphysis`, `epiphysis_apophysis`; `transverse:central`, `eccentric`; `soft_tissue_mass:absent`; `periosteal:none`, `present_unspecified`; `matrix:osteoid` |
| Tidak dibahas | 15 | `periosteal:codman`, `lamellated`, `solid_thin`; seluruh `density`; `cortex` selain sauserisasi; lainnya |

*Catatan:* (1) `cortex:saucerization` kini punya sumber terbuka (Kitajima, CC BY 3.0), tetapi kalimat umumnya adalah kutipan sekunder dalam laporan satu kasus; rumusan Liu hampir sama, sehingga keduanya tampaknya menyatakan ulang satu deskripsi yang lebih lama. (2) Soal diafisis: Kitajima dan Liu mendukung `diaphysis` +3, sedangkan seri Revell (bagian b) hanya menunjukkan 6 dari 17 di tengah batang. Kandidat hipotesis diafisis berbanding metafisis tetap terbuka, kini dengan bukti dua arah.

### Ringkasan lisensi bila pemilik ingin mendaftarkan
Nedopil CC BY-NC 3.0; Stefanidis CC BY 2.0; Kitajima CC BY 3.0; Mittal CC BY-NC 3.0; Liu dan Rivas-Garcia tanpa lisensi CC (`cite_only`, dan baru abstraknya yang dibaca).

---

## Pembaruan 2026-11-22 (e): tiga sumber didaftarkan (KB 0.6.2, sumber saja)

Atas persetujuan pemilik: **S-33** Kitajima 2018, **S-34** Nedopil 2013, **S-35** Stefanidis 2011 terdaftar di `data/sources.json` (registri 0.4.0, 35 entri). S-33 dikutip pada 11 klaim Periosteal osteosarcoma (daftar "didukung" di D3); S-34 pada 10 dan S-35 pada 9 klaim Desmoplastic fibroma (daftar "didukung" di D1; `longitudinal:metaphysis` hanya S-34). Klaim "sebagian" **tidak** dikutip, karena ketiganya laporan kasus. Bobot, prior, dan aturan identik dengan 0.6.0.

Belum selesai: Liu 2015 dan Rivas-Garcia 2013 menunggu PDF dari pemilik untuk dibaca penuh; Mittal 2016 belum didaftarkan; Skeletal tuberculosis masih tanpa sumber radiografik.

---

## Pembaruan 2026-11-22 (f): Liu 2015 dan Rivas-Garcia 2013 dibaca penuh dari PDF pemilik (usulan; tidak ada yang diterapkan)

### F1. Rivas-Garcia dkk. 2013, *Imaging findings of Pott's disease* (Eur Spine J; 12 halaman)

*Lisensi:* PDF memuat "© Springer-Verlag 2012", tanpa lisensi CC → hanya dapat `cite_only`.
*Jenis bukti:* ulasan pencitraan dengan seri sendiri, 48 pasien (31 radiograf, 37 CT). Punya bagian khusus radiografi dan CT. **Sumber radiografik yang selama ini tidak ada untuk Skeletal tuberculosis.**

*Isi yang relevan:* tulang belakang terkena pada lebih dari separuh TB muskuloskeletal; terutama dewasa, tanpa dominasi jenis kelamin; torakal lalu lumbal. Khas dua korpus berurutan dengan diskus di antaranya; keterlibatan tiga vertebra atau lebih tidak jarang dan menjadi ciri penyakit. Radiograf dapat normal pada tahap awal, tetapi sering sudah abnormal saat pemeriksaan pertama. Temuan paling awal: lusensi dan kaburnya lempeng ujung. Temuan tersering: destruksi korpus (terutama anterior), penyempitan diskus, erosi lempeng ujung, geode, sekuestrum, sklerosis, massa paravertebra. Kalsifikasi dalam massa paraspinal sangat mengarah ke TB. Tahap lanjut: sklerosis reparatif, ankilosis, kolaps, kifosis. Atipikal: vertebra "gading", lesi sentral tanpa diskus, keterlibatan arkus saja (2–10%), lesi tidak berurutan. Dibanding piogenik: tepi destruksi lebih tegas tanpa sklerosis reaktif. Massa atau abses paraspinal 45–100%; pada seri sendiri 95% studi CT, berkalsifikasi 46%. Pola destruktif pada 70% radiograf. Satu segmen (15) sedikit lebih sering daripada multilevel (14). Usia rata-rata 53 tahun.

| Vonis | Jumlah (dari 45) | Klaim |
|---|---|---|
| Didukung | 8 | `bone_class:spine_body` +2; `age_group:40-59` +2; `density:lytic` +2, `mixed` +1, `sclerotic` −2; `cortex:destruction` +2; `soft_tissue_mass:present` +1; `multiplicity:multiple` +1 |
| Sebagian | 9 | `age_group:20-39`, `60+`, `0-9`, ketiga `10-19`; `margin_lodwick:IB`, `IC`; `clinical_flags:fever_or_infection_signs` (hanya "gejala konstitusional") |
| Tidak dibahas | 28 | tulang panjang, tangan-kaki, pipih, sakrum; seluruh `longitudinal`, `periosteal`, `matrix`; nilai `transverse`, `margin`, `cortex` lainnya |

*Catatan:* (1) Dibanding Mittal (4 didukung), sumber ini jauh lebih kuat dan langsung membahas radiograf. (2) Kandidat hipotesis diperkuat: `soft_tissue_mass:present` +1 terlalu rendah untuk TB (45–100%). (3) Awal infeksi di sudut anterolateral korpus, bukan di tengah; `transverse:central` +2 berbanding `eccentric` +1 sulit diterapkan pada vertebra (pengamatan). (4) Pengamatan skema dari bagian (d) dikuatkan: penyempitan diskus, keterlibatan segmen berurutan, dan kalsifikasi massa paraspinal adalah ciri kunci yang tidak ada dalam skema fitur. Skema tidak diubah.

### F2. Liu dkk. 2015, *Periosteal osteosarcoma: a review of clinical evidence* (Int J Clin Exp Med; 8 halaman)

*Lisensi:* tidak ada pernyataan lisensi CC di PDF → hanya dapat `cite_only`.

*Isi yang relevan:* dekade kedua dan ketiga; puncak 15–30 tahun; tibia 40%, femur 38%, ulna dan humerus 5–10%. Radiografi: massa jaringan lunak berdasar lebar, erosi ekstrinsik dan *scalloping* pada korteks diafisis yang menebal, reaksi periosteal tegak lurus yang masuk ke massa; derajat mineralisasi massa bervariasi. Tabel pembeda: korteks menebal dan utuh, matriks berspikula yang memancar dari korteks.

*Masalah mutu: ulasan ini bertentangan dengan dirinya sendiri.* Abstrak menyebut semua lesi di diafisis; bagian lokasi menyebut lesi terutama metafisis dan jarang diafisis. Bagian lokasi menyebut hanya di tulang panjang, lalu membahas kranium, mandibula, klavikula, kalkaneus. Satu tempat menyebut dominasi laki-laki 2:1, tempat lain menyebut tidak ada predileksi jenis kelamin. Reaksi periosteal tersering disebut tidak agresif dan padat, sementara kalimat lain menekankan reaksi tegak lurus.

| Vonis | Jumlah (dari 38) | Klaim |
|---|---|---|
| Didukung | 9 | `cortex:saucerization` +2; ketiga `age_group:10-19` +3; `age_group:20-39` +2; `bone_class:long_bone` +3; `transverse:juxtacortical_surface` +3; `soft_tissue_mass:present` +2; `periosteal:spiculated` +3 |
| Bertentangan di dalam sumber | 3 | `longitudinal:diaphysis` +3, `metaphysis` 0; `periosteal:solid_thin` −2 |
| Sebagian atau tidak dibahas | 26 | lainnya |

**Saran:** jangan daftarkan Liu 2015. Ia tidak menambah apa pun di atas S-33 untuk sauserisasi, dan pertentangan internalnya membuatnya tidak layak dijadikan dasar bobot. Soal diafisis berbanding metafisis tetap terbuka (Kitajima: diafisis; Revell: 6 dari 17 di tengah batang; Liu: tidak dapat dipakai).

**Saran:** daftarkan Rivas-Garcia 2013 sebagai `cite_only` dan kutip pada 8 klaim Skeletal tuberculosis yang didukung. Menunggu keputusan pemilik.

---

## Pembaruan 2026-11-22 (g): S-36 didaftarkan (KB 0.6.3, sumber saja)

Atas persetujuan pemilik: **S-36** Rivas-Garcia 2013 terdaftar sebagai `cite_only` (registri 0.5.0, 36 entri) dan dikutip pada 8 klaim Skeletal tuberculosis berstatus "didukung" di F1. Klaim "sebagian" tidak dikutip. Liu 2015 tidak didaftarkan. Bobot, prior, dan aturan identik dengan 0.6.0.
