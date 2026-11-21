# Serah terima — keadaan per 2026-11-22 (KB 0.6.4)

Dokumen ini untuk memulai sesi baru tanpa kehilangan konteks. Baca bersama `claude/README.md`, `claude/CHANGELOG.md`
dan `docs/HANDOFF-UI.md` (pekerjaan UI; masih berlaku, langkah berikutnya di sana belum dikerjakan).

## 1. Ringkas

- **KB 0.6.4.** Sejak 0.6.0 hanya daftar sumber (`source_ids`) dan `data/sources.json` yang berubah. Bobot, prior,
  aturan, fitur, dan UI **identik dengan 0.6.0** (aturan isian v0.6.3, tema v0.6.7).
- **41 sumber** (S-01 … S-41): 31 `verified`, 10 `cite_only`.
- Dua tinjauan selesai dan **tidak diterapkan**: tinjauan skor (34 hipotesis) dan pemeriksaan sumber teks lengkap.
- GitHub `harmenreza/TumTul`, prototipe publik, matriks skor, dan proyek semuanya di KB 0.6.4.
- Skema data **v1.2.0** sejak 2026-11-22 (tiga nilai lisensi ditambahkan; lihat §2). `validate_kb.py` lolos.

## 2. Sudah selesai: enum lisensi di skema (skema v1.2.0)

Tiga sumber yang didaftarkan sesi ini (S-33 `CC BY 3.0`, S-34 `CC BY-NC 3.0`, S-35 `CC BY 2.0`) memakai nilai lisensi
di luar enum skema v1.1.0, sehingga `tools/validate_kb.py` gagal dengan 3 kesalahan. Penyebabnya: validator dan skema
hanya ada di proyek, dan tidak dijalankan sebelum sumber didaftarkan.

Pemilik menyetujui perubahan skema pada 2026-11-22: ketiga nilai itu ditambahkan ke enum `license`
(`schema/kb-schema.json` **v1.2.0**; tidak ada perubahan lain, tidak ada berkas data yang berubah). Kini
`validate_kb.py` mencetak OK (37 entitas, 1584 klaim, 5 aturan) dan `score_smoke.py` mencetak 20/20 (19 langsung,
ditambah satu seri yang disengaja: vinyet osteomielitis seri dengan Ewing, dihitung sebagai peringkat pertama).

Skema, `validate_kb.py`, dan `score_smoke.py` sudah ada di repo GitHub. Kedua skrip diketik ulang dari salinan proyek
dan diverifikasi dengan menjalankannya, bukan dengan pembandingan bita; salinan proyek tetap yang asli. **Generator
(`build_entities_batch1.py`, `build_entities_batch2.py`) belum ada di repo**: terlalu panjang untuk diketik ulang
dengan aman (memuat semua bobot). Cara aman: pemilik mengunduh keduanya dari proyek dan melampirkannya, lalu disalin
apa adanya.

## 3. Di mana semuanya

| Benda | Lokasi | Keadaan |
|---|---|---|
| Repo | https://github.com/harmenreza/TumTul (PR #1 dan #2 digabung; PR #3 memuat skema v1.2.0, validator, dan dokumen ini) | KB 0.6.4 |
| Prototipe publik | https://claude.ai/artifact/DsM6XAJos65GTAABAw79AX (slug `68353c8b-eab6-4b88-b328-135642ca0238`, publik) | versi artifact 20, KB 0.6.4 |
| Matriks skor | https://claude.ai/artifact/Do4A9wGh2uZFZzU9UxN8yv (slug `679bd2cb-b6e3-4dc5-a635-9ee1979562f9`, pribadi) | versi 6, KB 0.6.4 |
| Papan alur skor | https://claude.ai/artifact/DajnwWgBN7vsYrBBA2SKqF (slug `65e39472-dfa7-4d0c-a96a-de524e17838e`) | digambar tangan; tidak berubah |
| Proyek claude.ai | dokumen proyek ini | data, tools, docs, dan `web/index.html` di KB 0.6.4 |

**Hanya ada di proyek, tidak di repo GitHub** (diperiksa 2026-11-22): `schema/kb-schema.draft.json`,
`tools/build_entities_batch1.py`, `tools/build_entities_batch2.py`, `tools/validate_cases.py`, `tools/build_form.py`, `tools/sample_size_p1.py`, `web/form_template.html`, seluruh
`data/validation/`, serta `docs/SKEMA-DIAGNOSIS.md`, `docs/VALIDASI-*`, `docs/validation-brief*`,
`docs/FORMULIR-KASUS-PRAKTIK.md`, `docs/PROPOSAL-VALIDASI-PRAKTIK.md`. Ambil dengan `project_read` bila perlu.
Skema, validator, dan uji asap sudah masuk repo (PR #3); generator dan data validasi belum.

**Hanya ada di repo, tidak di proyek:** `web/matrix.html` (hasil build), `web/img/` (66 gambar),
`docs/tinjauan-skor-v0.6-keluaran.txt` dan `docs/tinjauan-sumber-v0.6-keluaran.txt` (keluaran skrip tinjauan),
serta folder kandidat gambar (`candidates/`, `candidates_pmc/`, `hires/`, `pool_sizes/`).

**Ada di keduanya:** `data/entities/`, `data/features.json`, `data/images.json`, `data/sources.json`, `tools/` lain,
`web/template.html`, `web/index.html`, `web/matrix_template.html`, dokumen tinjauan dan usulan, README, LICENSES,
CHANGELOG (di proyek ketiganya berada di `claude/`).

## 4. Angka KB (dicetak `tools/build_matrix.py`; tidak berubah sejak 0.6.0)

| Butir | Jumlah |
|---|---|
| Entitas | 37 |
| Nilai fitur yang ditawarkan di aplikasi | 62 |
| Klaim berbobot | 1584 (+ 4 klaim `not_applicable` berbobot 0) |
| +3 / +2 / +1 / 0 / −2 / −5 | 192 / 248 / 382 / 179 / 257 / 322 |
| Aturan khusus | 5 (Ewing ×2, osteomielitis, osteosarkoma telangiektatik, limfoma) |
| Entitas dengan prior ≠ 0 | 16 (7 pada −2, 9 pada −1) |

Bila angka ini berbeda setelah build ulang, KB sudah berubah: periksa CHANGELOG sebelum menerbitkan.

## 5. Yang dikerjakan (2026-11-21 dan 22)

1. **Dua tampilan referensi skor** (hanya membaca): papan alur dan matriks 37 entitas × 62 nilai fitur
   (`tools/build_matrix.py`, `web/matrix_template.html`). Label matriks berbahasa Inggris, tema Negatoskop.
2. **Tinjauan skor KB 0.6.0** — `docs/TINJAUAN-SKOR-v0.6.md`: 34 hipotesis v0.7 (H-01 … H-34) dan 7 opsi skema
   (S-1 … S-7). Temuan utama: temuan normal berbobot +3 pada 16 klaim (H-01); over-calling CMF dan GCTB struktural
   (H-02, H-03); 65 hard constraint meragukan dan 8 tidak konsisten dari 322; `ground_glass` menyingkirkan 27 dari 37
   entitas; 41,7% klaim hanya mengutip S-01. Dikerjakan agen terpisah; klasifikasi a/b/c, vinyet, dan simulasi belum
   diperiksa siapa pun selain agen itu.
3. **Pemeriksaan sumber teks lengkap** — `docs/TINJAUAN-SUMBER-v0.6.md`: pada sampel acak 40 klaim, 9 didukung, 11
   sebagian, 20 tidak ditemukan. Bertentangan dengan sumbernya sendiri: Chondroblastoma `soft_tissue_mass:present`
   −5 (S-06), Fibrous dysplasia `margin_lodwick:IC` −5 (S-22), Telangiectatic osteosarcoma `margin_lodwick:IA` −5
   (S-15). Dokumen ini menggambarkan KB 0.6.0; `tools/review_sources.py` berhenti pada baris CMF bila dijalankan
   pada 0.6.1 ke atas (memang diharapkan).
4. **Perbaikan sumber, KB 0.6.1 → 0.6.4** — rincian dan vonis per klaim di `docs/USULAN-SUMBER-v0.7.md` (bagian A
   sampai (i)). Semua lewat `tools/apply_source_overrides.py`; bobot terbukti identik setiap kali.

| KB | Sumber baru | Entitas | Klaim yang dikutip |
|---|---|---|---|
| 0.6.1 | S-18 menggantikan S-06 | Chondromyxoid fibroma | S-06 dihapus dari 44, S-18 pada 19 |
| 0.6.1 | S-31 Ariyaratne 2023 (CC BY 4.0) | Chordoma | 20 (11 didukung, 9 arah saja) |
| 0.6.1 | S-32 Ariyaratne 2023 (CC BY 4.0) | Vertebral haemangioma | 8 (3 dan 5) |
| 0.6.2 | S-33 Kitajima 2018 (CC BY 3.0) | Periosteal osteosarcoma | 11, termasuk `cortex:saucerization` |
| 0.6.2 | S-34 Nedopil 2013 (CC BY-NC 3.0), S-35 Stefanidis 2011 (CC BY 2.0) | Desmoplastic fibroma | 10 dan 9 |
| 0.6.3 | S-36 Rivas-Garcia 2013 (`cite_only`) | Skeletal tuberculosis | 8 |
| 0.6.4 | S-37 Pattamapaspong 2024, S-38 Abid 2024 (`cite_only`), S-39 Semionov 2022 (CC BY 4.0) | Skeletal tuberculosis | 20, 18, 8 (27 dari 45 klaim kini bersumber khusus) |
| 0.6.4 | S-40 Frick 2005 (`cite_only`), S-41 Ipponi 2025 (CC BY 4.0) | Desmoplastic fibroma | 16, 10 (19 dari 43) |

Kebiasaan pengutipan: untuk S-31 dan S-32 (ulasan pencitraan) klaim "arah saja" ikut dikutip; sejak S-33 hanya klaim
"didukung" yang dikutip.

**Dibaca tetapi sengaja tidak didaftarkan:** Revell 2002 (keputusan pemilik), Liu 2015 (bertentangan dengan dirinya
sendiri), Mittal 2016 (MRI TB atipikal), Butt 2025 (tuberkuloma jaringan lunak), Sindhura 2026 (tanpa lisensi, tidak
menambah), Khan 2012 (tidak relevan untuk celah; gambarnya CC BY 3.0 dan mungkin layak ditinjau untuk galeri), dua
poster EPOS (C-1421, C-13882; lisensi terbuka belum terlihat di halamannya). PDF kiriman pemilik tidak disimpan di
proyek.

## 6. Keputusan yang menunggu pemilik

1. **Generator ke repo**: lampirkan `build_entities_batch1.py` dan `build_entities_batch2.py` dari proyek agar dapat
   disalin apa adanya (§2).
2. **Hipotesis H-01 … H-34**: mana yang dipertahankan, dibuang, atau diubah. H-02 dan H-03 harus diuji sebelum hard
   constraint CMF dilonggarkan. Bobot dibekukan oleh protokol validasi; hipotesis diuji pada kasus praktik, bukan
   disetel ke kasus v1–v4.
3. **Kandidat hipotesis baru dari pembacaan sumber** (belum bernomor, belum diterapkan):
   - Vertebral haemangioma `cortex:destruction` −5 → −2 (hemangioma agresif; S-32).
   - Chordoma `matrix:none` +2 diturunkan (kalsifikasi berbintik sering; S-31).
   - Skeletal tuberculosis: `periosteal:lamellated` −2 dinaikkan (khas pada anak); `soft_tissue_mass:present` +1 dan
     `bone_class:spine_body` +2 terlalu rendah; `margin_lodwick:IC` +2 berbanding `IA`/`IB` +1 ditinjau;
     `clinical_flags:fever_or_infection_signs` +2 mungkin terlalu tinggi di luar tulang belakang.
   - Desmoplastic fibroma: `longitudinal:epiphysis_apophysis` −2 dinaikkan (5 dari 27, lebih sering daripada
     diafisis); `margin_lodwick:IA` 0 dinaikkan (tepi sklerotik 46%); `cortex:expansion_shell` +2 ditinjau;
     `soft_tissue_mass:present` 0 dan `cortex:focal_breach` +1 mungkin terlalu rendah.
   - Periosteal osteosarcoma: diafisis berbanding metafisis. S-15 dan S-33 mendukung diafisis atau metadiafisis;
     seri Revell hanya 6 dari 17 di tengah batang. Belum ada alasan mengubah bobot.
4. **Opsi skema untuk spondilitis TB**: penyempitan diskus, keterlibatan segmen berurutan, dan massa paraspinal
   berkalsifikasi adalah ciri kunci menurut S-36, S-37, S-38, dan tidak ada dalam skema fitur. Pengamatan saja.
5. **Lisensi dua poster EPOS**: perlu dipastikan di halaman posternya sebelum didaftarkan.
6. Yang lama dan masih terbuka: langkah UI no. 2 di `docs/HANDOFF-UI.md`; keputusan pada proposal validasi praktik.

## 7. Celah sumber yang tersisa

- Desmoplastic fibroma: seluruh `periosteal` (5 klaim) dan `matrix:ground_glass`.
- Skeletal tuberculosis: seluruh `matrix`, sebagian `transverse`, `periosteal:spiculated`, `codman`.
- Periosteal osteosarcoma: `periosteal:codman`, `lamellated`, seluruh `density`.
- Vertebral haemangioma: usia dan tepi (23 dari 32 klaim tidak dibahas S-32).
- Entitas yang hanya mengutip S-01 (H-26) belum disentuh.

## 8. Cara bekerja di sesi baru

- **Repo**: klon `harmenreza/TumTul`. Untuk mendorong, repo harus ditambahkan ke sesi dengan akses tulis (pemilik
  memberi akses GitHub); selalu lewat cabang dan pull request, pemilik yang menggabung.
- **Urutan build**: `build_entities_batch2.py` → `apply_source_overrides.py` → `validate_kb.py` → `score_smoke.py`
  (20/20, termasuk satu seri yang disengaja) → `build_web.py` → `build_matrix.py`. Generator hanya ada di proyek.
  Generator menghasilkan keadaan sumber 0.6.0; `apply_source_overrides.py` mengembalikannya ke 0.6.4
  (`--check` untuk memeriksa). Jalur dari keluaran generator ini belum diuji ulang sejak 0.6.1.
- **Jalankan `validate_kb.py` sebelum mendaftarkan sumber atau mengubah KB.** Pelajaran sesi ini (§2).
- **Format berkas**: entitas di proyek indent 2 dengan baris baru di akhir; di repo indent 1 tanpa baris baru.
  `data/sources.json` di proyek memuat `registry_version` (kini 0.6.0), `updated`, `note`; di repo hanya `sources`.
  Jangan menimpa salinan proyek dengan salinan repo; serialkan ulang (sesi ini memakai folder `.project_out/`).
- **Menulis ke proyek**: dokumen yang sudah ada harus dibaca dulu dengan `project_read` di percakapan yang sama.
  README, LICENSES, CHANGELOG ada di `claude/`.
- **Menerbitkan**: prototipe publik dikirim hanya `index.html`, mode patch, dengan `shared_live: "public"` dan judul
  artifact "TumTul"; matriks dikirim `web/matrix.html` sebagai `index.html`. Uji tanpa kepala pada 400 px dulu.
- **Mencari dan membaca sumber**: konektor PubMed (teks penuh hanya untuk sebagian PMC; wajib menyebut PubMed dan
  menautkan DOI), SciSpace (pencarian), EPOS lewat alamat `…/<nomor>/findings%20and%20procedure%20details`.
  Halaman PMC menolak pengambilan berulang. Cara paling andal: pemilik melampirkan PDF.
- **Vonis pemeriksaan sumber**: didukung / sebagian (arah saja) / tidak ditemukan / bertentangan. Nyatakan ulang
  dengan kata sendiri; jangan menyalin kalimat sumber.

## 9. Aturan tetap

Alat referensi/edukasi, bukan alat diagnostik; tidak pernah satu diagnosis; alasan dan sumber selalu tampil; tidak
menganalisis gambar, tidak menyimpan data pasien; tanya pemilik sebelum mengubah skema data; README, LICENSES,
CHANGELOG diperbarui setiap perubahan; tidak ada klaim akurasi (bobot belum memenuhi kriteria uji terdaftar v3 dan
v4); bobot dibekukan pada 0.6.0 sampai diuji pada kasus praktik.

## 10. Kalimat pembuka yang disarankan untuk sesi baru

> Lanjutkan TumTul dari `docs/HANDOFF-SKORING.md` (keadaan KB 0.6.4, skema v1.2.0). Saya lampirkan dua generator
> untuk dimasukkan ke repo; setelah itu kita bahas hipotesis mana yang masuk v0.7.
