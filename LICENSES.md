# LICENSES

## 1. Application code

To be decided by the owner before the first public release. Options under consideration:
MIT or Apache-2.0 for code. (Not yet chosen — recorded here so the decision is not forgotten.)

## 2. Original content written for this project

Scheme text, entity definitions, weights and UI copy are original works written in our
own words. Proposed licence: **CC BY 4.0** (so that the knowledge base itself remains
reusable by other educators). Final decision pending owner approval and HAKI registration.

## 3. Third-party sources

Full per-source records (DOI, PMID, licence, status, exact verification note) live in
`data/sources.json`. The first 30 entries were checked against publisher or PMC pages/PDFs on
2026-11-09; none remain `to_verify`. S-31 and S-32 (two CC BY 4.0 spine reviews, Diagnostics 2023) were added on
2026-11-22 with the licence taken from PMC metadata (32 entries in total).

| Licence | Reuse allowed | Constraint for this project | Sources |
|---|---|---|---|
| CC BY 4.0 (19) | Text, tables, figures with attribution | Attribution on the Sources page; indicate changes | S-01, S-03, S-04, S-06, S-09, S-10, S-11, S-15, S-16, S-17, S-19, S-20, S-22, S-24, S-25, S-26, S-27, S-31, S-32 |
| CC BY-NC-ND 4.0 (4) | Verbatim copies with attribution; no adaptation, non-commercial | Used for restated facts only; no figure or table adapted | S-05, S-14, S-18, S-21 |
| CC BY-NC 4.0 / 2.0 (2) | Adaptation with attribution, non-commercial only | App must remain free of charge and ad-free, or replace the source | S-13, S-23 |
| CC BY-NC-SA 3.0 (1) | Adaptation with attribution, NC, share-alike | Any adapted Radiopaedia-derived content must carry the same licence | S-30 |
| cite-only (6) | None | Bibliographic citation only; facts restated in our own words | S-02, S-07, S-08, S-12, S-28, S-29 |

Notes from verification:
- S-07 (ACR Bone-RADS consensus, JACR) and S-12 (MXSS, J Carcinogenesis) carry a publisher
  copyright line and no Creative Commons licence, although the PDFs are freely readable.
  Both are therefore cited but nothing from them is reproduced.
- S-09 and S-10 state "Creative Commons Attribution License" without a version on the PMC
  copy; both publishers (Hindawi, AOSIS) license under CC BY 4.0.
- S-14 is confirmed at journal level (Pol J Radiol "About the Journal") and on a same-journal
  article PDF; the 2020 article pages themselves do not display the licence line.
- S-18 is confirmed from the depositing institution's repository metadata for the
  published version.

**Distribution consequence:** six sources (CC BY-NC-ND ×4, CC BY-NC ×2) plus Radiopaedia
(CC BY-NC-SA) forbid commercial use. The app must be distributed free of charge and
without advertising, or those sources must be replaced before any paid distribution.

## 4. Attribution format used in the app

Sources page shows, per source: authors, title, journal/year, DOI link, licence name
with link, and the note "Facts restated; no text reproduced" or "Figure adapted under
[licence]" as applicable. Radiopaedia entries additionally show article title, author,
URL and "CC BY-NC-SA 3.0".

## 5. Fonts (UI theme "Negatoskop", since v0.6.7)

| Font | Use | Licence | Copyright |
|---|---|---|---|
| Source Serif 4 | App title, headings, entity names | SIL Open Font License 1.1 | © Adobe |
| IBM Plex Sans | UI text | SIL Open Font License 1.1 | © IBM Corp. |
| IBM Plex Mono | Scores, ranks, version labels | SIL Open Font License 1.1 | © IBM Corp. |

- OFL 1.1 permits use, bundling and redistribution with software, including commercial software,
  provided the font files keep their copyright notice and licence text and are not sold on their own.
- Web prototype: fonts are loaded from Google Fonts (hosting constraint of the published artifact);
  if they fail to load, system serif/sans/mono fallbacks are used and nothing breaks.
- Flutter app: the font files are to be **bundled in the APK** (offline use) together with each
  font's `OFL.txt`, and listed on the in-app licences screen (Flutter `LicenseRegistry`).

## 6. Example images (Sumbu B gallery)

Registry: `data/images.json`; files: `web/img/`. Every image carries, directly under it in the app:
source title with link, author(s), repository, licence with link, and changes made ("diperkecil", or
"dipotong ke panel radiograf, diperkecil"). Captions are our own words, not the source captions.

| Licence class | Images (approved, 2026-11-17, typical-only, ≥500 px; 66 total) | Obligation |
|---|---|---|
| CC BY 2.0 / 3.0 / 4.0 | 35 | Attribution, link to licence, indicate changes |
| CC BY-SA 2.0 / 3.0 (incl. 3.0 DE) / 4.0 | 29 | As CC BY; a modified image (cropped/resized) is shared under the same licence — the app's image files are therefore offered under the image's own CC BY-SA licence, separate from the app's code/content licence |
| CC0 / public domain | 2 | None (attribution kept as good practice) |

- Only CC0, public domain, CC BY and CC BY-SA are accepted for images (no NC, no ND, no "free use" or
  "no known restrictions" statements, no figures reprinted from third parties inside an article).
- Patient identity: all images are previously published, de-identified figures; the app never takes
  images from users and never analyses images.

## 7. Trademarks and names

"WHO Classification of Tumours" is referred to descriptively. No WHO/IARC text, tables or
figures are reproduced. "ACR Bone-RADS" is a trademark of the American College of
Radiology; referred to descriptively only. Radiopaedia is a trademark of Radiopaedia.org;
used descriptively.
