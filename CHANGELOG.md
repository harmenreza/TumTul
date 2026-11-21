# CHANGELOG

All notable changes to this project are recorded here. Format follows Keep a Changelog;
versions follow SemVer. Data-schema changes are only recorded after owner approval.

## [Unreleased] — 2026-11-16

### Changed (2026-11-22) — KB 0.6.1, sources only (owner-approved; every weight, rule and prior identical to 0.6.0)
- **Chondromyxoid fibroma re-cited from S-06 to S-18** (proposal A below, approved by the owner on 2026-11-22).
  `data/entities/chondromyxoid_fibroma.json`: S-06 removed from the 44 claims that cited it and from the entity's
  sources; S-18 added to 19 claims (20 of 46 now cite it). No weight, note, rule, prior or schema field changed, so all
  scores and rankings are identical to 0.6.0; `data/validation/kb_snapshot_v0.6.0.json` stays the frozen reference.
- New `tools/apply_source_overrides.py`, run after the generators (README "Build"). It holds the approved table, is
  idempotent, has a `--check` mode, stops if a listed claim is missing, and asserts that the entity is unchanged once
  source lists are removed. The generators were not edited: they exist only in the project store, not in the
  repository, and the override step keeps their weight tables untouched.
- **Two sources added and cited (proposal B2, approved by the owner the same day).** `data/sources.json` → registry
  0.3.0, 32 entries: **S-31** Ariyaratne et al. 2023, Primary Osseous Malignancies of the Spine, and **S-32** Ariyaratne
  et al. 2023, Primary Benign Neoplasms of the Spine (Diagnostics; CC BY 4.0 per PMC metadata; both read in full).
  S-31 added to 20 chordoma claims (11 supported, 9 direction only); S-32 added to 8 vertebral-haemangioma claims
  (3 and 5). Deliberately not cited: chordoma `matrix:none` (+2) and haemangioma `cortex:destruction` (−5), which the
  new sources contradict. `LICENSES.md` §3: CC BY 4.0 sources 17 → 19.
- `tools/build_web.py`: `kb_version` 0.6.0 → 0.6.1. `web/index.html` rebuilt; apart from the embedded KB line it is
  identical to the previous build. Loaded headlessly at 400 px: no script errors, no horizontal scroll.
- **Public prototype republished** (same link, artifact version 17, owner's go-ahead 2026-11-22) after confirming that
  the published `index.html` was byte-identical (SHA-256) to the previous repository build. Only `index.html` was sent;
  the 66 images are unchanged. The project copy of `web/index.html` is still the 0.6.0 build; regenerate it with
  `tools/build_web.py`.
- Scoring matrix rebuilt and republished (same link): counts unchanged; CMF, chordoma and haemangioma cells show the
  new sources.
- New hypothesis candidates from the two reviews, **not applied** (weights are frozen): vertebral haemangioma
  `cortex:destruction` −5 → −2 (aggressive haemangioma); chordoma `matrix:none` +2 → lower (punctate calcification common).
- `tools/review_sources.py` and its evidence file describe KB 0.6.0. Run against 0.6.1 they stop on the ten CMF rows
  that record S-06 findings; that is expected. `docs/SKEMA-DIAGNOSIS.md` header still says bobot v0.6.0, which remains
  true for the weights.

## Schema v1.2.0 — 2026-11-22 (owner-approved)
- `schema/kb-schema.json`: `CC BY 3.0`, `CC BY 2.0` and `CC BY-NC 3.0` added to the `license` enum of a source, for
  S-33, S-35 and S-34. Title and description updated. **Nothing else in the schema changed**; no data file changed.
- `tools/validate_kb.py` now prints `OK — 37 entities, 1584 weighted claims, 5 rules, 28 sources referenced by
  entities`. Against the previous licence list it reports exactly the three expected failures.
- `tools/score_smoke.py` prints 20/20 on KB 0.6.4: 19 vignettes rank the expected entity first outright, and the
  osteomyelitis vignette is the deliberate tie with Ewing sarcoma (both 23), which the script counts as first. This is
  the same result the README described as "19/20 PASS (the 20th is a deliberate tie)".
- Added to the GitHub repository: `schema/kb-schema.json`, `tools/validate_kb.py`, `tools/score_smoke.py`. The two
  scripts were retyped from the project copies (the project returns small files as text, not as files) and verified by
  running them, not by a byte comparison; the project copies remain the originals.
- **Not added:** the generators `build_entities_batch1.py` and `build_entities_batch2.py`. They hold every weight and
  are too long to retype safely; they stay in the claude.ai project until they can be copied exactly.

### Found and recorded (2026-11-22, end of session) — schema enum problem; handoff rewritten
- **Problem introduced this session:** S-33 (`CC BY 3.0`), S-34 (`CC BY-NC 3.0`) and S-35 (`CC BY 2.0`) use licence
  strings that are not in the `license` enum of `schema/kb-schema.json` v1.1.0. `tools/validate_kb.py` would fail with
  three errors. Cause: the schema and the validator exist in the claude.ai project but not in the GitHub repository,
  and the validator was not run before the sources were registered. The licence values are correct and were left as
  they are; extending the enum is a schema change and awaits the owner's decision.
- Checked with the schema's source rules (`$defs/source`, `$defs/sourceRef`): 41 sources and 1663 source lists; those
  three licence strings are the only problems. `validate_kb.py` and `score_smoke.py` themselves were not executed;
  scores cannot have changed because weights, priors and rules are identical to 0.6.0.
- `docs/HANDOFF-SKORING.md` rewritten as a single state-of-the-project handoff (KB 0.6.4). README status, layout and
  roadmap updated. Project copy of `web/index.html` replaced with the 0.6.4 build.
- These last documentation changes are in the claude.ai project only; GitHub `main` (e577558) has KB 0.6.4 data but
  the earlier handoff and README text.

## KB 0.6.4 — 2026-11-22 (sources only; weights, priors and rules identical to 0.6.0)
- Owner-approved. `data/sources.json` → registry 0.6.0, 41 entries: **S-37** Pattamapaspong et al. 2024 (BJR,
  `cite_only`), **S-38** Abid et al. 2024 (Skeletal Radiol, `cite_only`; read from the author version),
  **S-39** Semionov et al. 2022 (Open J Radiol, CC BY 4.0), **S-40** Frick et al. 2005 (AJR, `cite_only`),
  **S-41** Ipponi et al. 2025 (Cancers, CC BY 4.0).
- Skeletal tuberculosis: 27 of 45 claims now carry a specific source beyond S-01 (S-37 on 20, S-38 on 18, S-39 on 8,
  S-36 on 8). Desmoplastic fibroma: 19 of 43 (S-40 on 16, S-41 on 10, S-34 on 10, S-35 on 9). Supported claims only.
- `periosteal:solid_thin` for tuberculosis, counted as supported in the first pass, was reclassified as direction
  only and left uncited (27, not 28).
- `tools/apply_source_overrides.py`: per-source tables merged with a small helper; `--check` clean.
- `tools/build_web.py`: `kb_version` 0.6.3 → 0.6.4. Prototype (artifact version 20) and scoring matrix republished.
- `LICENSES.md` §3: CC BY 4.0 sources 19 → 21; cite-only 7 → 10.
- Added to pull request #2 on GitHub, which now carries KB 0.6.2, 0.6.3 and 0.6.4.

### Checked (2026-11-22, after KB 0.6.3) — nine PDFs from the owner; five were registered afterwards (KB 0.6.4)
- Skeletal TB: Pattamapaspong 2024 (BJR) and Abid 2024 (Skeletal Radiol), both `cite_only`, would raise supported
  claims from 8 to 28 of 45. Semionov 2022 (CC BY 4.0) is the only openly licensed one and supports about 8.
- Desmoplastic fibroma: Frick 2005 (AJR, `cite_only`; 38 radiographs) and Ipponi 2025 (Cancers, CC BY 4.0; 187 cases)
  would raise supported claims from 10 to 19 of 43. Periosteal reaction still has no source.
- Periosteal osteosarcoma: Cè 2025 is S-15 (already registered); its section states diaphysis or metadiaphysis.
- Not useful for the gaps: Butt 2025 (soft-tissue tuberculomas), Sindhura 2026 (no licence, adds nothing), Khan 2012.
- New hypothesis candidates recorded, not applied. Details in `docs/USULAN-SUMBER-v0.7.md`, update (h).

## KB 0.6.3 — 2026-11-22 (sources only; weights, priors and rules identical to 0.6.0)
- Owner-approved. `data/sources.json` → registry 0.5.0, 36 entries: **S-36** Rivas-Garcia et al. 2013, Imaging
  findings of Pott's disease (Eur Spine J; © Springer, no CC licence → `cite_only`; read in full from the owner's PDF).
- S-36 cited on 8 skeletal-tuberculosis claims (supported claims only): vertebral body, age 40–59, lytic, mixed,
  sclerotic, cortical destruction, soft-tissue mass, multiplicity. First radiographic source for this entity.
- Liu et al. 2015 deliberately **not** registered (internally contradictory).
- `tools/build_web.py`: `kb_version` 0.6.2 → 0.6.3. Prototype (artifact version 19) and scoring matrix republished.
- `LICENSES.md` §3: cite-only sources 6 → 7.
- KB 0.6.2 and 0.6.3 pushed to GitHub together as pull request #2.

### Checked (2026-11-22, last) — Liu 2015 and Rivas-Garcia 2013 read in full from the owner's PDFs
- Rivas-Garcia et al. 2013 (Eur Spine J; © Springer, `cite_only` at most): the first radiographic source for skeletal
  TB. 8 of 45 claims supported, 9 direction only. Registered afterwards as S-36 (see KB 0.6.3).
- Liu et al. 2015 (Int J Clin Exp Med; no CC licence): supports saucerisation but contradicts itself on diaphysis
  versus metaphysis and on other points. Recommended **not** to register.
- Details in `docs/USULAN-SUMBER-v0.7.md`, update (f).

## KB 0.6.2 — 2026-11-22 (sources only; weights, priors and rules identical to 0.6.0)
- Owner-approved. `data/sources.json` → registry 0.4.0, 35 entries: **S-33** Kitajima et al. 2018 (Cureus, CC BY 3.0),
  **S-34** Nedopil et al. 2013 (Open Orthop J, CC BY-NC 3.0; non-commercial flag as S-13 and S-23), **S-35** Stefanidis
  et al. 2011 (J Med Case Rep, CC BY 2.0). All three read in full; all are case reports (S-34 with a literature review).
- S-33 cited on 11 periosteal-osteosarcoma claims, including `cortex:saucerization`. S-34 on 10 and S-35 on 9
  desmoplastic-fibroma claims. **Supported claims only**: because these are case reports, direction-only claims were
  left uncited (unlike S-31 and S-32, which are imaging reviews).
- `tools/apply_source_overrides.py` extended; `--check` clean; weights, priors and rules verified identical.
- `tools/build_web.py`: `kb_version` 0.6.1 → 0.6.2. Prototype (artifact version 18) and scoring matrix republished.
- `LICENSES.md` §3 updated (new CC BY 3.0 / 2.0 row; CC BY-NC sources 2 → 3; seven non-commercial sources).

### Checked (2026-11-22, later) — more source candidates; the three above were registered afterwards
- Revell et al. 2002 (Sarcoma; 17 periosteal osteosarcomas; owner's PDF, read in full): 8 of 38 claims supported,
  8 direction only. Owner decided **not** to register it. Its Table 1 contradicts its own text and Table 2.
- SciSpace search for the three remaining gaps; licences from PubMed/PMC metadata. Six candidates checked against the
  weights: Nedopil 2013 and Stefanidis 2011 (desmoplastic fibroma: 10 of 43 supported), Mittal 2016 and Rivas-Garcia
  2013 (skeletal TB: 4 of 45), Kitajima 2018 and Liu 2015 (periosteal osteosarcoma: 11 of 38, including
  `cortex:saucerization`). Four were read in full; Liu and Rivas-Garcia as abstracts only.
- New hypothesis candidates, not applied: desmoplastic fibroma `cortex:intact` and `margin_lodwick:IA`; TB
  `bone_class:spine_body` and `soft_tissue_mass:present`; periosteal osteosarcoma diaphysis versus metaphysis.
- Observation for the schema options (no change): the features that separate TB spondylitis (disc, contiguous levels,
  paraspinal abscess) are not in the feature schema.
- Details in `docs/USULAN-SUMBER-v0.7.md`, updates (b), (c), (d).

### Checked (2026-11-22) — two EPOS posters screened; nothing applied
- Read through per-section page summaries, not word for word. Neither page showed an open-licence statement, so both
  are treated as `cite_only` until that is confirmed on the poster page.
- Periosteal osteosarcoma against ECR 2022 C-13882: of 38 claims, 10 supported (age 10–19, long bone, diaphysis,
  surface, lytic, soft-tissue mass, spiculated and Codman periosteal reaction), 11 direction only, 17 not discussed
  (including `cortex:saucerization`).
- Skeletal tuberculosis against ECR 2019 C-1421: of 45 claims, 4 supported, 14 direction only, 27 not discussed (no
  age, spine or clinical signs in that section). Weak; spondylitis still needs a source.
- Details in `docs/USULAN-SUMBER-v0.7.md`, "Pembaruan 2026-11-22".

### Proposed (2026-11-22; B2 has since been applied, see above)
- **B2. Two spine reviews read in full** (Ariyaratne et al. 2023, Diagnostics, both CC BY 4.0; proposed as new sources
  S-31 and S-32, not yet registered). Chordoma against "Primary Osseous Malignancies of the Spine": of 32 claims,
  11 supported, 9 direction only, 11 not discussed, 1 mild conflict (`matrix:none` +2; the source says punctate
  calcification is common). Vertebral haemangioma against "Primary Benign Neoplasms of the Spine": 3 supported
  (vertebral body, coarse trabeculae, soft-tissue mass −2), 5 direction only, 23 not discussed (no age data), and
  1 contradicted — `cortex:destruction` −5, because the source describes aggressive haemangioma with bone destruction.
  Both reviews are CT/MRI-led. They also cover enostosis, osteoid osteoma, osteoblastoma, ABC, GCTB, LCH, lymphoma,
  plasmacytoma and spinal Ewing sarcoma (noted, not checked claim by claim). Details in `docs/USULAN-SUMBER-v0.7.md` §B2.
- **C. EPOS posters** (owner's suggestion): EPOS disclaimer read — ESR holds copyright; posters from ECR 2014 onward
  carry an open licence (attribution, non-commercial, share-alike); earlier ones, including the owner's two ESSR 2013
  examples, can only be `cite_only`. Posters are not peer-reviewed. Candidates listed in `docs/USULAN-SUMBER-v0.7.md` §C:
  ECR 2019 C-1421 for skeletal tuberculosis and ECR 2022 C-13882 for periosteal (and parosteal) osteosarcoma; nothing
  dedicated for desmoplastic fibroma. None read in full yet.

### Proposed and partly applied (2026-11-22)
- `docs/USULAN-SUMBER-v0.7.md` — source fixes that touch `source_ids` only (no weight changes, so scores and ranking
  stay identical):
  - **A. Chondromyxoid fibroma → S-18 (applied, see above).** Claim-by-claim table for all 46 CMF claims against the CMF section of S-18.
    Drop S-06 from the 44 claims that cite it (it has no CMF content) and add S-18 to 19 claims. Result: 20 of 46 CMF
    claims would cite a source that discusses the finding (now 1): 13 supported, 7 direction only; 23 not discussed by
    S-18; the three 10–19 age claims do not fit S-18, which says young adults (bears on H-02).
  - **B. Candidate open-access sources (incomplete).** Chordoma: Ariyaratne et al. 2023, Primary Osseous Malignancies of
    the Spine (Diagnostics, CC BY 4.0, doi 10.3390/diagnostics13101801). Vertebral haemangioma: Ariyaratne et al. 2023,
    Primary Benign Neoplasms of the Spine (Diagnostics, CC BY 4.0, doi 10.3390/diagnostics13122006). Both known from
    abstract and licence metadata only; not yet read in full. Nothing adequate found yet for desmoplastic fibroma
    (two CC BY-NC case reports only), skeletal tuberculosis or periosteal osteosarcoma.

### Added (2026-11-22) — full-text source check of KB 0.6.0 (review only: no weight, entity, feature, source, UI or schema change)
- `docs/TINJAUAN-SUMBER-v0.6.md`: does the source CITED by a claim support it? Redoes §3.5 of the scoring review on full
  text. Fourteen articles read in full from PubMed Central (S-01, S-04, S-05, S-06, S-10, S-15, S-16, S-19, S-20, S-22,
  S-23, S-24, S-25, S-26) and S-18 from the PDF supplied by the owner. Only S-21 (one claim) was not read. Done by a
  separate high-effort model pass, checked by the main session. **It does not judge whether a weight is clinically right.**
- 312 claims checked (19.7% of 1584) in four sets, plus the 5 rules:

  | Set | n | supported | partly | not found | contradicted |
  |---|---|---|---|---|---|
  | A — the 73 hard constraints flagged b/c by the scoring review | 73 | 3 | 28 | 39 | 3 |
  | B — all +3 claims | 192 | 107 | 51 | 34 | 0 |
  | D — random sample of the rest (seed 20261121), the only unbiased set | 40 | 9 | 11 | 20 | 0 |

  Set D, 95% interval: supported 12–38%, not found 35–65%. The rule was strict (membership of an S-01 list counts as
  direction only); with list membership accepted, set B would be 131 of 192 supported.
- Contradicted by their own cited source (3): chondroblastoma `soft_tissue_mass:present` −5 (S-06), fibrous dysplasia
  `margin_lodwick:IC` −5 (S-22), telangiectatic osteosarcoma `margin_lodwick:IA` −5 (S-15).
- Sourcing is the main problem: claims citing only S-01 are supported in 11 of 56 (set B) and 0 of 15 (set D), against
  96 of 136 and 9 of 25 with a second source. No radiographic source at all for chordoma, desmoplastic fibroma and
  skeletal tuberculosis; location only for vertebral haemangioma and periosteal osteosarcoma; S-01 lists only for brown
  tumour, geode and intraosseous lipoma. Second sources without radiographic content for the entity: S-06 for CMF,
  S-24 for myeloma, S-15 for periosteal osteosarcoma, S-04 for Ewing and osteochondroma (208 claim citations).
  S-18 has a full CMF section but is cited by 1 of 46 CMF claims.
- Effect on the scoring review's hypotheses: strengthened H-06, H-08 (osteomyelitis), H-09, H-10, H-11, H-12
  (telangiectatic), H-14, H-16, H-26; weakened H-13 for BPOP `juxtacortical_continuous` and H-15 for the weight (the cited
  sources support those −5); the rest unchanged. Of the earlier 50-item spot-check, 46 were re-judged: 31 the same, 15 changed.
- Files: `tools/review_sources.py` (validates every evidence row against the KB, draws set D, combines verdicts),
  `tools/review_source_evidence.tsv` (526 findings, one per claim per source, with locator and own-words note),
  `tools/review_source_coverage.tsv` (entity × source), `docs/tinjauan-sumber-v0.6.csv` (verdict per claim). The full
  script output is not stored; regenerate with `python3 tools/review_sources.py`.
- Limits: one reviewer, no second rater; figure contents were not readable (S-01 Fig. 1 and 3 may support some age and
  location claims now marked not found); the main session re-checked the counts, the S-06 evidence and two S-18
  findings, not the verdicts resting on the other twelve sources.
- `data/sources.json` unchanged. S-18's licence statement (CC BY-NC-ND, open access) was seen on the article's first page.

### Added (2026-11-21, later) — scoring review of KB 0.6.0 (review only: no weight, entity, feature, UI or schema change)
- `docs/TINJAUAN-SKOR-v0.6.md`: consistency and plausibility review of the scoring, done at the owner's request by a
  separate high-effort model pass and checked by the main session. **Not validation; nothing applied.** Output is 34
  hypotheses for v0.7 (H-01 … H-34) and 7 schema-level options (S-1 … S-7, owner approval needed), to be tested on
  practice cases under the pre-registered protocol.
- `tools/review_scoring.py` (read-only, standard library, about 2 minutes) prints every figure in the report and writes
  `docs/tinjauan-skor-v0.6-hard-constraints.csv` (all 322 hard constraints classed a/b/c with reason and confidence).
  `tools/review_cases_v1_v4.txt`: compact transcription of the 193 coded cases, verified by re-scoring (193/193 match
  the stored rank and score). The full script output (138 KB) is not stored; regenerate it with the script.
- Main findings:
  - Normal/absent findings (`cortex:intact`, `periosteal:none`, `matrix:none`) carry 16 weights of +3; bone infarct
    outranks enchondroma and intraosseous lipoma on their constructed textbook vignettes (H-01).
  - CMF and GCTB over-calling is structural: highest attainable scores on the six core features (GCTB 18, CMF 17,
    median 14); CMF in the top 3 in 58% of adolescent long-bone lytic combinations (H-02, H-03).
  - Attainable maximum ranges from 14 (BPOP) to 26 (Ewing, osteoid osteoma); rare entities also have lower ceilings.
  - Hard constraints: 249 judged justified, 65 questionable, 8 inconsistent (47 of the 73 flags at low confidence).
    In v1–v4 the reference entity is excluded in 7 of 193 cases by 9 claims (H-06 … H-18).
  - `matrix:ground_glass` excludes 27 of 37 entities in one tap; 318 of 322 hard constraints have no `note_id` (H-27).
  - The Ewing/lymphoma soft-tissue rule fired 15 times in v1–v4, always through `cortex:focal_breach` (H-05).
  - Sourcing: 41.7% of claims cite only S-01, 14 entities cite nothing else; 44 of 46 CMF claims cite S-06, which
    has no CMF section (confirmed on the full text). Spot-check of 50 claims, weighted towards flagged ones:
    22 supported, 10 partly, 12 not found in the cited source, 6 contradicted by it (H-26, H-28).
  - 48 reviewer-constructed vignettes (not validation): expected entity first in 40, top 3 in 47.
- Limits stated in the report: the a/b/c classes and the vignettes are the reviewer's judgement and need the owner's
  clinical assessment; several sources were read only through page summaries; S-18 and five others were not checked;
  Axis A was not reviewed.

### Added (2026-11-21) — scoring reference views (no weight, entity, feature, UI or schema change; KB content still 0.6.0)
- **Scoring matrix** page, artifact "TumTul scoring matrix" (https://claude.ai/artifact/Do4A9wGh2uZFZzU9UxN8yv):
  all 37 entities against the 62 feature values offered in the app, every weight colour-coded (+3 hallmark, +2 typical,
  +1 compatible, 0 stated neutral, dot = no claim, −2 unusual, −5 hard constraint), with the prevalence prior as its own
  column. Below the matrix: the 5 special rules with their conditions, the priors by class, and the Axis A point table.
  Tap a cell for its note (Indonesian, as stored) and source codes; tap an entity name for prior, hallmarks and counts.
  Filter by behaviour; order by WHO group, name or number of hard constraints. English labels, Negatoskop tokens,
  light and dark. Read-only: it reads the KB and stores nothing.
- `tools/build_matrix.py` + `web/matrix_template.html` → `web/matrix.html`. The script stops on an unknown feature
  value, WHO group or behaviour, and prints the counts shown on the page. KB 0.6.0: 37 entities, 62 values, 1584
  weighted claims (192 / 248 / 382 / 179 / 257 / 322 at +3 / +2 / +1 / 0 / −2 / −5), 5 rules; the 4 `not_applicable`
  claims (all 0) are counted but not drawn. Column and group labels (`SHORT`, `VS`, `GROUPS`, `BEH`) are display text
  outside the data schema.
- **Scoring flow** Whiteboard "TumTul scoring flow" (https://claude.ai/artifact/DajnwWgBN7vsYrBBA2SKqF): reader's
  features → UI input rules → Axis A (0–9 points, three classes) and Axis B (prior + feature weights + rules →
  any −5? → excluded list, or compatible list ranked with ties sharing a rank) → screen. Hand-drawn from
  `docs/SKEMA-DIAGNOSIS.md` §4 and `web/template.html`; not generated.
- `docs/HANDOFF-SKORING.md`: handoff for the next session.
- Built from the entity files in GitHub `harmenreza/TumTul` (commit b37defc); spot-checked against
  `data/validation/kb_snapshot_v0.6.0.json`. Checked headlessly at 400 px light and 1400 px dark: no horizontal page
  scroll, no script errors.

### Fixed (documentation, 2026-11-21)
- `README.md` "Scoring logic": the formula now includes `base_prior` (in the scorer since v0.6.0; the README line
  had not been updated).

### Not done (2026-11-21)
- The new files of 2026-11-21 (matrix script and template, handoff, review report, CSV, review script and case
  transcription) are in the project store only; they have not been pushed to the GitHub repository.

### Added (UI only, 2026-11-19, later) — expertise-style findings summary (owner-approved mockup, variant B)
- **"Deskripsi temuan"** strip above the results on both Sumbu A and Sumbu B: the filled features are assembled into one
  radiological description sentence. Collapsed it shows two lines; tapped, it opens to the full sentence, a context
  line (age group, clinical flags), the list of features not yet filled, and a **Salin** (copy) button that copies the
  sentence only. Each phrase can be tapped to reopen that feature's picker.
- Assembly order: density, multiplicity, location, transverse position, size, then positive findings ("dengan …") and
  negative findings ("tanpa … maupun …"). Unfilled features are never mentioned in the sentence.
- The sentence only restates the user's entries. It does not read weights, scores or entities and never names an
  entity or a behaviour (aggressive/benign/malignant). The phrase dictionary (`EK`, `EK_NEG`, `EK_AGE`, `EK_CLIN` in
  `web/template.html`) is display text, like the pictograms; the data schema is unchanged (v1.1.0).
- Owner wording decision: cortex "Ekspansi dengan cangkang tipis" is phrased "ekspansi korteks dengan penipisan".
- Nothing is stored; copying happens only on the user's tap.
- Verified headlessly at 400 px, light and dark: no horizontal scroll, no script errors, ranking for the built-in
  example unchanged.

### Changed (UI only, 2026-11-19 — no weight, entity, feature or schema change; KB content still 0.6.0)
- **Location map** (owner-approved mockup): the tiles "Posisi longitudinal" and "Posisi transversal" now open one sheet
  "Lokasi lesi" with two original diagrams — a long bone in longitudinal section (tap epiphysis / metaphysis /
  metadiaphysis / diaphysis; both ends highlight together because the KB does not distinguish proximal from distal)
  and a cross-section (central, eccentric, intracortical, surface, surface with continuity). Buttons beside each diagram
  give the same choices for keyboard and screen-reader use. Feature codes, dependency rule (long bone only) and
  conflict rules are unchanged; the conflict notice is shown inside the sheet.
- **Pictograms** in the pickers for margin (Lodwick IA–III), periosteal reaction (7 values) and matrix (5 values):
  own schematic drawings in radiograph convention (light = dense bone, dark = lucent). Not patient images; no licence
  obligation. About page explains both.
- Verified headlessly at 400 px, light and dark: no horizontal scroll, no script errors, conflict rule and ranking unchanged.
- Design mockup kept at https://claude.ai/artifact/TtqriTDXt8ourmMVCYXgFN.

### Released to the web prototype (2026-11-17, later) — 2 more example images approved
- Owner approved both third-pass candidates (chordoma #2, osteomyelitis #2). `data/images.json` v0.3.1: 66 approved
  images for 32 entities. Prototype rebuilt and republished; LICENSES §6 count CC BY 33 → 35.

### Added (2026-11-17) — third image search pass, 2 candidates (approved, see above)
- New Europe PMC pass (`GAP=2`, `tools/pmc_queries_gap2.json`) over CC BY radiology review journals and pictorial reviews for the 17 under-covered entities; figures kept only when the caption names the entity, mentions a radiograph, has no atypical wording and the original is >= 500 px. "Rare" in an article title is now flagged for manual check instead of dropped.
- 23 figures returned; 21 rejected on screening (radiograph panel under 500 px after cropping, post-treatment, chest radiographs, or not typical).
- 2 candidates added to `data/images.json` (v0.3.1) with status `candidate`: chordoma #2 (sacral chordoma, AP pelvis; Ariyaratne et al., Diagnostics 2023, CC BY 4.0) and osteomyelitis #2 (chronic osteomyelitis of the femur; Desimpel et al., J Belg Soc Radiol 2017, CC BY 4.0). They are not shown in the app until approved.
- Still without images: clear cell chondrosarcoma, periosteal chondroma, vertebral haemangioma, desmoplastic fibroma, periosteal osteosarcoma.

### Released to the web prototype (2026-11-17) — example images approved
- Owner reviewed all 64 candidates and approved all 64 (`data/images.json` v0.3.0, every record `status: "approved"`).
  The Sumbu B gallery is now live in the published prototype for 32 entities; the other 5 show
  "Contoh gambar untuk entitas ini belum tersedia."
- About page text updated: sources (Wikimedia Commons and PubMed Central open-access figures), licences, pre-treatment,
  typical-only, ≥ 500 px, own-words captions, images never analysed.

### Added (UI + tooling; no weight, entity, feature or KB-schema change)
- Sumbu B: per-entity button **"Lihat contoh gambar (n)"** in the expanded row; opens a bottom-sheet gallery
  (up to 3 radiographs, black frame, caption in our own words, attribution line under each image: file title
  with link, author, repository, licence with link, changes made). Note in the gallery: examples are for
  shared terminology, not for matching a case. Entities without approved images show "Contoh gambar … belum
  tersedia". About page states the image licensing policy. Verified headlessly with placeholder images
  (light and dark, 400 px, no overflow, no script errors). **Not yet published** — waits for real images.
- `data/images.json` v0.1.0: example-image registry, kept **separate from the knowledge base**
  (`schema/kb-schema.json` untouched). Only `status: "approved"` records are shown. Empty for now.
- `tools/build_web.py`: embeds the registry, checks that approved records name a known entity, carry the
  mandatory attribution fields and that the image file exists under `web/`.
- `tools/fetch_commons.py` + `tools/commons_queries.json` + `.github/workflows/fetch-commons.yml`: collects
  candidate radiographs from Wikimedia Commons on a GitHub Actions runner (this workspace cannot reach
  Commons). Keeps only CC0 / public domain / CC BY / CC BY-SA files, records full attribution metadata,
  flags likely non-radiographs (histology, CT/MRI, animals, photos), saves 640 px thumbnails and numbered
  contact sheets per entity for screening. Tested offline with mocked API responses.

### Added (2026-11-17) — example-image candidates, awaiting owner review
- 92 candidate radiographs for 36 of 37 entities, screened visually from two free sources:
  Wikimedia Commons (CC0 / public domain / CC BY / CC BY-SA) and figures of open-access articles in
  PubMed Central under CC BY / CC BY-SA / CC0 (licence read from each article's XML; figures whose caption says
  reprinted/reproduced/with permission are excluded). Pre-treatment radiographs only; panels cropped to the
  radiograph where a figure also held CT/MRI/histology (stated as "dipotong" in the attribution).
  Excluded on screening: mimic cases (e.g. synovial osteochondroma imitating parosteal OS, OI callus imitating
  periosteal OS), other-entity figures in review articles, post-operative images, heavy overlays.
- 3 images for 26 entities; fewer for chondromyxoid fibroma, LCH, enostosis, osteoblastoma, osteomyelitis,
  Paget (2), chordoma, clear cell CS, Ewing sarcoma, periosteal OS, periosteal chondroma (1);
  **vertebral haemangioma: none** (no freely licensed typical radiograph found).
- `data/images.json` v0.2.0 (all `status: "candidate"`, so nothing shows in the app yet), `web/img/*.jpg`
  (max 900 px), `tools/assemble_images.py`, `tools/image_picks.json`, `tools/image_captions_id.json`.
  Images are kept in the GitHub repository harmenreza/TumTul (the project store holds text only).
- Fetchers: Commons fetcher gained category retrieval and radiograph-first ranking; new
  `tools/fetch_pmc.py` (Europe PMC search, images from the public PMC Open Access S3 bucket because
  europepmc.org refuses automated image downloads) with a targeted gap pass (`tools/pmc_queries_gap.json`).
- Review sheet artifact "Tinjauan Gambar TumTul" (https://claude.ai/artifact/QJaFQ1VKudCtcoUHGa1Mi2):
  approve/reject per image with notes; decisions are pasted back into the chat and applied to `status`.

### Changed (owner rule, 2026-11-17) — typical images only
- Owner: the gallery is an atlas of the **most typical** radiograph of each entity; no images from sources that
  describe the case as atypical. 12 candidates removed because their source says atypical / unusual /
  rare location / aggressive / giant / multifocal / misdiagnosed or mistaken for another lesion
  (adamantinoma multifocal; BPOP ×2 "two atypical cases"; aggressive chondroblastoma; CMF "localisation rare";
  desmoplastic fibroma "unusual lesion" and "rare case" of the scapula; clear cell CS "unusual case";
  Brodie abscess "unusual cause"; telangiectatic OS "misdiagnosed as ABC"; giant periosteal chondroma;
  spinal TB "mistaken for metastatic cancer"). Also removed on review: a "very subtle" chondroblastoma and
  an osteoblastoma of the capitate (uncommon site). Two typical chondroblastomas added (proximal tibial
  epiphysis, patella). "Giant cell tumour" and "atypical cartilaginous tumour" are entity names and are not
  treated as atypical wording.
- Now **80 candidates, 34 entities**; 0 images for clear cell chondrosarcoma, periosteal chondroma and
  vertebral haemangioma. Both fetchers skip such sources automatically (`ATYPICAL` filter on article title,
  figure caption and Commons description). Review sheet republished (decisions key reset).

### Changed (owner rule, 2026-11-17) — minimum resolution 500 px; review sheet fix
- Owner: fix low-resolution images. New rule: the **longest side after cropping must be at least 500 px**.
  The full-resolution originals were fetched (`tools/fetch_hires.py`, workflow `fetch-hires.yml`: Commons
  original or 2560 px rendering, largest PMC figure file from the PMC open-access S3 bucket); most small images
  were already at their original size, so they could not be upscaled honestly and were removed.
- 20 removed as below 500 px (brown tumour ×2, chondroblastoma ×2, central chondrosarcoma ×2, GCT ×2,
  conventional OS ×2, osteoid osteoma ×2, telangiectatic OS, parosteal OS, periosteal OS, desmoplastic fibroma,
  skeletal TB, stress fracture, fibrous dysplasia, myeloma); 4 typical high-resolution replacements added (fibrous
  dysplasia of a rib, GCT of distal femur, conventional OS of distal femur, multiple myeloma of the shoulder).
- `tools/assemble_images.py` now builds from the full-resolution original, output max 1600 px, JPEG q84, and
  warns below 500 px. `tools/measure_pool.py` + workflow `measure-pool.yml` record candidate pixel sizes.
- Now **64 candidates, 32 entities** (smallest 502 px, most 750–1600 px). No image yet for clear cell
  chondrosarcoma, periosteal chondroma, vertebral haemangioma, desmoplastic fibroma, periosteal osteosarcoma.
- Review sheet: each image sits in a fixed-height frame (tap to enlarge), and the decision bar is compact, so
  the Setujui/Tolak buttons are always visible. Decisions key reset (`tumtul-review-v3`).

### Decided (owner, 2026-11-16)
- Example images: radiographs only (CT only where no typical radiograph exists, and flagged); 3 per entity;
  freely licensed sources with attribution under each image; images fetched via a GitHub repository.

## [0.6.7] — 2026-11-11

### Changed (UI only — no weight, entity, feature or schema change; KB content still 0.6.0)
- Visual theme **"Negatoskop"** chosen by the owner (option A of three proposed). Warm film-viewer light mode
  (background #F3EFE6, text #1C2024) and a near-black PACS reading-room dark mode (#0E1215, text #E7E3DA).
  Colour roles: **rust** (#A3471F / dark #E8935F) for what the app computes — active tab, score bar, bottom-nav
  selection; **teal** (#2E5C63 / dark #7FB6BC) for what the user entered and what is cited — filled tiles, picker
  selection, source links, licence tags. All text/background pairs checked ≥ 4.5:1 (WCAG AA) in both modes.
- Typography: Source Serif 4 for the app title, panel headings, entity names and picker titles; IBM Plex Sans
  for UI text; IBM Plex Mono for scores, ranks and version labels (unchanged).
- Behaviour pills (jinak / intermediate / ganas / non-neoplastik) are now neutral; the label carries the meaning,
  colour no longer grades the ranked list. Axis A badge keeps a three-step scale (teal / ochre / brick).
- Feature-tile hint reworded ("Bertanda centang = sudah diisi") since filled tiles are no longer green.
- New **display-mode switch** in the header: Sistem / Terang / Gelap (radio group with labels). Choice is kept in
  the browser's localStorage under `tumtul-theme` on this device only (display preference, no patient data;
  falls back to the system setting if storage is unavailable). Stated on the About page.
- Verified headlessly at 400 px in light and dark: no horizontal scroll, no script errors, switch persists across
  reload and "Sistem" clears the stored value. Artifact republished at the same URL.

## [0.6.6] — 2026-11-10

### Added (study planning only — no weight, entity, feature, UI or schema change; KB content still 0.6.0)
- Research proposal draft for the practice-case validation ("Studi VALID-TumTul"), kept as a Claude Docs
  document (https://claude.ai/artifact/TGKRyBf3viaYsbkgaXyN91); summary and pointer in
  `docs/PROPOSAL-VALIDASI-PRAKTIK.md`. Two stages on the same consecutive, histology-proven cases:
  Stage 1 diagnostic accuracy (200 cases; features read independently by two expert readers, consensus features
  scored on the frozen KB; primary Top-3 tested against a 65% performance goal, exact one-sided binomial) and
  Stage 2 crossover multi-reader multi-case study (12 readers × 80 cases, with vs without TumTul, ≥ 4-week
  washout; Obuchowski–Rockette analysis). Secondary: Axis A vs malignancy, harmful/beneficial answer changes,
  per-feature agreement, System Usability Scale. Reporting per STARD 2015, DECIDE-AI (relevant items), GRRAS.
- `tools/sample_size_p1.py`: exact binomial power for Stage 1 (n = 200 → 85.5% power for 75% vs 65%) and
  simulation-based power for Stage 2 (12 × 80 → 95.1% / 89.4% for a 10-point difference under base / high
  variability; seed 20261110). All Stage 2 parameters are assumptions, to be re-checked on Stage 1 data.

### Proposed (awaiting owner decision; nothing applied)
- Primary population = all eligible cases within the v1 anatomical scope; reference diagnoses outside the
  37 entities stay in and count as misses.
- Conservative tie rule for the primary endpoint (rank = number of entities scoring ≥ the reference entity);
  differs from the v1–v4 convention, which is kept as a sensitivity analysis.
- Practice-case form: session/condition marker and start timestamp for Stage 2 (form data dictionary change;
  KB schema untouched).
- Storage of study data (artifact database on a third-party cloud vs institutional server) to be declared to the
  ethics committee.

## [0.6.5] — 2026-11-10

### Changed
- App renamed **TumTul** (short for *Tumor Tulang*) by the owner, replacing the working title BoneDx.
  Avoids "Dx" in the name, which could read as a diagnostic-device claim. Prototype header carries the
  expansion and tagline "Tumor Tulang · referensi diagnosis banding"; the About page states that the
  scope includes non-neoplastic tumour mimics. Practice-case form renamed "TumTul Kasus Praktik";
  default case-code prefix `TT-P` (worklist was empty, no stored codes changed); export files `tumtul_praktik_*`.
- Artifact links unchanged. Historical entries below keep the old name. `schema/kb-schema.json` title
  left as is (schema files change only with owner approval; the title is not user-facing).

## [0.6.4] — 2026-11-10

### Added
- Practice-case reading form (artifact "BoneDx Kasus Praktik"; `web/form_template.html` → `tools/build_form.py`
  → `web/form.html`). Options are generated from `data/features.json` v1.3.0 and the entity list, so codes are
  identical to the app; the app's input rules are mirrored. Reader view (blinding attestation, 13 features,
  reader's own ranked differential, confidence 1–5, imaging available, de-identified notes; final readings lock)
  and coordinator view (case list generator, reference diagnosis and confirmation method hidden from readers,
  per-reader progress, JSON/CSV export in `validate_cases.py` format). Shared artifact database with access rules
  verified at Contributor level. Data dictionary and workflow: `docs/FORMULIR-KASUS-PRAKTIK.md`.
- No patient identifiers are collected; free text with long digit runs, date patterns or record-number keywords is rejected.

## [0.6.3] — 2026-11-10

### Changed (UI only — no weight, entity or schema change; KB content still 0.6.0)
- Ties shown explicitly in Axis B: equal scores share a rank (competition ranking 1, 1, 3 …) with a
  "seri" marker and a note that order within a tie carries no clinical meaning; every entity tied with
  5th place is listed (up to 10 rows). Lower-scored list shows ranks too. (Proposed in v3, supported by v4.)
- Sparse-input warning when fewer than 6 features are filled (v3: ¾ of cases below this; v4 misses
  concentrated at 2–3 features).
- Input rules extended after a systematic review of all value pairs against definitions and the 193
  coded cases of v1–v4 (owner decisions 2026-11-10), documented in `docs/SKEMA-DIAGNOSIS.md` §2:
  - Lodwick tile disabled for surface lesions (`juxtacortical_surface`, `juxtacortical_continuous`).
  - Mutually exclusive pairs (later choice wins, earlier value cleared with a notice; the picker warns
    beforehand): surface lesion × endosteal scalloping; cortico-medullary continuity × lytic density.
  - Rare-but-possible pairs deliberately left to the weights (listed in §2).
- About page: schema version label corrected to v1.1.0; explains ties and input rules.

## [0.6.2] — 2026-11-10

### Added (validation only — no weight or content change)
- Pre-registered set v4: illustrative patient cases from open-access review articles (owner request,
  to remove the atypical bias of case reports). Protocol `docs/VALIDASI-v4-PROTOKOL.md`, brief
  `docs/validation-brief-v4.md` (registry sources and v1–v3 PMCIDs excluded; only the illustrated
  patient coded, never generic entity text), nine blind coders (`data/validation/raw_v4/groupA–I.json`).
- 38/74 slots filled (figure legends unavailable through the PubMed full-text tool for most
  publishers; PMC/Europe PMC blocked); 2 documented eligibility exclusions (CT/MRI only,
  `data/validation/v4_exclusions.json`); 36 analysed, 92% typical, mean 4.5 coded features.
- Result: **primary criterion not met** — Top-3 69% (threshold ≥ 80%); Top-1 47%, Top-5 83%,
  0 excluded by hard constraints, prior effect +1 (S3 passed). Tie-aware Top-3 81%.
  Report `docs/VALIDASI-INTERNAL-v4.md` with a v3–v4 comparison: typicality raised Top-3 by
  21 points despite fewer features; input sparsity now the limiting factor.
- `tools/validate_cases.py`: `EXCLUDE` option for documented eligibility exclusions.

## [0.6.1] — 2026-11-10

### Added (validation only — no weight or content change)
- Pre-registered confirmation set v3: protocol `docs/VALIDASI-v3-PROTOKOL.md` (criteria fixed
  before coding; Amendment 1 before analysis), KB frozen as `data/validation/kb_snapshot_v0.6.0.json`,
  brief `docs/validation-brief-v3.md`, 52 new case reports in prevalence-weighted proportions
  selected quasi-consecutively (newest-first, first eligible) by seven blind coders
  (`data/validation/raw_v3/groupJ–P.json`, `cases_v3.json`, `results_v3.md`, `results_v3_noprior.md`).
- `tools/validate_cases.py`: `KB_SNAPSHOT` (score against a frozen KB) and `NO_PRIOR=1`
  (disable `base_prior`) options.
- Result: **primary criterion not met** — Top-3 48% (threshold ≥ 75%); Top-1 21%, Top-5 58%,
  5 excluded; prior effect neutral-to-positive (S4 passed). Typical cases 42/68/84%.
  63% of v3 cases atypical, mean 6.0 coded features. Report `docs/VALIDASI-INTERNAL-v3.md`
  with v0.7 hypotheses (CMF and GCTB overcalls, explicit ties in UI, sparse-input warning),
  none applied. Recommendation: no accuracy claims; next validation must use practice cases.

## [0.6.0] — 2026-11-10

### Schema (owner-approved) — `schema/kb-schema.json` v1.1.0
- New optional entity fields: `base_prior` (−2 | −1 | 0), `base_prior_note_id`,
  `base_prior_source_ids`. Score = base_prior + feature weights + rule weights.

### Decided (owner)
- All six v2 hypotheses applied; UI dependency rules: longitudinal position only when bone is a
  long bone, Lodwick margin only when density is lytic or mixed.

### Added / Changed
- `data/features.json` 1.3.0: `matrix: coarse_trabeculae` (vertebral haemangioma +3, Paget +1,
  metastasis/myeloma −2). `not_applicable` values kept in the KB but hidden in the UI.
- Prevalence priors: −2 desmoplastic fibroma, clear cell CS, OFD–adamantinoma, BPOP, periosteal
  chondroma, parosteal OS, periosteal OS; −1 telangiectatic OS, chordoma, CMF, lymphoma,
  osteoblastoma, chondroblastoma, brown tumour, intraosseous lipoma, Paget; 0 otherwise
  (skeletal TB deliberately 0 for the Indonesian context).
- Relaxed hard constraints (−5 → −2): geode at 10–19 open physis, brown tumour cortical
  destruction, CMF lamellated periosteal reaction, intracortical lipoma.
- Weights: osteomyelitis 20–39 +1→+2 and endosteal scalloping 0→+1; skeletal TB spine body
  +3→+2, lytic +3→+2, soft-tissue mass +2→+1; GCTB long bone +2→+3; bone infarct flat bone 0→−2.
- Reference scorer and web prototype add the prior as a "Prevalensi" reason row; smoke test
  counts a tie for first as a pass (20/20).
- Web prototype: dependent tiles are greyed with an explanatory label and cleared
  automatically when the parent changes; verified headlessly. KB label 0.6.0.
- Validation: v2 post-hoc 45/70/76% (excluded 6→2); v1 regression 58/84/87%. Report §5.

## [0.5.1] — 2026-11-10

### Added (validation only — no weight or content change)
- Confirmation set v2: 74 new open-access case reports (2 per entity, v1 PMCIDs excluded),
  coded blind by nine independent coders (`docs/validation-brief-v2.md`,
  `data/validation/raw_v2/groupA–I.json`, `cases_v2.json`, `results_v2.md`).
  `tools/validate_cases.py` now takes a set name (`v1` | `v2`).
- Result at v0.5.0: all 74 — Top-1 39%, Top-3 68%, Top-5 76%, 6 excluded; typical cases
  (n=42) — 52/74/83%; typical with ≥8 coded features (n=18) — 72/89/100%.
- `docs/VALIDASI-INTERNAL-v2.md`: stratified results and six systematic findings recorded
  as hypotheses for v0.6 (prevalence prior — schema decision; vertebral-haemangioma
  trabecular pattern value; four over-strict hard constraints; adult osteomyelitis vs TB;
  GCTB long-bone weight; coding-conflict rule). Nothing applied.

## [0.5.0] — 2026-11-09

### Decided (owner)
- Three feature values approved after validation v1 (feature enumeration only; schema
  structure unchanged): `transverse: juxtacortical_continuous`, `cortex: saucerization`,
  `periosteal: present_unspecified`. `data/features.json` → 1.2.0.
- App opens with an empty form (no example preloaded).

### Added / Changed
- Generators: `CONTINUITY_OVERRIDES` (osteochondroma +3; parosteal OS, BPOP, periosteal
  chondroma, periosteal OS −5; others inherit juxtacortical_surface), `SAUCERIZATION_OVERRIDES`
  (periosteal chondroma +3, periosteal OS +2, osteochondroma −2), derived
  `present_unspecified` weights (+1 / −2 / 0 rule; explicit 0 for skeletal TB).
  1580 weighted claims; validation passes; smoke tests 19/20.
- Validation v1 re-run after recoding five cases with the new values: Top-1 18/31 (58%),
  Top-3 27/31 (87%), Top-5 28/31 (90%). Report §4a added.
- Web prototype: bottom navigation no longer covers the last content on phones (body
  `height:100%` removed; spacer + `scroll-padding-bottom` sized to the nav and safe area);
  opens empty with an explanatory empty state. KB label 0.5.0.

## [0.4.1] — 2026-11-09

### Added
- Internal validation v1: 31 open-access, histopathologically confirmed case reports
  coded blind to the weights by five independent coders following
  `docs/validation-brief.md` (one case per entity; no OA biopsy-proven bone-infarct case
  report exists). Files: `data/validation/raw/group1-5.json`, `cases_v1.json`,
  `results_v1_pre.md`, `results_v1.md`; runner `tools/validate_cases.py`; report
  `docs/VALIDASI-INTERNAL-v1.md`.
- Result at v0.4.0: Top-1 17/31 (55%), Top-3 24/31 (77%), Top-5 27/31 (87%), 1 excluded.
  After corrections (v0.4.1): Top-1 55%, Top-3 26/31 (84%), Top-5 87%, 0 excluded.

### Changed (weights, post-hoc — to be confirmed on a fresh case set)
- Osteochondroma: age 20–39 +1→+2, density sclerotic +1→+2. Parosteal osteosarcoma:
  long_bone +3→+2.
- NOF: margin IB 0→+1. Osteomyelitis/Brodie: margin IA +2→+3.
- Brown tumour: soft_tissue_mass present −5→−2 (pathological fracture), cortex
  focal_breach 0 (explicit).
- Skeletal TB: density mixed −2→+1, margin IA 0→+1 (chronic forms).
- Smoke tests unchanged (19/20).

### Proposed (awaiting owner decision; feature-value additions, no schema change)
- `transverse: juxtacortical_continuous`, `cortex: saucerization`,
  `periosteal: present_unspecified` — see report §4.

## [0.4.0] — 2026-11-09

### Changed (web prototype, mobile-first redesign per owner spec)
- Bottom navigation: Penilaian · Sumber · Tentang (fixed, safe-area aware).
- Penilaian split into a sticky segmented control: Fitur (with filled-count badge) ·
  Sumbu A · Sumbu B.
- Features are large square tiles (2 columns on phones, 3 on tablets, 4 on desktop) with
  an original line icon, title and current value; tapping opens a bottom-sheet picker
  with option help text and a "Tidak diketahui / ragu" clear option; filled tiles get a
  green border, tinted background and a check mark. Multi-select features (clinical
  flags) use checkboxes with a "Selesai" button.
- "Fitur yang paling mengubah peringkat" items are now tappable and open the picker.
- Scoring, Axis A thresholds, excluded-entity display and Sources tab unchanged.
  Verified headlessly at 400 px (no horizontal scroll, no console errors).

## [0.3.3] — 2026-11-09

### Changed
- Licence verification completed for all 14 `to_verify` sources (publisher/PMC pages or
  PDFs; exact statements in `license_note`). Result: CC BY 4.0 confirmed for S-01, S-03,
  S-09, S-10, S-11, S-20, S-26, S-27; CC BY-NC-ND 4.0 for S-05, S-14, S-18, S-21; no CC
  licence found for S-07 (JACR/ACR) and S-12 (J Carcinogenesis) → reclassified `cite_only`.
  Registry 0.2.0: 24 verified, 6 cite-only, 0 to verify.
- `LICENSES.md` rewritten with final licence classes and the distribution consequence
  (free, ad-free, or replace NC sources).
- UI placeholder for unfilled features changed to "— tidak diketahui / ragu —" (0.3.2 → 0.3.3).
- Web prototype rebuilt (Sources tab reflects the new statuses).

## [0.3.2] — 2026-11-09

### Fixed (from owner testing)
- Entities removed by a hard constraint were only visible inside a collapsed section, so a
  classic entity (GCTB) appeared to be "missing" when e.g. chondroid matrix or mixed density
  was selected. The web prototype now shows up to three excluded entities whose
  constraint-free score would reach the top group as greyed rows inside the main list,
  with the excluding feature and the hypothetical score marked `*`.

### Changed (weights)
- GCTB: margin IA −2 → 0 (thin sclerotic rim possible in latent lesions, S-01/S-16);
  density mixed −5 → −2 (reactive bone, post-fracture, post-denosumab).
- Chondroblastoma: age 20–39 +1 → 0 (most cases 10–25 years).
- Intraosseous ganglion/geode: transverse eccentric +2 → +1.
- Legacy `physis` tables removed from the generators (they were already dropped at build).
- Smoke tests unchanged: 19/20.

## [0.3.1] — 2026-11-09

### Decided (owner)
- Physeal status is folded into the age feature so the two can never contradict:
  `age_group` now has 7 values (0–9 · 10–19 open · 10–19 closed · 10–19 not assessable ·
  20–39 · 40–59 · 60+); the separate `physis` feature is removed. Decision §6-2 revised.
  No change to the data schema structure.

### Changed
- `data/features.json` → 1.1.0 (age values with help text; `physis` removed).
- Generators: `finalize()` expands the 10–19 weight into the three values;
  `PHYSIS_OVERRIDES` gives explicit open/closed weights for 13 physis-sensitive entities
  (GCTB, chondroblastoma, simple bone cyst, NOF, ABC, osteochondroma, Ewing, LCH,
  osteomyelitis, CMF, telangiectatic OS, clear cell CS, geode). All 37 entity files
  regenerated (1511 weighted claims); validation passes.
- `tools/score_smoke.py`: vignettes updated, two added (17-y closed physis → GCTB first;
  13-y open physis → chondroblastoma first, GCTB excluded by hard constraint). 19/20 pass;
  the 20th is the intended Ewing vs osteomyelitis tie.
- Web prototype rebuilt and republished (same URL); example case uses `10-19_open`.
- `docs/SKEMA-DIAGNOSIS.md` §2, §3.1, §6 updated.

## [0.3.0] — 2026-11-09

### Added
- `data/entities/` batch 2 — 18 entities: parosteal, periosteal and telangiectatic
  osteosarcoma; periosteal chondroma; chondromyxoid fibroma; clear cell chondrosarcoma;
  OFD–adamantinoma spectrum; desmoplastic fibroma; primary bone lymphoma; bone infarct;
  Paget disease; brown tumour; enostosis; stress/insufficiency fracture; skeletal
  tuberculosis; intraosseous ganglion/geode; intraosseous lipoma; BPOP. Total 37 entities,
  1443 weighted claims, 5 rules. Validation passes.
- `tools/build_entities_batch2.py`; `tools/score_smoke.py` extended to 18 vignettes
  (17/18 rank the expected entity first; the remaining one is the intended Ewing vs
  osteomyelitis tie).
- `web/template.html`, `tools/build_web.py`, `web/index.html` — self-contained web
  prototype (Indonesian UI): feature form, Axis A aggressiveness badge (0–9 points),
  Axis B ranked list with per-feature reasons and source links, "considered but lower",
  "excluded by hard constraint", next-most-informative-feature heuristic, Sources tab with
  licence status, About tab. Scoring JS verified equal to the Python reference on the
  example case. Published as a Claude artifact.
- `docs/SKEMA-DIAGNOSIS.md` §4.2a — Axis A point table and thresholds.

### Notes
- Weights in batch 2 follow the same conventions as batch 1 and are likewise unreviewed.

## [0.2.0] — 2026-11-09

### Decided (owner)
- Entity names in standard English (WHO) with Indonesian equivalents; UI/notes in Indonesian.
- Age groups fixed at 0–9 / 10–19 / 20–39 / 40–59 / 60+.
- Simple weight scale (−5 / −2 / 0 / +1 / +2 / +3), not likelihood ratios.
- v1 scope: long bones + pelvis + spine (incl. sacrum).
- Closed-access landmark sources may be cited bibliographically (`cite_only`), nothing reproduced.

### Added
- `schema/kb-schema.json` v1.0.0 — frozen; identical structure to the approved draft.
  `schema/kb-schema.draft.json` marked superseded.
- `data/features.json` — 14 input features, ID/EN labels, help text with sources for the
  features with lower inter-reader agreement (periosteal reaction, soft-tissue mass,
  endosteal scalloping; S-27).
- `data/entities/` — batch 1, 19 entities, 752 weighted claims, 3 conjunctive rules:
  osteosarcoma (conventional), osteoid osteoma, osteoblastoma, osteochondroma, enchondroma,
  chondroblastoma, central chondrosarcoma/ACT, GCTB, ABC, NOF, simple bone cyst, fibrous
  dysplasia, vertebral haemangioma, chordoma, plasmacytoma/myeloma, LCH, Ewing sarcoma,
  bone metastasis, osteomyelitis/Brodie.
- `tools/build_entities_batch1.py` (generator), `tools/validate_kb.py` (schema +
  cross-reference validation, passes), `tools/score_smoke.py` (reference scoring; 9/10
  classic vignettes rank the expected entity first, the 10th is a deliberate Ewing vs
  osteomyelitis tie).
- `docs/SKEMA-DIAGNOSIS.md` → v0.2.0: §6 rewritten as decisions table, new §7 on entity
  authoring conventions.

### Changed
- `README.md`: layout, scoring-logic reference, roadmap.

## [0.1.0] — 2026-11-09

### Added
- `docs/SKEMA-DIAGNOSIS.md`: diagnostic scheme v0.1 — binding principles, 7-step
  assessment flow, input feature enumerations, feature→entity tables (age, longitudinal
  and transverse location, specific bones, density, Lodwick–Madewell margins and modified
  grading, cortex/extra-osseous, periosteal reaction, matrix, multiplicity), scoring and
  ranking logic with hard constraints and special rules, initial entity list organised by
  WHO 5th-edition groups, and open decisions.
- `schema/kb-schema.draft.json`: DRAFT JSON Schema for features, entities (weights +3…−5,
  rules, pitfalls, source refs) and sources (licence + licence_status). **Not approved.**
- `data/sources.json`: 30-entry source registry built from PubMed/OpenAlex searches;
  licence checked via PMC metadata where available (12 verified CC BY / CC BY-NC,
  14 to verify, 4 cite-only).
- `README.md`, `LICENSES.md`, `CHANGELOG.md`.

### Notes
- Literature search run 2026-11-09 (PubMed + OpenAlex). Key evidence anchoring weights:
  modified Lodwick–Madewell malignancy rates (S-08), feature-importance ranking from a
  796-patient model (S-09), sign-level PPV from a 88-lesion reader study (S-10), paediatric
  age/location series of 420 cases (S-04), SEER incidence trends (S-05).
- Indonesian local scoring system (S-12, RS Dr. Soetomo) recorded for context.
