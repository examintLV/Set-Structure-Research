# Repository Understanding Audit

**Audit ID:** AUD-001
**Framework version audited:** 1.0.0 (`CHANGELOG.md`)
**Repository commit:** `83c59b9a56e36a8b0796c402a72af0ced534dd28`
**Branch:** `arena/7acbc817-set-structure-research`
**Audit date:** 2026-11-15 (UTC)
**Auditor:** Arena.ai research agent
**Nature of document:** Framework comprehension + data-feasibility reconnaissance. **No match results are analysed in this document.** It contains no findings about tennis set structure, no predictions, and no market data.

---

## 0. Scope and honesty statement

This audit reports three separable things, and keeps them visually separate throughout:

| Tag | Meaning |
|---|---|
| **[READ]** | Directly observed by opening the file. |
| **[RUN]** | Directly observed by executing code and inspecting output. |
| **[NOT CHECKED]** | Asserted by the repository or by a data provider and **not** independently verified by me. |

Nothing marked **[RUN]** is inferred. Nothing marked **[NOT CHECKED]** is claimed as verified. Where I looked for something and it was absent, I say so rather than assuming it does not exist.

One important limit up front: **I read the framework documents, but I have not executed a research study.** This audit is the pre-flight check the prompt asked for. Its purpose is to establish what the framework permits, and — the part that matters more — what the available data can actually support.

---

## 1. Files successfully accessed

### 1.1 Repository framework files — all 19 files [READ]

The repository root contains only a 24-byte placeholder `README.md` (`# Set-Structure-Research`); **all framework content lives one level down** in `Set-Structure-Research-v1/Set-Structure-Research/`. Nothing was missing.

| # | File | Lines | Status |
|---|---|---:|---|
| 1 | `README.md` (repository map) | 45 | [READ] complete |
| 2 | `AGENTS.md` | 40 | [READ] complete |
| 3 | `RESEARCH_CHARTER.md` | 67 | [READ] complete |
| 4 | `PROTOCOL.md` | 72 | [READ] complete |
| 5 | `FILTER_CATALOG.md` | 95 | [READ] complete |
| 6 | `DATA_DICTIONARY.md` | 73 | [READ] complete |
| 7 | `SOURCE_STANDARDS.md` | 26 | [READ] complete |
| 8 | `DATA_COLLECTION_SOP.md` | 12 | [READ] complete |
| 9 | `STATISTICAL_METHODS.md` | 38 | [READ] complete |
| 10 | `ANALYSIS_PLAYBOOK.md` | 38 | [READ] complete |
| 11 | `QUALITY_CONTROL.md` | 55 | [READ] complete |
| 12 | `REPORT_TEMPLATE.md` | 95 | [READ] complete |
| 13 | `DATA_SCHEMA.json` | 381 | [READ] complete, parsed |
| 14 | `CHANGELOG.md` | 10 | [READ] complete |
| 15 | `templates/STUDY_SPECIFICATION.md` | 23 | [READ] complete |
| 16 | `templates/RESEARCH_LOG.csv` | 1 (header) | [READ] empty apart from header |
| 17 | `templates/CORRECTION_LOG.csv` | 1 (header) | [READ] empty apart from header |
| 18 | `tools/validate_records.py` | 55 | [READ] complete, executed [RUN] |
| 19 | `tools/test_validate_records.py` | 26 | [READ] complete, executed [RUN] |

Root-level placeholder `README.md` read [READ]. No `LICENSE`, no `.gitignore`, no `.github/` (CI), no `data/`, `studies/`, `reports/`, `sources/`, `scripts/`, or `analyses/` directory exists [RUN].

### 1.2 External sources accessed for feasibility reconnaissance [RUN]

All retrieved through `api.github.com` with retrieval timestamps and SHA-256 hashes logged in `audits/artifacts/source_access_log.csv`. **11/11 requests returned HTTP 200.**

| Target | Bytes | Purpose |
|---|---:|---|
| `Aneeshers/tennis-sackmann-archive` metadata + directory listings (`atp/`, `wta/`, `slam_pointbypoint/`) | 189,941 / 134,649 / 197,030 | Source inventory |
| `atp/matches_data_dictionary.txt` | 3,758 | Field semantics |
| `atp/atp_matches_2024.csv` | 650,136 | Structural test |
| `slam_pointbypoint/2024-wimbledon-points.csv` | 7,827,299 | Set-level feasibility test |
| `slam_pointbypoint/2024-wimbledon-matches.csv` | 20,457 | Match join test |
| `JeffSackmann/tennis_MatchChartingProject` metadata + `charting-m-matches.csv` + dictionary | 6,673 / 1,141,817 / 2,649 | Coverage test |

Additional files were pulled earlier in the same session for field and coverage checks: `atp_matches_1991/2000/2010/2020/2023.csv`.

### 1.3 Access routes that failed [RUN] — important for planning

| Host | Result | Consequence |
|---|---|---|
| `www.atptour.com`, `www.wtatennis.com`, `tennisabstract.com`, `www.tennis-data.co.uk` | HTTP 000 (connection blocked) | **Official tour records are not directly reachable from this sandbox.** |
| `raw.githubusercontent.com` | TLS error (`SSL_ERROR_SYSCALL`) | Raw file route unusable. |
| `api.github.com` | HTTP 200 | **Only working bulk-data route.** |
| `pypi.org` | HTTP 200 | Could install `jsonschema`/`pandas` if needed. |

Consequence: this environment **cannot** satisfy the source hierarchy's tier 1–2 (official tour/tournament records) directly. It can reach tier 3–4 (specialist databases with documented methods), and only via GitHub-hosted repositories. Any future study must therefore **declare a tier-3/4 source basis and state plainly that official-record cross-checking was not performed**, rather than implying official verification. This is a real constraint on the charter's cross-check requirement, not a detail.

### 1.4 Licence and provenance caveat on the reconnaissance sources [RUN]

The Sackmann archive mirror is labelled **CC BY-NC-SA 4.0** (non-commercial, share-alike), per its repository description. `SOURCE_STANDARDS.md` requires respecting terms and redistribution limits. **I did not open the full licence text** [NOT CHECKED]. Practical implication recorded now rather than discovered later: a research dataset built from these files cannot be redistributed freely, so the archive should hold a **source manifest plus derived aggregates**, not re-hosted raw files. The mirror is also a *third-party copy* of upstream data, so its `sha256` values identify the mirror's blobs, not upstream's — provenance must name the mirror and the upstream project both.

---

## 2. Repository structure

```
README.md                                  ← 24-byte placeholder
Set-Structure-Research-v1/
└── Set-Structure-Research/
    ├── README.md              framework map, scope, reading order
    ├── RESEARCH_CHARTER.md    mission, 8 research questions, scope, 10 filters, principles
    ├── PROTOCOL.md            10-step study lifecycle (register → archive)
    ├── FILTER_CATALOG.md      the 10 filters + optional secondary filters + status vocabulary
    ├── DATA_DICTIONARY.md     match / set / player-set / provenance fields, derived metrics
    ├── DATA_SCHEMA.json       JSON Schema 2020-12 record definition
    ├── SOURCE_STANDARDS.md    source hierarchy, cross-check, citation, licensing
    ├── DATA_COLLECTION_SOP.md 10-step collection procedure
    ├── STATISTICAL_METHODS.md denominators, Wilson CIs, dependence, confounding
    ├── ANALYSIS_PLAYBOOK.md   standard tables A–G and a common-errors list
    ├── REPORT_TEMPLATE.md     11-section mandated report structure
    ├── QUALITY_CONTROL.md     6 audit gates incl. AI audit and release gate
    ├── AGENTS.md              agent mission, 6 hard prohibitions, 13-step procedure
    ├── CHANGELOG.md           v1.0.0
    ├── templates/             STUDY_SPECIFICATION.md, RESEARCH_LOG.csv, CORRECTION_LOG.csv
    └── tools/                 validate_records.py + unit tests
```

**Structural observations [RUN]:**

- This is a **specification-only repository.** There is no data, no study, no report, no analysis code. `RESEARCH_LOG.csv` and `CORRECTION_LOG.csv` are header-only, so **no study has yet been registered** under this framework.
- The framework is well specified for *governing* research but contains **no mechanism to execute it** — no ingestion code, no parser, no analysis module, no dataset. Every study starts from zero tooling.
- The nested `-v1/Set-Structure-Research/` path suggests an uploaded archive rather than a designed layout; it makes every path longer and will need to be honoured consistently in documentation.

---

## 3. Research principles understood

I take these as binding constraints on any work I do here, not as background reading:

1. **Retrospective only.** Completed matches. No forecast of an upcoming match, no exact-set prediction, ever — not even as a "demonstration".
2. **No market data of any kind.** No odds, bookmaker prices, exchange prices, implied probabilities, market consensus, tipster content. Not as a feature, label, baseline, or validation signal. This extends to *not scraping pages that mix odds with statistics*.
3. **No prospective conversion.** A historical frequency in a sample is never restated as a probability for a future match.
4. **Accuracy before coverage.** A small verified sample beats a large contaminated one.
5. **Provenance per value.** Every material number traceable to source name, direct URL/ID, retrieval date, and match ID.
6. **Fixed definitions before results.** Population, window, filters, denominators declared in advance; changes recorded as dated amendments.
7. **Observational language.** "Historical frequency in this sample", "observed association" — never "cause", "proves", "will", "guarantees".
8. **Missingness is not zero.** `null` means not recorded/unavailable. Never impute scores or set-level stats in primary analysis.
9. **Separate the incomparable.** Best-of-3 vs best-of-5; singles vs doubles; ATP vs WTA vs Challenger vs ITF; main draw vs qualifying; conventional sets vs match tiebreaks.
10. **No invented anything.** No fabricated statistics, sample sizes, URLs, sources, or tool-use claims. "Verified" is reserved for records I actually checked.
11. **Agreement between agents is not replication** when the agents share sources.
12. **Inconclusive is a valid result.**

The framework's own vocabulary is strict in a useful way: every filter must be reported as **Analysed / Unavailable / Not applicable / Excluded with reason** — silence is not an option.

---

## 4. The ten filters, their purpose, and required data

The charters' ten filters are a *decomposition of match structure into nested levels*: match → set → player-set. My reading of each filter's real evidential demand:

| # | Filter | Purpose | Minimum fields | Enables | Blocks |
|---|---|---|---|---|---|
| 1 | Historical match-structure distribution | How many conventional sets did matches actually last? | match_id, status, format, set count, match-tiebreak flag | Baseline denominator for every other filter | Nothing — works from score strings |
| 2 | First-set outcome context | Does who won set 1 relate to final winner and match length? | set-1 score/winner, final winner, set count, status | 2×2 contingency of set-1 winner vs match winner | Retirement handling must be explicit |
| 3 | After winning set one | Descriptive follow-through for the set-1 winner | as #2, indexed by set-1 winner | Subsequent set scores, completion structure | Player-duplication risk (each match yields 2 rows) |
| 4 | After losing set one | "Comeback" definition: lose set 1, win match | as #2, indexed by set-1 loser | Comeback counts with exact denominators | Must not become a "clutch trait" claim |
| 5 | Set competitiveness | Were sets close, and does closeness vary by set position? | per-set games, total games, absolute differential, TB flag | Scoreline taxonomy, margin distributions | Margin ≠ quality — no quality inference |
| 6 | Tiebreak structure | How often, where, and with what scores? | TB marker per set, TB points, set position | Set-level TB rate; match-level any-TB rate | **Match tiebreaks must be excluded** from conventional counts |
| 7 | Serve performance by set | Does serving change across sets? | per-set serve counts (points, 1st in/won, 2nd won, aces, DF, service games, BP faced/saved) | Within-match set-to-set comparison | **Match-total stats cannot be used.** Needs set-level or point-level data |
| 8 | Return performance by set | Does returning change across sets? | per-set return points/games won, BP earned/converted | Return-side counterpart to #7 | Same — no distribution of match totals |
| 9 | Deciding-set structure | What do final sets look like? | deciding-set score, games, margin, TB, stats if present | Conditional on reaching a decider only | Denominator is *matches reaching a decider*, not all matches |
| 10 | Surface & competition context | Do patterns differ by clay/hard/grass, tour, level, format, round, era? | surface, indoor/outdoor, tour, level, discipline, format, round, date | Every other filter stratified | Small cells; confounding; coverage differs by era |

**Cross-cutting requirement the catalog states plainly and that is easy to violate:** filters 1–6 and 9 are *set-level descriptive* and are computable from score strings alone; **filters 7–8 are the only ones needing a fundamentally different data source.** No amount of score-string data can produce them. That single fact drives the entire feasibility picture in §8.

---

## 5. Data requirements: dictionary vs schema

### 5.1 The schema cannot represent the dictionary [RUN]

`DATA_SCHEMA.json` declares `"additionalProperties": false`. Measured gap — **10 dictionary match-level fields have no schema slot:**

`source_match_id`, `event_name`, `event_id`, `match_datetime`, `tour`, `event_level`, `draw_type`, `round`, `total_sets_played`, `match_tiebreak_used`.

The two most serious:

- **`tour` and `event_level` are absent.** Filter 10 explicitly requires tour and level stratification, and the charter mandates separating ATP/WTA/Challenger/ITF. A schema-compliant record literally cannot state its tour or level.
- **`round` and `draw_type` are absent**, so round- and main-draw-vs-qualifying stratification cannot be encoded.
- `total_sets_played` and `match_tiebreak_used` are derived fields the dictionary lists but the schema does not store — meaning any consumer must re-derive them, with the risk of re-deriving them differently.

### 5.2 The schema cannot represent doubles [RUN]

`players` has `minItems: 2, maxItems: 2`. A doubles match has four players. The dictionary says doubles results use `winner1/winner2/loser1/loser2`, and the charter requires doubles be *separated*, not ignored. As written, **a doubles record cannot validate**.

### 5.3 What the schema does well

Set-level fields (`set_index`, `games[2]`, `set_winner_id`, `tiebreak_played`, `tiebreak_score[2]`, `is_match_tiebreak`, `duration_minutes`, `status`) correctly keep match tiebreaks distinguishable from conventional sets — the single most important modelling trap, and the schema gets it right. `player_set_stats` correctly stores integer counts (not percentages) with nullable fields, honouring "zero is not missing". Provenance is enforced: `sources` is required, non-empty, with `verification_status` enum (`unverified`/`single_source`/`cross_checked`/`corrected`).

### 5.4 Dependence and the row model

The dictionary prescribes `matches.csv` (one row per match), `sets.csv` (one per set), `player_set_stats.csv` (one per player per set). This is the right normalised shape, but note that **`player_set_stats` yields two rows per set per match**, i.e. roughly 2 × sets × matches rows. `STATISTICAL_METHODS.md` warns that two players' records from one match are not independent. Any Filter 7/8 analysis must therefore aggregate to a **player-match or set-within-match** unit and cluster by match; naively taking `n = rows` would inflate the sample by ~2× and understate uncertainty.

---

## 6. Source requirements

Hierarchy (tiers 1→5), with the practical mapping I measured:

| Tier | Standard | Reachable here? |
|---|---|---|
| 1 | Official tour/federation/tournament records | **No** — atptour.com, wtatennis.com blocked [RUN] |
| 2 | Official result books, match-stat PDFs, scoring systems | **No** [RUN] |
| 3 | Reputable specialist databases, transparent match records | **Yes**, via GitHub mirrors [RUN] |
| 4 | Established statistical projects with documented methods | **Yes** [RUN] |
| 5 | Reputable media for context only | Not tested; and not sufficient for core scores |

Requirements per record: stable ID, direct URL/ID, retrieval timestamp, fields captured, verification status. Cross-check triggers are explicit: unusual scores, retirements/defaults/walkovers, match-tiebreak formats, name/date inconsistencies, and **set-level stats that do not reconcile with match totals**. That last clause is the one that turns out to be the key to Filters 7–8 (§8.3).

Non-negotiable: search snippets are leads, not evidence; a tournament homepage is not a match record; **two sources repeating the same underlying feed are not independent confirmation** — relevant because the two datasets I tested both trace to the same upstream author.

---

## 7. Statistical requirements

- **Every rate carries numerator and denominator.** Set-level rates → denominator is sets. Match-level rates → denominator is matches. Never mix.
- **Denominators exclude unobserved records**; `0%` is forbidden when the denominator is 0.
- **Uncertainty:** Wilson intervals preferred over normal approximation for small n / extreme proportions; state method and level. Intervals do **not** fix selection bias.
- **Dependence:** sets within a match are not independent; neither are two players from one match. Use match-clustered methods or match-level aggregation. Do not inflate n.
- **Zero vs missing** must be distinguished; missing values are never replaced with zero, and are never imputed in primary descriptive analysis.
- **Multiple comparisons:** ten filters × subgroups is a large search space. Predefine primary outcomes, label exploratory findings, seek replication.
- **No causal language, no psychological traits from small samples.**
- **Historical rankings** only with a date-matched snapshot; current rankings are not historical rankings (the archive does provide date-stamped rankings and per-match `winner_rank`, which would satisfy this if used carefully).

---

## 8. Feasibility of the ten filters against reachable data [RUN]

This is the section that changes the research plan. I did not assume; I fetched and measured.

### 8.1 What the sources actually contain

**Dataset A — ATP/WTA season match files** (mirror of the standard Sackmann match CSVs):
- **59 ATP tour-level singles season files, 1968–2026**; 59 WTA singles season files; plus ATP `doubles` (2000–2020, 21 files), `futures` (1991–2026, 36 files), `qual_chall` (1978–2026, 49 files), 1 amateur file, player and ranking files — 166 `atp_matches_*.csv` files in total.
- Columns include `score`, `best_of`, `surface`, `round`, `minutes`, per-player `w_/l_` serve counts, and date-matched `winner_rank`/`loser_rank`.
- **WTA caveat:** 0 WTA qualifying/Challenger and 0 WTA doubles files are present [RUN]. Women's coverage is tour-level singles only, and *tour-level* here means whatever upstream covered — not a guarantee of completeness.

**Dataset B — Grand Slam point-by-point** (mirror of slam point files):
- 49 point files, **2011–2024**, four slams; 271 MB total.
- Carries **both tours**: 2024 Wimbledon has 252 match rows, 125 men + 127 women; verified by finding both ATP and WTA players [RUN].
- Also carries doubles/mixed point files (36 doubles, 32 mixed).
- Per-point fields include `SetNo`, `GameNo`, `PointWinner`, `PointServer`, `ServeNumber`, `P1/P2` aces, double faults, break-point flags, rally count.

**Dataset C — MatchChartingProject charted matches:**
- 7,566 charted matches, 1960–2026, with point-level files for a subset. Men and women.

### 8.2 Measured completeness (ATP season files) [RUN]

| Year | n rows | score | best_of | surface | minutes | `w_svpt` | RET/WO/DEF | Bo5 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1991 | 3,727 | 100.0% | 100.0% | 100.0% | 86.9% | 86.8% | 69 | 756 |
| 2000 | 3,378 | 100.0% | 100.0% | 100.0% | 87.1% | 87.1% | 101 | 756 |
| 2010 | 3,030 | 100.0% | 100.0% | 100.0% | 88.6% | 88.6% | 121 | 738 |
| 2020 | 1,462 | 100.0% | 100.0% | 100.0% | 97.2% | 96.8% | 32 | 381 |
| 2023 | 2,986 | 100.0% | 100.0% | 98.2% | 92.2% | 94.3% | 97 | 523 |
| 2024 | 3,076 | 100.0% | 100.0% | 100.0% | 92.3% | 98.0% | 103 | 523 |

Score, format and surface are essentially complete; **`minutes` and match-level serve stats run 87–98%**, so the ~2–13% missing-tail must be reported per field, not glossed. Score-string parseability across 16,197 rows: 0.03–0.33% unparseable per year, and every failure I inspected was a genuine status/format case rather than a parser defect.

**Status and format tokens found in `score` [RUN]** over 16,197 rows: `RET` 399, `W/O` 84, `DEF` 8, `Def.` 1, "Played and unfinished" 2, "Played and abandoned" 1.

**The match-tiebreak trap is real and located [RUN].** Bracket notation (`[10-4]`, `[11-9]`) appears in 16 rows, all 2023–2024, and every one is **Davis Cup or Laver Cup** — team events with best-of-3 plus a match tiebreak in lieu of a third set. Examples: `6-4 6-7(4) [10-4]`; `6-3 6-7(6) [10-4]`; `6-2 4-6 [11-9]`. A parser that treats `[10-4]` as a 10–4 set would manufacture impossible 16-game sets and corrupt Filter 1 (set-count distribution) and Filter 5 (competitiveness). These must be flagged `is_match_tiebreak` and excluded from conventional-set counts.

### 8.3 The decisive test: can set-level serve/return stats be derived *and* verified?

Filters 7–8 need set-level serve/return data. Dataset A has only **match totals**. So the only sound route is to derive set-level values from point data — which the charter permits only if match totals are not distributed across sets. I tested whether point-derived aggregates **reconcile with independent match totals**, which is both the feasibility test and the reconciliation check that `SOURCE_STANDARDS.md` demands.

**Method:** for `2024-wimbledon-points.csv`, drop placeholder rows (511 rows with `PointWinner`=0/`PointServer`=0), then per server accumulate service points, first serves in (`ServeNumber`=1), first/second-serve points won, aces, double faults. Join to `2024-wimbledon-matches.csv` by player names, map to `atp_matches_2024.csv`, and compare against `w_/l_1stIn`, `svpt`, `ace`, `df`, `1stWon`, `2ndWon`.

**Result [RUN]: 113 of 117 joinable ATP matches reconciled exactly on all six fields (96.6%).**

Four mismatches, listed in full because they are source disagreements and the framework requires disclosure:

| Match | Round | Fields differing | Difference |
|---|---|---|---|
| Ruusuvuori–Tsitsipas | R64 | w_svpt, l_1stIn, l_svpt, l_1stWon | ±1 point each |
| Fritz–Rinderknech | R64 | w_1stIn | −1 |
| Rune–Seyboth Wild | R64 | w_svpt, w_2ndWon, l_1stIn, l_svpt | ±1 |
| Halys–Khachanov | R64 | w_1stIn, w_1stWon | ±1 |

All four are **single-point discrepancies, all in one round** — consistent with a boundary point being attributed to the wrong game/serve in one pipeline, but that is a hypothesis, not a finding, and I am not asserting it. What is established: the derivation works, it is checkable, and residual disagreement is small, bounded, and recordable in `CORRECTION_LOG.csv`.

**Two further data-quality facts [RUN], both material:**
- `P1FirstSrvIn`/`P1FirstSrvWon`/`P1SecondSrvIn`/`P1SecondSrvWon` are **empty in all 48,155 rows** — these convenience columns are unusable, and serve outcomes must be reconstructed from `ServeNumber` + `PointWinner`. Anyone trusting the column names would silently produce empty Filters 7–8.
- The `P1Ace`-style columns are **server-indexed, not player-indexed**: aces are recorded in the serving player's column. I verified this (P2 aces on P2 serve: 1,825; P1 "ace" recorded while P2 served: 0). Treating them as player-indexed would swap serve stats between players.

### 8.4 Feature × filter support matrix

| Filter | Dataset A (season files) | Dataset B (slam points) | Dataset C (charted) |
|---|---|---|---|
| 1 Set-count distribution | ✅ 1968–2026, all tours/levels | ✅ 2011–2024, slams | ✅ subset, 1960–2026 |
| 2 First-set context | ✅ | ✅ | ✅ |
| 3 After winning set 1 | ✅ | ✅ | ✅ |
| 4 After losing set 1 | ✅ | ✅ | ✅ |
| 5 Set competitiveness | ✅ | ✅ | ✅ |
| 6 Tiebreak structure | ✅ TB marker; TB *score* parseable from string | ✅ exact | ✅ exact |
| 7 Serve by set | ❌ match totals only | ✅ **derivable + verifiable** | ✅ but small, self-selected |
| 8 Return by set | ❌ | ✅ derivable (opponent of #7) | ✅ small |
| 9 Deciding set | ✅ | ✅ | ✅ |
| 10 Surface/competition | ✅ surface, level, round, best_of, rank | ⚠️ slams only; surface constant | ⚠️ opportunistic |

**Read the matrix as a constraint, not a to-do list.** Filters 1–6, 9, 10 are broadly feasible and become the backbone. Filters 7–8 are feasible **only** in the 2011–2024 Grand Slam point window, and therefore **cannot be studied on clay/hard/grass-independent tour-level samples or on Challenger/ITF data at all**. Any report must say that set-level serve/return conclusions are *Slam-only, 2011–2024* — a much narrower population than the structural filters.

### 8.5 Defects found in Dataset C (charted matches) [RUN]

`charting-m-matches.csv` has 7,566 rows but contains shifted columns in a Davis Cup cluster: one row's `Surface` holds an umpire name ("Eva Asderaki-Moore") with `Best of`="1", and a second row has `Surface`="3", `Best of`="Zindaras" and `Date`="RR" (a round code in the date column). **2 of 7,566 distinct rows are malformed (~0.03%)**. Small, but it proves the file needs a validator pass before use — and it is exactly the "unusual record" class the SOP says to flag rather than drop silently. Both rows are unusable for surface or format stratification.

### 8.6 Validator behaviour [RUN]

I executed `tools/validate_records.py` (stdlib-only, runs under Python 3.11) and its three unit tests pass. Tested against crafted edge cases:

| Case | Behaviour | Verdict |
|---|---|---|
| Empty `surface` (missing) | Rejected: "invalid surface" | **Conflicts with "missing ≠ zero"** — a legitimately unknown surface is unrepresentable |
| `Best of 5 sets with match tiebreak` as format | **Accepted** (free text) | Format is unconstrained, so incompatible scoring formats can pass |
| Any walkover row | Rejected outright | Overshoots: SOP says *separate* walkovers, not forbid the file |
| Impossible date `2025-02-30` | Rejected | Correct |
| Duplicate `match_id` | Rejected | Correct |

The validator checks **structure only** and says so in its own output — "source accuracy is not verified". No score-string, set-count, tiebreak, or reconciliation checks exist. So nothing in the repository currently prevents the match-tiebreak trap in §8.2 or the ace-index trap in §8.3.

---

## 9. Potential methodological weaknesses

Ranked by how much damage each would do if unaddressed.

1. **Source-provenance circularity (highest risk).** The two usable datasets trace to the same upstream project. Cross-checking one against the other is *not* independent verification, and the charter names this trap explicitly. My 96.6% reconciliation result is genuinely useful — it validates the *derivation method* — but it does **not** independently confirm the underlying numbers. Every report must state that no tier-1 official source was consulted.
2. **Set-level data window is narrow and Slam-only.** Filters 7–8 exist only for 2011–2024 majors. Generalising any serve-by-set finding beyond that is unsupported.
3. **Within-match dependence is easy to violate silently.** `player_set_stats` is ~2 rows per set per match; pooling rows as independent inflates n and shrinks intervals. Match-clustered or match-aggregated analysis should be the default, declared in the study spec.
4. **Match-tiebreak contamination.** 16 rows in 2023–2024 team events. Silent inclusion corrupts set-count and competitiveness distributions.
5. **"Open era" is not homogeneous.** Best-of-5 finals in best-of-3 events, tiebreak-scoring changes, Davis Cup format changes, and the 2020 season's disruption (1,462 matches vs ~3,000 typical) all break naive era pooling.
6. **Retirement handling.** RET rows retain partial scores; they must be excluded from structure distributions with a labelled sensitivity analysis, never silently.
7. **Missing minutes / serve stats (2–13% tail)** could cluster by tour, year or level; completeness must be reported by stratum, not pooled.
8. **Ten filters × many strata = large multiple-comparison surface.** Without predecomposition and exploratory labelling, chance findings will look like discoveries.
9. **Small subgroups** (carpet, indoor, ITF, round-of-16-in-qualifying-style cells) invite over-reading.
10. **Coverage asymmetry between tours.** Women's data lacks qualifying/Challenger/doubles; cross-tour comparisons would confound tour with coverage.
11. **Licence non-commercial/share-alike** constrains redistribution of derived datasets.
12. **Date semantics.** `tourney_date` is usually the Monday of the tournament week, not the match date — this affects any "season", "rest days" or "period" analysis and must not be treated as match date.

---

## 10. Missing components and concrete improvements

Proposed in dependency order. None of this is applied yet — this audit's job is to identify, not to change the framework.

**Blocking (a study cannot be executed soundly without these)**

1. **A study-execution layer.** Nothing exists between the specification and a report. Required: an ingest script, a score-string parser (incl. `[10-4]` match-tiebreak detection, RET/W/O/DEF/`Def.`/"Played and unfinished" handling), a set-table builder, an analysis module with Wilson CIs, and a report generator.
2. **Schema alignment.** Add `tour`, `event_level`, `round`, `draw_type`, `source_match_id`, `match_datetime`, `total_sets_played`, `match_tiebreak_used` to `DATA_SCHEMA.json` — or an explicit `framework` block — otherwise Filter 10 is unencodable.
3. **Doubles representation.** Allow 2 *or* 4 players (team objects), so the mandated doubles separation is possible.
4. **A set-level serve/return ingestion spec.** Document the point→set derivation rule (placeholder filtering, `ServeNumber` semantics, server-indexed columns) and the reconciliation check against match totals, with a stated tolerance rule for ±1-point disagreements. This is the only defensible path to Filters 7–8 and it is currently undocumented.
5. **Validator upgrade.** Widen `surface` to accept `unknown` explicitly; add format-domain checks (reject mixed match-tiebreak/conventional formats under one label); allow walkovers in-file with a *warning* rather than a hard error; verify set counts against `best_of`; detect bracket match-tiebreaks; check `sum(set games)` consistency.

**High value**

6. **A machine-readable source manifest** (`sources.csv` with URL, blob hash, retrieval timestamp, upstream attribution, licence) — the artefact type this audit produced manually should be generated automatically.
7. **Reconciliation report** as a standing artefact: N matches joined, N reconciled exactly, list of disagreements with the differing fields, feeding `CORRECTION_LOG.csv`.
8. **A missingness report** generated per stratum (tour × year × level × surface) rather than per file.
9. **A frozen-analysis-plan template** that predeclares primary vs exploratory outcomes to blunt §9.8.
10. **A dependence policy** written down: the unit of analysis for each filter, and the clustering approach.

**Housekeeping**

11. Root `README.md` is a 24-byte placeholder while the real map is nested — a reader following the prompt's instruction 1 hits a dead end first. Add a pointer file.
12. **No `LICENSE`**, no `.gitignore`, no CI. Given the data-licence constraints in §1.4, a licence decision and an ignore policy for large CSVs are needed before any dataset is committed.
13. **No `data/`, `studies/`, `reports/` directories** despite the protocol's archive requirements. Create the expected layout (or document where artifacts go).
14. `templates/CORRECTION_LOG.csv` and `RESEARCH_LOG.csv` are header-only, confirming no prior study — worth stating in the changelog so future agents do not look for a precedent.

---

## 11. Filter-readiness summary

| Filter | Status at audit | Basis |
|---|---|---|
| 1 Historical structure | **Ready to plan** | Score strings parse at ≥99.7% |
| 2 First-set context | **Ready to plan** | Set-1 winner derivable from score |
| 3 After winning set 1 | **Ready to plan** | Same, with dependence handling |
| 4 After losing set 1 | **Ready to plan** | Comeback definition must be predeclared |
| 5 Set competitiveness | **Ready to plan** | Games/differentials from scores |
| 6 Tiebreak structure | **Ready to plan** | TB marker in scores; match tiebreaks must be excluded |
| 7 Serve by set | **Feasible but narrow** | Only 2011–2024 Slams via point derivation; reconciled 113/117 |
| 8 Return by set | **Feasible but narrow** | Same window; opponent-side of #7 |
| 9 Deciding set | **Ready to plan** | Denominator = matches reaching a decider |
| 10 Surface/competition | **Partly blocked** | Surface/format/round available; **schema cannot encode tour/level** |

No filter is *Analysed* — this audit performs no analysis, by design.

---

## 12. What I did not do

To keep the record clean:

- **No match structure was analysed.** No set-count distribution, no first-set table, no trend, no finding appears in this document.
- **No predictions, no probabilities, no market data**, and none was sought. I did encounter one GitHub repository during a broad repo search whose name and description referenced betting; I did not open it, clone it, or use anything from it, and I note it here only so the provenance trail is complete.
- **I did not verify any record against official ATP/WTA sources** — those hosts are blocked here (§1.3). All external values above are from GitHub-hosted mirrors and are described as such.
- **I did not read the full CC BY-NC-SA licence text** [NOT CHECKED].
- The 96.6% reconciliation covers **117 of 252** 2024 Wimbledon matches (those joining by name to the ATP season file); the remaining 135 (mostly women's) were not reconciled against an independent match-total source in this audit.

---

## 13. Neutral conclusion

The framework is coherent, unusually disciplined about denominators, dependence, and missingness, and it clearly anticipates the traps that the data actually contains — match tiebreaks, mixed formats, retirement handling, within-match dependence. Its specifications are *not* aspirational: the traps it warns about are present in real files I fetched.

The binding constraint is not the framework but the **evidence base available to this environment**. Filters 1–6, 9 and 10 are well supported by score-string data across 1968–2026. **Filters 7–8 — service and return by set — are supportable only for 2011–2024 Grand Slam matches via point-level derivation**, and only with an explicitly documented derivation rule; they cannot be answered for Challenger/ITF data or for a general tour-level sample in this environment. That asymmetry, not any tennis finding, is the most important thing to know before a study is registered.

Before registering Study 001, the repository needs: (a) a study-execution layer, (b) schema alignment so tour/level/round are representable, (c) doubles representation, and (d) the point→set derivation and reconciliation rule written down. Until then, a report could be *written* under this framework but not *reproduced* from it.

---

## 14. Reproducibility

- **Repository commit audited:** `83c59b9a56e36a8b0796c402a72af0ced534dd28` (branch `arena/7acbc817-set-structure-research`).
- **Framework version:** 1.0.0.
- **Environment:** Python 3.11.2, standard library only (`csv`, `json`, `re`, `hashlib`, `collections`). `pandas`, `numpy`, `jsonschema`, `pytest` are **not installed**; tests were run with `python3 -m unittest` and pass (3/3).
- **Source access log:** `audits/artifacts/source_access_log.csv` — 11 requests, timestamps 2026-11-15T07:47:50Z–07:47:54Z, HTTP status, byte counts, SHA-256 per retrieved file, and full URLs.
- **Re-running:** all external files were fetched with the `Accept: application/vnd.github.raw` header against `api.github.com/repos/{owner}/{repo}/contents/{path}`. Blob hashes in the log identify the exact bytes audited; re-fetching the same path later may return different bytes if upstream changes, which is why hashes are recorded.
- **Not reproduced here:** the individual probe scripts used for completeness, parseability, reconciliation and malformed-row detection were run interactively and are described by method above; they are not yet committed as reusable tools (see §10.1).
