# Serah terima sesi UI — 2026-11-19

Dokumen ini untuk memulai sesi baru tanpa kehilangan konteks. Baca bersama `claude/README.md` dan `claude/CHANGELOG.md`.

## Keadaan sekarang

- Prototipe TumTul: https://claude.ai/artifact/DsM6XAJos65GTAABAw79AX (versi 15). KB 0.6.0, skema data v1.1.0, 37 entitas.
- Tema "Negatoskop" (terang/gelap/sistem).
- Galeri contoh gambar di Sumbu B: 66 gambar disetujui untuk 32 entitas (`data/images.json` v0.3.1).
  Belum ada gambar: kondrosarkoma sel jernih, kondroma periosteal, hemangioma vertebra, fibroma desmoplastik,
  osteosarkoma periosteal.
- Ringkasan "Deskripsi temuan" bergaya ekspertise sudah diterapkan (2026-11-19).
- Elemen visual orisinal yang sudah diterapkan (2026-11-19): lembar "Lokasi lesi" (diagram tulang potongan memanjang
  dan melintang) dan piktogram pada pilihan margin Lodwick, reaksi periosteal, matriks.
- Mockup desain: https://claude.ai/artifact/TtqriTDXt8ourmMVCYXgFN.
- Lembar tinjauan gambar: https://claude.ai/artifact/QJaFQ1VKudCtcoUHGa1Mi2.

## Langkah berikutnya (urutan yang disepakati)

1. ~~Ringkasan bergaya ekspertise (ide no. 5)~~ — **selesai 2026-11-19**: strip "Deskripsi temuan" (varian B, terlipat
   dua baris, dibuka dengan ketukan) di atas hasil Sumbu A dan B, dengan tombol Salin. Kamus frasa: `EK`, `EK_NEG`,
   `EK_AGE`, `EK_CLIN`; perangkai: `ekspertise()`; tampilan: `paintEksp()` di `web/template.html`.
2. **Sumbu B sebagai lembar film** (ide no. 3): skor sebagai strip densitas (step-wedge), entitas seri diikat satu kurung.
3. Sumbu A sebagai skala bertanda 0–9 (ide no. 4).
4. Polesan: detail negatoskop, logo/ikon aplikasi, suara teks ruang baca (ide no. 6–8).

Semua langkah di atas hanya tampilan; skema data, bobot dan kode fitur tidak berubah.

## Keputusan pemilik yang masih terbuka

- Piktogram: pemilik diminta menilai Codman, cangkang, dan beda IC dengan II; gambar ulang bila kurang tepat.
- Lima entitas tanpa gambar: (a) pemilik mengirim tautan kasus tipikal, atau (b) mengizinkan gambar Radiopaedia
  CC BY-NC-SA untuk lima entitas itu (aplikasi harus tetap gratis dan tanpa iklan). Aturan gambar saat ini hanya
  menerima CC0, domain publik, CC BY, CC BY-SA.

## Aturan tetap

- Alat referensi/edukasi, bukan alat diagnostik; tidak pernah satu diagnosis; alasan dan sumber selalu tampil.
- Tidak menganalisis gambar, tidak menyimpan data pasien.
- Tanya pemilik sebelum mengubah skema data. `data/images.json` adalah registri terpisah dari skema KB.
- Gambar contoh: radiograf pra-terapi, kasus paling tipikal (tolak sumber yang menyebut atipikal, tidak lazim,
  lokasi jarang, agresif, raksasa, multifokal, peniru, salah diagnosis), dipotong ke panel radiograf, sisi terpanjang
  ≥ 500 px setelah dipotong, disetujui pemilik satu per satu.
- README, LICENSES, CHANGELOG diperbarui setiap perubahan.

## Cara bekerja di sesi baru

- Sumber kebenaran berkas: proyek ini (teks) dan repo GitHub publik `harmenreza/TumTul` (teks + gambar `web/img/`,
  kandidat, berkas resolusi penuh `hires/`). Ruang kerja sesi bersifat sementara: klon repo, jangan mengandalkan
  berkas lokal sesi lama.
- Build: `python3 tools/build_web.py` menyisipkan KB dan `data/images.json` ke `web/template.html` → `web/index.html`.
  Berkas KB (`data/features.json`, `data/sources.json`, `data/entities/*.json`) ada di repo; bila hilang, pulihkan dari
  blok `<script id="kb">` di `web/index.html`.
- Terbitkan ulang prototipe ke URL artifact yang sama; gambar dikirim lewat peta `files` dengan `root` = `web`
  (berkas yang tidak dikirim tetap ada).
- Ruang kerja tidak dapat menjangkau Wikimedia, Europe PMC atau Radiopaedia; pengambilan gambar dijalankan lewat
  GitHub Actions di repo (`fetch-commons.yml`, `fetch-pmc.yml` dengan input `gap`, `fetch-hires.yml` otomatis saat
  `tools/image_picks.json` didorong). Mendorong `tools/fetch_pmc.py` atau `tools/pmc_queries.json` memicu putaran
  pertama secara otomatis; batalkan bila tidak dimaksud.
- `tools/assemble_images.py` menulis status yang sama untuk semua rekaman; setelah menjalankannya, tandai kembali
  gambar yang sudah disetujui sebagai `approved`.
- Uji tanpa kepala (Playwright, lebar 400 px, terang dan gelap) sebelum menerbitkan.
- Kode UI terkait: `PICTO`, `pic()`, `choose()`, `mapHTML()`, `openMap()`, `openSheet()` di `web/template.html`.

## Kalimat pembuka yang disarankan untuk sesi baru

> Lanjutkan TumTul dari `docs/HANDOFF-UI.md`. Kerjakan langkah berikutnya no. 2 (Sumbu B sebagai lembar film),
> buat mockup dulu untuk saya setujui.
