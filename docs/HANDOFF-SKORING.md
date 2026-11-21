# Serah terima sesi skoring — 2026-11-21

Dokumen ini untuk memulai sesi baru tanpa kehilangan konteks. Baca bersama `claude/README.md`, `claude/CHANGELOG.md`
dan `docs/HANDOFF-UI.md` (pekerjaan UI; masih berlaku, langkah berikutnya di sana belum dikerjakan).

## Yang dikerjakan di sesi ini

Dua tampilan referensi sistem skor. Keduanya hanya membaca; bobot, entitas, fitur, UI aplikasi dan skema data
**tidak berubah** (KB tetap 0.6.0, skema v1.1.0, aturan isian v0.6.3).

1. **Diagram alur skor** (Whiteboard "TumTul scoring flow"): https://claude.ai/artifact/DajnwWgBN7vsYrBBA2SKqF
   - Kiri ke kanan: fitur pembaca → aturan isian UI → dua jalur.
   - Sumbu A: 4 fitur, 0–9 poin, tiga kelas (0–1 non-agresif, 2–3 indeterminate, ≥4 agresif).
   - Sumbu B: skor 37 entitas (prior + bobot fitur + aturan) → ada bobot −5? → ya: daftar disingkirkan (tetap
     ditampilkan dengan alasan; maks. 3 baris abu-abu di daftar utama) / tidak: daftar kompatibel (5 teratas + semua
     yang seri dengan peringkat 5, maks. 10; seri berbagi peringkat).
   - Warna: biru = masukan pembaca, peach = dihitung aplikasi, abu-abu = disingkirkan, kuning = tampil di layar.
   - Digambar tangan dari `docs/SKEMA-DIAGNOSIS.md` §4 dan `web/template.html`. Tabel poin Sumbu A dan nilai prior
     tidak ada di papan. Belum dilihat hasil rendernya oleh Claude; blok atau panah mungkin perlu digeser.
2. **Matriks skor lengkap** (artifact "TumTul scoring matrix"): https://claude.ai/artifact/Do4A9wGh2uZFZzU9UxN8yv
   - 37 entitas (baris) × 62 nilai fitur (kolom), bobot berwarna +3 … −5, kolom prior prevalensi.
   - Di bawah matriks: 5 aturan khusus, prior per kelas, tabel poin Sumbu A.
   - Ketuk sel: catatan (bahasa Indonesia, apa adanya dari KB) dan kode sumber. Ketuk nama entitas: prior, ciri khas
     (+3), jumlah hard constraint dan aturan.
   - Saring menurut perilaku; urut menurut kelompok WHO, nama, atau jumlah hard constraint.
   - Label dan judul berbahasa Inggris; tema Negatoskop, terang dan gelap.
   - Nilai `not_applicable` tidak digambar (4 klaim, semuanya 0).

3. **Tinjauan skor KB 0.6.0** (atas permintaan pemilik; dikerjakan satu agen terpisah dengan effort tinggi, diperiksa
   sesi utama): `docs/TINJAUAN-SKOR-v0.6.md`.
   - Tinjauan konsistensi dan kewajaran, **bukan validasi; tidak ada yang diterapkan.**
   - Hasil: 34 hipotesis v0.7 (H-01 … H-34) dan 7 opsi tingkat skema (S-1 … S-7, perlu persetujuan pemilik).
   - Temuan utama: temuan normal (`cortex:intact`, `periosteal:none`, `matrix:none`) berbobot +3 pada 16 klaim (H-01);
     over-calling CMF dan GCTB bersifat struktural (H-02, H-03); plafon skor 14–26; 65 hard constraint meragukan dan
     8 tidak konsisten dari 322 (H-06 … H-18); `ground_glass` menyingkirkan 27 dari 37 entitas; aturan jaringan lunak
     Ewing/limfoma selalu menyala lewat `focal_breach` (H-05); 41,7% klaim hanya mengutip S-01, dan 44 dari 46 klaim
     CMF mengutip S-06 yang tidak membahas CMF (H-26).
   - Berkas: `tools/review_scoring.py` (± 2 menit; mencetak semua angka laporan),
     `docs/tinjauan-skor-v0.6-hard-constraints.csv`, `tools/review_cases_v1_v4.txt`. Keluaran lengkap skrip (138 KB)
     tidak disimpan; buat ulang dengan `python3 tools/review_scoring.py > docs/tinjauan-skor-v0.6-keluaran.txt`.
   - Yang belum diperiksa siapa pun selain agen peninjau: klasifikasi a/b/c tiap hard constraint, 48 vinyet buatan,
     simulasi input jarang, dan sebagian besar uji petik sumber. S-18 dan lima sumber lain tidak dibaca.
   - **Langkah berikutnya ada pada pemilik:** menilai hipotesis mana yang dipertahankan, dibuang atau diubah. H-02 dan
     H-03 harus diuji sebelum hard constraint CMF dilonggarkan. H-22, H-26, H-27, H-28, H-34 tidak memerlukan penilaian
     klinis (konsistensi, sumber, teks alasan), tetapi tetap perubahan KB dan belum dikerjakan.

4. **Pemeriksaan sumber teks lengkap** (2026-11-22; agen terpisah effort tinggi, diperiksa sesi utama):
   `docs/TINJAUAN-SUMBER-v0.6.md`. Menjawab apakah sumber yang DIKUTIP mendukung klaimnya, bukan apakah bobotnya benar
   secara klinis. **Tidak ada yang diterapkan; `data/sources.json` tidak diubah.**
   - Dibaca penuh: 14 artikel dari PubMed Central dan S-18 dari PDF kiriman pemilik. Hanya S-21 yang belum dibaca.
   - 312 klaim diperiksa. Set D (40 klaim acak, satu-satunya yang tak bias): 9 didukung, 11 sebagian, 20 tidak
     ditemukan. Set B (192 klaim +3): 107 / 51 / 34. Set A (73 hard constraint bertanda): 3 / 28 / 39, dan 3 bertentangan.
   - Bertentangan dengan sumbernya sendiri: Chondroblastoma `soft_tissue_mass:present` −5 (S-06), Fibrous dysplasia
     `margin_lodwick:IC` −5 (S-22), Telangiectatic osteosarcoma `margin_lodwick:IA` −5 (S-15).
   - Tanpa sumber radiografik sama sekali: Chordoma, Desmoplastic fibroma, Skeletal tuberculosis. Hanya lokasi:
     Vertebral haemangioma, Periosteal osteosarcoma. S-18 memuat bagian CMF tetapi hanya dikutip 1 dari 46 klaim CMF.
   - Hipotesis: H-06, H-08 (osteomielitis), H-09, H-10, H-11, H-12 (telangiektatik), H-14, H-16, H-26 dikuatkan;
     H-13 (BPOP `juxtacortical_continuous`) dan H-15 (bobotnya) dilemahkan.
   - Berkas: `tools/review_sources.py`, `tools/review_source_evidence.tsv`, `tools/review_source_coverage.tsv`,
     `docs/tinjauan-sumber-v0.6.csv`. PDF S-18 tidak disimpan di proyek (hanya dibaca di sesi); minta lagi ke pemilik
     bila perlu, atau pakai DOI 10.1067/j.cpradiol.2023.01.005.
   - Belum diperiksa siapa pun selain agen: vonis yang bersandar pada 12 sumber selain S-06 dan S-18; isi gambar
     (S-01 Fig. 1 dan 3) tidak terbaca oleh konektor.
   - **Langkah berikutnya yang tidak butuh penilaian klinis:** mengutip ulang klaim CMF ke S-18; mencari sumber
     radiografik berlisensi terbuka untuk entitas tanpa sumber. Keduanya mengubah KB, jadi menunggu keputusan pemilik.

5. **Usulan perbaikan sumber** (2026-11-22, menunggu keputusan pemilik; belum diterapkan): `docs/USULAN-SUMBER-v0.7.md`.
   - Bagian A **disetujui pemilik dan diterapkan sebagai KB 0.6.1 (sumber saja)**: S-06 dihapus dari 44 klaim CMF,
     S-18 ditambah pada 19. Skor identik dengan 0.6.0. Diterapkan lewat `tools/apply_source_overrides.py` (jalankan
     setelah generator; `--check` untuk memeriksa). `tools/build_web.py` kini `kb_version` 0.6.1 dan `web/index.html`
     sudah dibangun ulang. **Prototipe publik sudah diterbitkan ulang** atas izin pemilik (versi artifact 17; slug
     `68353c8b-eab6-4b88-b328-135642ca0238`, status publik; hanya `index.html` yang dikirim, mode patch, setelah
     SHA-256 `index.html` terbitan dicocokkan dengan build repo sebelumnya). Salinan `web/index.html` di proyek masih
     build 0.6.0.
   - Bagian B2 **disetujui dan diterapkan (tetap KB 0.6.1)**: S-31 dan S-32 (dua ulasan Ariyaratne dkk. 2023) terdaftar
     di `data/sources.json` (registri 0.3.0; salinan proyek memuat `registry_version`, `updated`, `note`, sedangkan
     salinan repo hanya `sources` — jangan menimpa salinan proyek dengan salinan repo). S-31 pada 20 klaim Chordoma,
     S-32 pada 8 klaim Vertebral haemangioma. Kandidat hipotesis baru, belum diterapkan: haemangioma
     `cortex:destruction` −5 → −2; Chordoma `matrix:none` +2 diturunkan.
   - Dua poster EPOS utama sudah disaring lewat ringkasan halaman (C-13882 untuk osteosarkoma periosteal: 10 dari 38
     klaim didukung; C-1421 untuk TB: 4 dari 45). Tulisan lisensi terbuka tidak terlihat di halamannya: `cite_only`
     sampai dipastikan. Belum didaftarkan.
   - Berkas entitas di proyek berformat indent 2; di repo indent 1. Ubah lewat `.project_out/` seperti sesi ini, atau
     bangun ulang dari generator lalu jalankan `tools/apply_source_overrides.py`.
   - Bagian C (usulan): poster EPOS. ECR 2014+ berlisensi terbuka non-komersial berbagi-serupa; sebelum itu
     `cite_only`. Kandidat utama: ECR 2019 C-1421 (TB) dan ECR 2022 C-13882 (osteosarkoma permukaan). Belum dibaca penuh.
     Bagian poster dapat dibuka di alamat `…/<nomor>/findings%20and%20procedure%20details`.
   - Bagian B (**belum selesai**): kandidat utama untuk Chordoma dan Vertebral haemangioma adalah dua ulasan
     Ariyaratne dkk. 2023 di Diagnostics (CC BY 4.0), baru dibaca abstraknya. Belum ada sumber memadai untuk
     Desmoplastic fibroma, Skeletal tuberculosis, Periosteal osteosarcoma.
   - Langkah berikutnya: baca teks lengkap kedua ulasan itu (PMC10217758, PMC10297602) dan periksa klaimnya; lakukan
     pencarian khusus untuk tiga entitas sisanya. Halaman PMC menolak WebFetch berulang; pakai konektor PubMed.

## Angka KB 0.6.0 (dicetak oleh `tools/build_matrix.py`)

| Butir | Jumlah |
|---|---|
| Entitas | 37 |
| Nilai fitur yang ditawarkan di aplikasi | 62 |
| Klaim berbobot | 1584 (+ 4 klaim `not_applicable` berbobot 0) |
| +3 / +2 / +1 / 0 / −2 / −5 | 192 / 248 / 382 / 179 / 257 / 322 |
| Aturan khusus | 5 (Ewing ×2, osteomielitis, osteosarkoma telangiektatik, limfoma) |
| Entitas dengan prior ≠ 0 | 16 (7 pada −2, 9 pada −1) |

Bila angka ini berbeda setelah build ulang, KB sudah berubah: periksa CHANGELOG sebelum menerbitkan.

## Berkas baru

- `tools/build_matrix.py` — `python3 tools/build_matrix.py [root] [keluaran] [templat]`; bawaan: `web/matrix_template.html`
  → `web/matrix.html`. Berhenti bila ada nilai fitur, kelompok WHO atau perilaku yang tidak dikenal (tambahkan
  labelnya di `SHORT`, `VS`, `GROUPS`, `BEH`; ini teks tampilan, di luar skema data).
- `web/matrix_template.html` — templat halaman; data disisipkan pada `/*DATA*/`, angka pada `{{entities}}` dst.
- `web/matrix.html` adalah hasil build dan tidak disimpan di proyek.

## Yang belum dilakukan

- **Berkas baru belum didorong ke GitHub** `harmenreza/TumTul`; saat ini hanya ada di proyek. Sesi baru yang mengklon
  repo harus mengambil berkas matriks dan berkas tinjauan dari proyek (`project_read`) atau mendorongnya dulu atas izin
  pemilik.
- README di repo juga belum memuat perubahan sesi ini (salinan proyek sudah).
- Matriks belum ditautkan dari prototipe aplikasi atau dari tab Tentang.
- Tidak ada versi berbahasa Indonesia dari matriks.

## Aturan tetap

Sama dengan `docs/HANDOFF-UI.md`: alat referensi/edukasi, bukan alat diagnostik; tidak pernah satu diagnosis; alasan
dan sumber selalu tampil; tidak menganalisis gambar, tidak menyimpan data pasien; tanya pemilik sebelum mengubah skema
data; README, LICENSES, CHANGELOG diperbarui setiap perubahan. Matriks tidak boleh disertai klaim akurasi: bobot belum
memenuhi kriteria uji terdaftar v3 dan v4.

## Cara bekerja di sesi baru

- Klon `harmenreza/TumTul` (publik); berkas KB ada di `data/`. Salinan proyek dan repo README/CHANGELOG identik sampai
  commit b37defc (2026-11-19); perubahan 2026-11-21 hanya ada di proyek.
- Setelah bobot, entitas atau nilai fitur berubah: `python3 tools/build_matrix.py`, cocokkan angka, lalu terbitkan
  ulang `web/matrix.html` sebagai `index.html` ke artifact yang sama (slug `679bd2cb-b6e3-4dc5-a635-9ee1979562f9`).
- Papan alur diubah langsung di Whiteboard (slug `65e39472-dfa7-4d0c-a96a-de524e17838e`); baca seluruh papan sebelum
  mengubahnya.
- Uji tanpa kepala (Playwright, 400 px terang dan gelap) sebelum menerbitkan.

## Kalimat pembuka yang disarankan untuk sesi baru

> Lanjutkan TumTul dari `docs/HANDOFF-SKORING.md` dan `docs/HANDOFF-UI.md`. Dorong berkas matriks ke repo, lalu
> kerjakan langkah UI no. 2 (Sumbu B sebagai lembar film); buat mockup dulu untuk saya setujui.
