# TumTul — Tumor Tulang

*Referensi diagnosis banding lesi tulang* · bone lesion differential reference app
(named TumTul on 2026-11-10; earlier working titles: BoneDx, Bone Tumour Differential)

An Android reference/educational app that returns a **ranked, reasoned differential**
for bone tumours from user-selected imaging features (age, bone, location within bone,
lytic/sclerotic, margin, periosteal reaction, matrix, etc.), with a source citation
for every statement.

**Owner:** MSK oncology radiologist, Indonesia · **Language of content:** Bahasa Indonesia
with standard English (WHO) entity names · **Status:** v0.6.7 — data schema v1.1.0,
37 entities (v1 scope: long bones + pelvis + spine), web prototype published with the
"Negatoskop" theme and light/dark mode; four internal validation sets run (no accuracy claim);
practice-case validation pending.

## What this app is and is not

- It **is** a reference and teaching tool for radiologists and trainees.
- It **is not** a diagnostic device. It never outputs a single diagnosis; it always shows
  a ranked list, the reasoning per feature, and the sources.
- It **never** analyses images and **never** stores patient data. All inputs are feature
  selections made by the user from their own reading.
- Two output axes are kept separate: (A) radiographic aggressiveness, (B) compatible
  entities ranked by score. Aggressive-looking ≠ malignant.

## Content rules

- Facts come from open sources only: CC BY journal articles, WHO 5th-edition
  classification criteria restated in our own words, Radiopaedia with full
  CC BY-NC-SA attribution. Closed-access landmark papers may be cited bibliographically
  (`license_status: cite_only`) but nothing from them is reproduced.
- Every entity and every weight in the knowledge base carries one or more source codes
  (`S-xx`) that resolve to `data/sources.json`.
- Licence status of each source is tracked (`verified` / `to_verify` / `cite_only`).
  Nothing marked `to_verify` is reused beyond restated facts until confirmed.
- Non-commercial-licensed sources (CC BY-NC, CC BY-NC-SA) constrain distribution:
  the app must stay free and ad-free, or those sources must be replaced.

## Visual design (since v0.6.7)

Theme **"Negatoskop"**: warm film-viewer light mode and a PACS reading-room dark mode, switchable
in the header (Sistem / Terang / Gelap; stored per device only).

| Token | Light | Dark | Role |
|---|---|---|---|
| `--bg` | #F3EFE6 | #0E1215 | page |
| `--surface` | #FBF9F4 | #161B1F | panels, tiles |
| `--fg` / `--muted` | #1C2024 / #5A5F66 | #E7E3DA / #9AA0A6 | text |
| `--accent` (rust) | #A3471F | #E8935F | what the app computes: active tab, score bar, nav |
| `--sel`, `--link` (teal) | #2E5C63 | #7FB6BC | what the user entered and what is cited |
| `--warn` / `--crit` | #8A5A12 / #8E2F22 | #D9A653 / #E8806A | Axis A scale, notices |

Rules: no red/green on the ranked list (behaviour pills are neutral; the label carries the meaning);
all text pairs ≥ 4.5:1. Fonts: Source Serif 4 (headings, entity names), IBM Plex Sans (UI),
IBM Plex Mono (scores) — all SIL OFL 1.1; bundled in the Flutter app (see `LICENSES.md` §5).
The same tokens are to be mapped to a Flutter `ThemeData` light/dark pair.

Original visual elements (since 2026-11-19): location is entered on a bone diagram (longitudinal section +
cross-section) instead of two list pickers, and the options for margin, periosteal reaction and matrix carry
schematic pictograms drawn for this project (radiograph convention: light = dense, dark = lucent). Defined in
`web/template.html` (`PICTO`, `mapHTML`); to be redrawn as Flutter `CustomPainter`/SVG assets from the same paths.

## Repository layout

```
README.md                     this file
LICENSES.md                   licences of code, content, fonts and each source class
CHANGELOG.md                  running log of changes
docs/SKEMA-DIAGNOSIS.md       the diagnostic scheme (features, tables, scoring logic, decisions) — ID
schema/kb-schema.json         JSON Schema for the knowledge base — v1.1.0 (base_prior added 2026-11-10, owner-approved)
schema/kb-schema.draft.json   superseded draft, kept for history
data/features.json            input feature enumerations (ID/EN labels, help text)
data/sources.json             source registry with licence status
data/entities/<id>.json       one file per entity: weights, rules, pitfalls, sources (37)
data/validation/             blind-coded validation cases, results, raw coder output
docs/validation-brief.md      coding brief for validation cases
docs/VALIDASI-INTERNAL-v1.md  validation report v1
tools/build_entities_batch1.py  generator, batch 1 (19 entities) — single source of truth for weights
tools/build_entities_batch2.py  generator, batch 2 (18 entities); imports batch 1 helpers
tools/validate_kb.py          schema + cross-reference validation (run before every commit)
tools/score_smoke.py          reference scoring implementation + 18 classic-vignette smoke tests
tools/build_web.py            inlines features + entities + sources into web/template.html → web/index.html
tools/build_form.py           builds the practice-case reading form web/form.html from web/form_template.html
docs/FORMULIR-KASUS-PRAKTIK.md  practice-case form: roles, access rules, privacy, data dictionary, export
docs/PROPOSAL-VALIDASI-PRAKTIK.md  research proposal for the practice-case validation: summary, open decisions, link to the full manuscript
tools/sample_size_p1.py       sample-size and power calculations for the practice-case validation (exact binomial; reader-study simulation)
web/template.html             prototype UI (Indonesian), scoring JS mirrors score_smoke.py; theme tokens in :root
data/images.json              example-image registry for the Sumbu B gallery (separate from the KB schema); only status "approved" is shown
web/img/                      example radiographs (JPEG, 500–1600 px); files kept in GitHub harmenreza/TumTul
tools/fetch_commons.py, tools/fetch_pmc.py   candidate fetchers (run as GitHub Actions; Commons + PMC open access)
tools/fetch_hires.py          fetches full-resolution originals of the picked images (GitHub Action)
tools/assemble_images.py      picks + Indonesian captions -> web/img/ + data/images.json (crop, resize, attribution)
tools/image_picks.json, tools/image_captions_id.json   selected images per entity and our own captions
web/index.html                built, self-contained prototype (published as a Claude artifact)
flutter/                      Android app (after the web prototype is validated)
```

## Build

```
python3 tools/build_entities_batch2.py   # regenerates batch 1 and 2
python3 tools/validate_kb.py             # must print OK
python3 tools/score_smoke.py             # expect 19/20 PASS (the 20th is a deliberate tie)
python3 tools/build_web.py               # writes web/index.html (inlines KB + data/images.json; checks approved images exist)
```

## Scoring logic (reference)

`tools/score_smoke.py` is the normative implementation: per entity,
`score = Σ feature weights (given inputs) + Σ matching rule weights`; any weight of −5 is a
hard constraint that moves the entity to an "excluded because…" list instead of deleting
it. `unknown` inputs contribute nothing. The web and Flutter implementations must
reproduce its output on the vignettes in that file.

## Stack

1. Knowledge base as JSON (validated against `schema/kb-schema.draft.json`).
2. Scoring logic first as a static web prototype (plain HTML/JS, no backend, no tracking).
3. Flutter for Android, reading the same JSON.

## Governance

- **Data schema changes require explicit approval from the owner before they are made.**
  Propose changes as a diff against `schema/kb-schema.draft.json` and wait.
- `README.md`, `LICENSES.md` and `CHANGELOG.md` are kept current with every change.
- Indonesian IP registration (HAKI) is planned; keep authorship/attribution records clean.

## Roadmap (short)

- [x] Literature sweep (PubMed, OpenAlex) and source registry with licence check
- [x] Diagnostic scheme v0.1 (`docs/SKEMA-DIAGNOSIS.md`)
- [x] Design decisions (§6) → `schema/kb-schema.json` v1.0.0 frozen
- [x] Batch 1: 19 core entities + validator + smoke tests
- [x] Batch 2: 18 further v1 entities (37 total)
- [x] Web prototype: form → aggressiveness axis + ranked reasoned differential + sources tab
- [x] Confirm licences in `data/sources.json` (24 verified, 6 cite-only)
- [x] Internal validation v1 on 31 open-access case reports (`docs/VALIDASI-INTERNAL-v1.md`):
      Top-3 84%, Top-5 87% after post-hoc corrections
- [x] Three feature values added after v1 (continuity, saucerization, periosteal present-unspecified)
- [x] Confirmation set v2 (74 new case reports, weights untouched): Top-3 68% overall,
      89% on typical cases with ≥8 features (`docs/VALIDASI-INTERNAL-v2.md`)
- [x] v0.6.0: prevalence prior (schema v1.1.0), haemangioma trabecular value, relaxed hard
      constraints, osteomyelitis/TB/GCTB weights, UI dependency rules
- [x] Pre-registered confirmation set v3 (52 cases): primary criterion NOT met (Top-3 48% vs ≥75%);
      open-access case reports judged exhausted as a validation instrument (`docs/VALIDASI-INTERNAL-v3.md`)
- [x] Pre-registered set v4 from review-article illustrative cases (36 analysed): primary criterion NOT met
      (Top-3 69% vs ≥80%; Top-5 83%); typical but sparse input (mean 4.5 features) — `docs/VALIDASI-INTERNAL-v4.md`
- [x] v0.6.3 UI: ties shown explicitly; sparse-input warning (< 6 features); impossible value pairs blocked
- [x] v0.6.7 UI: "Negatoskop" colour theme, serif/sans/mono type system, light/dark/system switch
- [ ] Share prototype with colleagues as an educational tool, without accuracy claims; collect feedback
- [x] Practice-case reading form (digital, same codes as the app, reader blinding, export) — `docs/FORMULIR-KASUS-PRAKTIK.md`
- [x] Research proposal for the practice-case validation drafted (two stages: diagnostic accuracy on 200 cases,
      reader study 12 readers × 80 cases) — `docs/PROPOSAL-VALIDASI-PRAKTIK.md`; owner decisions pending
- [ ] Practice-case validation: consecutive biopsy-proven cases, features read from images, pre-registered
      protocol, ethics approval (v1–v3 remain regression tests: `validate_cases.py v1|v2|v3`)
- [ ] Prepare v0.7 hypotheses (CMF/GCTB weights, explicit ties, sparse-input warning) for evaluation on practice cases
- [ ] Batch 3 (v2): hands/feet, calvaria, clavicle entities; dedifferentiated and
      mesenchymal chondrosarcoma; CRMO; leukaemia; Erdheim-Chester
- [ ] Flutter app reading the same JSON (theme tokens and bundled OFL fonts per `LICENSES.md` §5)

## Example images (Sumbu B gallery)

Button "Lihat contoh gambar" on each ranked entity opens up to three typical radiographs with our own caption
and full attribution. Selection rules (owner): pre-treatment radiographs only; most typical case only (no source
that calls the case atypical, unusual, rare-site, aggressive, mimic or misdiagnosed); longest side ≥ 500 px after
cropping; licence CC0 / public domain / CC BY / CC BY-SA only. Every image is approved by the owner before it is
shown. Status 2026-11-17: 66 approved images for 32 of 37 entities; none yet for clear cell chondrosarcoma,
periosteal chondroma, vertebral haemangioma, desmoplastic fibroma and periosteal osteosarcoma.
