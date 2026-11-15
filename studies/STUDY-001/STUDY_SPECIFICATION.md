# Study Specification — STUDY-001

**Status:** REGISTERED before any outcome was computed.
**Registered:** 2026-11-15T08:05Z
**Protocol version:** 1.0.0 (repository framework)
**Repository commit at registration:** see `git log` for this file
**Analyst/agent:** Arena.ai research agent

> **Declaration of ordering.** This specification was written after inspecting only the *sample frame* (column names, `tourney_level` counts, round labels, surfaces, `best_of` values, draw sizes) and **before** computing any outcome measure. Per `PROTOCOL.md` §1, no primary definition below was chosen after viewing results. Any later change must be added here as a dated amendment.

---

## 1. Research question

**Primary:** Among completed ATP Challenger men's singles matches (best-of-3, conventional scoring) played in the window 2024-01-01 to 2026-06-01, what is the historical distribution of match structure — how many conventional sets matches lasted — and how does that distribution differ by surface, round, and season?

**Secondary (descriptive, registered):**
- S1: Frequency of matches containing at least one conventional tiebreak.
- S2: Distribution of first-set game margins; frequency of first-set tiebreaks.
- S3: Relationship between first-set winner and eventual match winner (contingency, indexed explicitly by player identity).
- S4: Structure of deciding sets (score distribution, game margin, tiebreak frequency) among matches that reached a third set.

**Explicitly NOT research questions (out of scope):**
- Any forecast of an upcoming or unplayed match.
- Any probability statement about a future match's set count.
- Any prediction of a winner.
- Any use of, or reference to, sportsbook odds, prices, or market-implied probabilities.

## 2. Target population

Completed, played ATP Challenger tour-level singles matches of the men's professional tour, best-of-three sets, conventional scoring, played 2024-01-01 through 2026-06-01 inclusive.

This is a **sample definition, not a universal population.** It describes Challenger tennis in this window only and must not be generalised to ATP Tour, Grand Slam, WTA, ITF, or doubles competition.

## 3. Source and freeze

| Item | Value |
|---|---|
| Source project | `Aneeshers/tennis-sackmann-archive` (GitHub mirror of the Sackmann tennis datasets) |
| Upstream authorship | Jeff Sackmann's tennis data collections |
| Files used | `atp/atp_matches_qual_chall_2024.csv`, `atp/atp_matches_qual_chall_2025.csv`, `atp/atp_matches_qual_chall_2026.csv` |
| Retrieval method | `api.github.com` contents API, `Accept: application/vnd.github.raw` |
| Retrieval date | 2026-11-15 |
| Source tier | Tier 3–4 (specialist database, documented fields). **Not** tier 1–2 official tour records |
| Blob hashes | Recorded in `studies/STUDY-001/outputs/source_manifest.csv` |
| Licence | CC BY-NC-SA 4.0 per repository description. Raw rows are **not** redistributed; only derived aggregates are committed |

**Known and declared source limitation:** the archive's coverage in the retrieved files ends **2026-06-01**. Matches played between 2026-06-02 and the analysis date (2026-11-15) are **absent**. The study window is therefore capped at 2026-06-01, not 2026-11-15, and no claim is made about that later period.

## 4. Inclusion criteria

A record is included if **all** hold:
1. `tourney_level` = `C` (Challenger; per the source data dictionary).
2. `best_of` = `3`.
3. `score` is present and non-empty.
4. `surface` ∈ {`Hard`, `Clay`, `Grass`}.
5. `tourney_date` within 2024-01-01 … 2026-06-01.
6. The score string **fully reconciles** with best-of-3 conventional scoring after parsing (see §6).

## 5. Exclusion criteria, and how each is counted

| # | Rule | Handling |
|---|---|---|
| E1 | `score` contains `RET` (retirement) | Excluded from primary structure distribution. Counted and reported. **Separate labelled sensitivity analysis** with retirements included. |
| E2 | `score` contains `W/O` (walkover) | Excluded — no played match structure exists. Counted and reported. Never enters any denominator. |
| E3 | `score` contains `DEF` / `Def.` (default) | Excluded. Counted and reported. |
| E4 | `score` contains "Played and unfinished", "Played and abandoned", `ABD` | Excluded as abandoned. Counted. |
| E5 | Match-tiebreak notation present (`[10-4]` style bracket set) | Excluded from the conventional-set structure primary analysis; counted and reported. Rationale: a match tiebreak is not a conventional set, and a "2-set match" ending in a match tiebreak is structurally different. |
| E6 | Score unparseable under the grammar in §6 | Excluded as unclassified; **listed individually in the data-quality output**, not silently dropped. |

No record is discarded silently. Every exclusion is counted in the sample-construction table and, where feasible, itemised.

## 6. Score-string grammar (frozen)

Score strings are **winner-perspective**. Grammar:

```
set_token   := games "-" games [ "(" tb_loser_points ")" ]
bracket_tok := "[" games "-" games "]"          # match tiebreak
score       := ( set_token | bracket_tok )+  status_suffix?
```

Parsing rules fixed now:
- Set winner = the player with more games in that token.
- `(n)` records the **loser's** tiebreak points; a conventional set tiebreak occurred iff the parenthetical is present and the set reached 6-6 (7-6 or 7-5 after a TB is impossible; 7-6x always implies a TB).
- A **conventional set** must satisfy: winner games ∈ {6,7}, and if winner = 6 then loser ≤ 4; if winner = 7 then loser ∈ {5,6}.
- A set is a **tiebreak set** iff the score is 7-6 or 6-7.
- Any token violating those bounds → record flagged `parse_ok = false` and excluded (E6), with the reason logged.
- Best-of-3 requires 2 or 3 conventional sets for a completed match; anything else → E6.
- Retirements legitimately produce partial sets (e.g. `6-3 2-4 RET`); RET rows are parsed only to extract completed-set counts for the sensitivity analysis and are **never** used in primary denominators.

## 7. Denominators (frozen)

| Measure | Numerator | Denominator |
|---|---|---|
| Straight-set share | eligible matches with exactly 2 conventional sets | eligible completed matches |
| Three-set share | eligible matches with exactly 3 conventional sets | eligible completed matches |
| Match-with-tiebreak share | eligible matches with ≥1 conventional tiebreak | eligible completed matches |
| Tiebreak-set share | conventional tiebreak sets | all conventional sets in eligible matches |
| First-set TB share | matches whose set 1 was a tiebreak | eligible completed matches |
| First-set-winner-wins-match | eligible matches where set-1 winner also won the match | eligible completed matches |
| Deciding-set TB share | 3-set matches whose set 3 was a tiebreak | eligible matches reaching 3 sets |

A rate is reported **only** when its denominator is > 0. `0%` is never reported for an empty denominator.

## 8. Planned analyses

1. Sample construction waterfall (candidates → exclusions by rule → eligible).
2. Completeness/missingness table by field and by year.
3. **Filter 1** — set-count distribution, overall and stratified by surface, round, season.
4. **Filter 2** — first-set outcome context: contingency of set-1 winner × match winner, with the indexing rule stated; plus set-1 margin distribution.
5. **Filter 5** — set competitiveness: total games and absolute game differential by set position.
6. **Filter 6** — tiebreak structure: set-level and match-level rates by set position and surface.
7. **Filter 9** — deciding-set structure: score distribution, margin, TB frequency.
8. **Filter 10** — surface/round/season stratification of the above, with group sizes shown.
9. **Filters 3, 4, 7, 8** — status stated explicitly (see §9).
10. Sensitivity checks (§10).

## 9. Pre-declared filter statuses

Per `RESEARCH_CHARTER.md`, every filter must carry a status even when not analysed.

| Filter | Expected status | Reason |
|---|---|---|
| 1 Historical structure | **Analysed** | Score data supports it |
| 2 First-set context | **Analysed** | Derivable from scores |
| 3 After winning set 1 | **Analysed (descriptive)** | Same data; dependence handled at match level |
| 4 After losing set 1 | **Analysed (descriptive)** | "Comeback" = lost set 1, won match |
| 5 Set competitiveness | **Analysed** | Games/differentials from scores |
| 6 Tiebreak structure | **Analysed** | TB marker in score |
| 7 Serve by set | **Unavailable** | Source provides match-total serve counts only; set-level serve data does not exist for this population. Distributing totals across sets is prohibited. |
| 8 Return by set | **Unavailable** | Same reason as Filter 7 |
| 9 Deciding-set structure | **Analysed** | Conditional on reaching set 3 |
| 10 Surface/competition context | **Analysed, with limits** | Surface/round/season available; indoor-outdoor not recorded; draw type partly inferable from round labels |

**Filters 7 and 8 cannot be analysed in this study.** This is the single most important scope limitation and is stated in the report, not buried.

## 10. Pre-declared sensitivity checks

1. Retirements included vs excluded (structure distribution only).
2. Main draw only (excluding `Q1`/`Q2` rounds) vs all rounds.
3. By season (2024 / 2025 / 2026 partial).
4. By surface (Hard / Clay / Grass).
5. Excluding 2026 (a partial season, ending 2026-06-01) to test whether the partial year distorts pooled figures.

## 11. Statistical methods

- Counts, numerators and denominators everywhere; shares as derived displays only.
- **Wilson score confidence intervals** (95%) for all proportions. Formula stated in output.
- **Match-level aggregation** for match-level rates; set-level rates report set denominators **and** the number of contributing matches.
- **Dependence:** sets within a match are not independent. No test is applied that assumes independent sets. Set-position comparisons are reported descriptively; where a chi-square is run, it is flagged as treating sets as independent and therefore approximate/exploratory only.
- **Multiple comparisons:** the ten-filter structure creates many subgroup comparisons. All surface/round/season subgroups are **exploratory**; no subgroup finding is treated as confirmatory.
- No imputation. No regression (sample does not require it for these descriptive questions, and the charter prefers descriptive first).
- Software: Python 3.11.2 standard library only. No external statistics packages — Wilson intervals implemented directly and unit-tested.

## 12. Known limitations (declared in advance)

1. **Tier 3–4 source only**; no official ATP cross-check was possible in this environment (official hosts unreachable).
2. **Single-source.** No independent dataset used; agreement with another source cannot be claimed.
3. **Coverage ends 2026-06-01**; a ~5.5-month gap to the analysis date.
4. **Challenger only**; results do not transfer to ATP Tour, Slams, WTA or ITF.
5. **Best-of-3 only**; no best-of-5 comparison is possible within this population.
6. **No set-level serve/return data** (Filters 7–8 unavailable).
7. **No opponent-quality adjustment**; ranking is available in the source but no adjustment is attempted in this descriptive study.
8. **Missing fields** (minutes, serve totals) will be quantified, and any clustering of missingness reported rather than assumed absent.
9. **Qualifying rounds included in the primary sample**; they are a different population from main-draw matches and are separated in sensitivity check 2.
10. Descriptive only. No causal claim, no psychological trait, no player "clutch" attribute.

## 13. Outputs

| Artefact | Path |
|---|---|
| This specification | `studies/STUDY-001/STUDY_SPECIFICATION.md` |
| Pipeline code | `tools/study001_pipeline.py` |
| Unit tests | `tools/test_study001_pipeline.py` |
| Aggregate outputs (CSV) | `studies/STUDY-001/outputs/*.csv` |
| Source manifest | `studies/STUDY-001/outputs/source_manifest.csv` |
| Data-quality log | `studies/STUDY-001/outputs/data_quality_exclusions.csv` |
| Report | `studies/STUDY-001/REPORT.md` |

Raw source rows are **not** committed (licence + size). Only derived aggregates and the manifest are committed, so the study is reproducible by re-running the pipeline against the same blob hashes.

## 14. Protocol amendments

### A1 — 2026-11-15 — tiebreak-point parenthetical is optional

**Where:** §6, rule "`(n)` records the loser's tiebreak points; a conventional set tiebreak occurred iff the parenthetical is present".

**Problem found during unit testing:** this wording made a bare `7-6` (tiebreak points not recorded by the source) fail grammar validation. But a set cannot finish 7-6 by any route other than a tiebreak, so the parenthetical is redundant for *detection*; it only supplies the tiebreak *score*.

**Amendment:** a set is a conventional tiebreak set iff `max(games)==7 and min(games)==6`, **irrespective of whether tiebreak points are recorded**. `tb_loser_points` remains `null` when unrecorded, consistent with "missing is not zero".

**Effect on results:** none. No outcome had been computed when this was written; the change was driven by a failing unit test, not by data. It slightly *increases* tiebreak detection relative to the original wording, and that direction is disclosed.

**Ordering note:** the amendment was made after outcomes were computed in the sense that A1 was written into this file following a test run, but **before** any tennis result had been examined. No data-driven decision is involved.

### A2 — 2026-11-15 — status resolution must precede parse validation

**Problem found:** the first pipeline run reported **0 retirements** and **947 unparsed** records. Inspection of the exclusion log showed the cause was an ordering defect in the code, not in the data: a retirement such as `6-1 2-1 RET` contains a legitimately incomplete set (`2-1`), which fails conventional-set validation. Because parse validity was tested first, every retirement fell into the E6 "unparsed" bucket and E1 stayed empty.

**Amendment:** match status is now resolved **before** parse validity. A partial set is expected in a retirement and is not an error. Retirements are classified E1; only completed matches that still fail grammar are E6.

**Effect:** E1 0 → 941; E6 947 → 3 (then 2 after A3). Eligible total unchanged at 24,292, because these records were excluded either way. **This defect changed no rate** — it changed only the *labelling* of exclusions, which matters for the sample-construction table and for not hiding retirements.

### A3 — 2026-11-15 — additional retirement spelling `Ret'd`

**Problem found:** after A2, 3 residual E6 records remained, all containing `0-0`. Enumerating every status-like token across all 25,393 level-C scores found exactly one further variant: `Ret'd`, in a single Szczecin CH record (`6-3 0-0 Ret'd`).

**Amendment:** `Ret'd` added to the retirement token list.

**Effect:** E6 3 → 2. The remaining 2 records (`6-1 0-0`, `7-5 0-0`, both Manama CH) carry no status token at all and are genuinely unclassified; they stay in E6 and are itemised in `outputs/data_quality_exclusions.csv`.

### A4 — 2026-11-15 — retirements retain their completed sets

**Problem found:** the retirement sensitivity row initially returned a distribution of 1-set and 2-set "matches", which is meaningless — a 2-vs-3-set distribution cannot contain retirements, which have no final set count by construction. Worse, `n_conventional` was 0 for all 941 retirements because parsing aborted at the first partial set.

**Amendment:** on a retirement, sets completed *before* the interruption are retained and counted. The sensitivity output reports the **progress distribution of retirements** (`{0: 160, 1: 572, 2: 209}`) and states explicitly that its shares are shares of *retirements*, not of matches. Retirements are never folded into the primary structure distribution.

### A5 — 2026-11-15 — conditional-direction disclosure

**Problem found in my own reasoning:** I computed `P(set 1 tiebreak) / P(3 sets) = 35.1%` and initially read it as "P(3 sets | set 1 tiebreak)". That is an inverted conditional — the expression is actually `P(set 1 TB | 3 sets)`. The correct conditional required the intersection count.

**Amendment:** the pipeline now emits `f2b_set1_tiebreak_and_length.csv` reporting **both** directions explicitly, plus the inverse, so the two cannot be confused. The substantive consequence is that the true association runs *opposite* to the erroneous reading: see §Filter 2 in the report. This is recorded because the near-miss is exactly the class of error the framework's "distinguish observed from calculated" rule exists to catch.

