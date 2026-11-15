# STUDY-001 — Set Structure in ATP Challenger Men's Singles, 2024–2026

## 1. Metadata

| Field | Value |
|---|---|
| Study ID | STUDY-001 |
| Report version | 1.0 |
| Protocol version | 1.0.0 (repository framework) |
| Repository commit | see `git log` for this file; base `83c59b9` |
| Dataset version/fingerprint | per-file SHA-256 in `outputs/source_manifest.csv` |
| Analyst/agent | Arena.ai research agent |
| Extraction date | 2026-11-15 |
| Analysis date | 2026-11-15 |
| Study date range | 2024-01-01 → 2026-06-01 |
| Specification | `STUDY_SPECIFICATION.md` (registered before outcomes computed; amendments A1–A6) |

---

## 2. Question and scope

**Primary question.** Among completed ATP Challenger men's singles matches of 2024-01-01 to 2026-06-01, how were matches distributed across conventional set counts, and how did that distribution differ by surface, round and season?

**Population.** ATP Challenger (`tourney_level` = `C`), men's singles, best-of-three sets, conventional scoring.

**Deliberately excluded from scope:** any forecast of an unplayed match; any probability statement about a future match; any winner prediction; any betting-market data. This study is wholly retrospective.

**Important scope limits, stated up front:**
- This is **Challenger only**. Nothing here transfers to ATP Tour, Grand Slam, WTA, ITF, or doubles.
- **Best-of-3 only.** No best-of-5 comparison exists within this population.
- The source is a **tier 3–4 specialist database mirror**, not official ATP records. No official cross-check was possible.
- Source coverage **ends 2026-06-01**, about 5.5 months before the analysis date.

---

## 3. Sample construction

| Stage | n |
|---|---:|
| Candidate rows (all three season files) | 28,564 |
| Excluded: not Challenger level `C` | 3,171 |
| In-frame records (level C, best-of-3, in-window, valid surface) | 25,378 |
| Excluded E1 — retirements | 941 |
| Excluded E2 — walkovers | 139 |
| Excluded E3 — defaults | 4 |
| Excluded E4 — abandoned | 0 |
| Excluded E5 — match tiebreaks | 0 |
| Excluded E6 — unparsed | 2 |
| **Eligible completed matches** | **24,292** |

Every exclusion is itemised in `outputs/data_quality_exclusions.csv`. The two residual E6 records (`6-1 0-0`, `7-5 0-0`, both Manama CH) carry no status token and are unclassifiable; they are listed rather than dropped silently.

Three notes on the exclusions:

- **Retirements (941, 3.7%)** are excluded from the primary distribution but are not wasted: 781 of them had at least one completed set, and their progress distribution is reported in the sensitivity table.
- **Match tiebreaks: zero.** Every level-C record in this window is conventional scoring (`best_of` = 3 with no bracket notation). This contrasts with the 2023–2024 Davis Cup / Laver Cup rows identified in AUD-001 and confirms the match-tiebreak hazard does not touch this particular population.
- **Walkovers (139)** have no played structure and never enter a denominator.

---

## 4. Completeness

| Variable | Available | Missing | Completeness |
|---|---:|---:|---:|
| Score string | 25,378 | 15 | 99.94% |
| Set scores (derived) | 24,292 | 0 in eligible | 100% of eligible |
| Surface | 25,393 | 0 | 100% |
| Format (`best_of`) | 25,393 | 0 | 100% |
| Round | 25,393 | 0 | 100% |
| Match duration (`minutes`) | 25,160 | 233 | 99.08% |
| Match-level serve totals | 25,316 | 77 | 99.70% |
| **Set-level serve stats** | **0** | **25,393** | **0%** |
| Indoor/outdoor | 0 | 25,393 | 0% |

Missingness is low and does not cluster by season (minutes: 98.70% / 99.26% / 99.44% for 2024/2025/2026). The two hard zeros are structural, not incidental: the source supplies serve totals **per match only**, and carries no indoor/outdoor flag.

---

## 5. Ten-filter results

### Filter 1 — Historical match-structure distribution · **ANALYSED**

**Denominator:** eligible completed matches (n = 24,292).
**Numerator:** matches lasting exactly 2 or exactly 3 conventional sets.

| Stratum | n | 2 sets | 95% CI | 3 sets | 95% CI |
|---|---:|---:|---|---:|---|
| **All eligible** | **24,292** | **66.1%** | 65.5–66.7 | **33.9%** | 33.3–34.5 |
| Hard | 12,089 | 66.4% | 65.6–67.2 | 33.6% | 32.8–34.4 |
| Clay | 11,772 | 65.8% | 64.9–66.7 | 34.2% | 33.3–35.1 |
| Grass | 431 | 64.0% | 59.4–68.4 | 36.0% | 31.6–40.6 |
| 2024 | 9,443 | 66.3% | 65.3–67.2 | 33.7% | 32.8–34.7 |
| 2025 | 9,877 | 66.1% | 65.2–67.1 | 33.9% | 32.9–34.8 |
| 2026 (partial) | 4,972 | 65.5% | 64.2–66.8 | 34.5% | 33.2–35.8 |
| Main draw (R32–F) | 15,747 | 64.7% | 63.9–65.4 | 35.3% | 34.6–36.1 |
| Qualifying (Q1–Q2) | 8,545 | 68.7% | 67.7–69.6 | 31.3% | 30.4–32.3 |
| Round Q1 | 5,557 | 70.7% | 69.5–71.9 | 29.3% | 28.1–30.5 |
| Round Q2 | 2,988 | 64.9% | 63.1–66.6 | 35.1% | 33.4–36.9 |
| Round R32 | 8,097 | 65.5% | 64.5–66.5 | 34.5% | 33.5–35.5 |
| Round R16 | 4,063 | 65.1% | 63.6–66.6 | 34.9% | 33.4–36.4 |
| Round QF | 2,045 | 61.9% | 59.8–64.0 | 38.1% | 36.0–40.2 |
| Round SF | 1,020 | 62.5% | 59.4–65.4 | 37.5% | 34.6–40.6 |
| Round F | 522 | 63.0% | 58.8–67.1 | 37.0% | 32.9–41.2 |

**Observed:** roughly two-thirds of completed Challenger matches (66.1%, 95% CI 65.5–66.7) finished in straight sets in this sample.

**Surface:** differences are small and the intervals overlap substantially. Hard 66.4% vs Clay 65.8% is a 0.6 pp gap with a confidence interval difference that does not clearly exclude zero. Grass (64.0%, n = 431) is too small to interpret separately.

**Round:** a gradient exists from Q1 (70.7% straight sets) through to QF (61.9%). The Q1 figure is the clearest outlier. Two candidate explanations — qualifying draws pairing very unevenly-matched players, and best-of-3 qualifying having different competitive dynamics — are **not distinguished by this design**, and the margin across main-draw rounds (65.5% → 61.9%) is modest. This is labelled **exploratory**.

### Filter 2 — First-set outcome context · **ANALYSED**

**Denominator:** eligible completed matches (n = 24,292). Indexed by **first-set winner** (= the eventual match winner in the row below).

| Measure | n | Rate | 95% CI |
|---|---:|---:|---|
| Set-1 winner also won the match | 20,037 | 82.5% | 82.0–83.0 |
| Set-1 winner lost the match ("comeback") | 4,255 | 17.5% | 17.0–18.0 |
| Set 1 was a tiebreak | 2,889 | 11.9% | 11.5–12.3 |

**First-set margin distribution** (absolute games, n = 24,292):

| \|margin\| | n | share |
|---|---:|---:|
| 1 | 3,714 | 15.3% |
| 2 | 8,130 | 33.5% |
| 3 | 5,621 | 23.1% |
| 4 | 3,646 | 15.0% |
| 5 | 2,405 | 9.9% |
| 6 | 776 | 3.2% |

The modal first set is a **2-game margin** (33.5%), which corresponds to 6-4. Note that absolute margin is reported rather than signed margin: set 1 can be won by the player who ultimately loses the match, so a signed value would not be a "margin".

**An association worth reporting, and one worth being careful about.** A first-set tiebreak is associated with **shorter** matches in this sample, not longer:

| Measure | n | Rate | 95% CI |
|---|---:|---:|---|
| P(3 sets \| set 1 was a tiebreak) | 659 / 2,889 | **22.8%** | 21.3–24.4 |
| P(3 sets \| set 1 was not a tiebreak) | 7,583 / 21,403 | **35.4%** | 34.8–36.1 |
| P(set 1 was a tiebreak \| 3 sets) *(inverse direction)* | 659 / 8,242 | 8.0% | 7.4–8.6 |

That is a **12.6 pp difference** in the direction opposite to the intuitive guess that tight first sets predict long matches. The inverse conditional (8.0%) is reported alongside deliberately, because it is easy to compute one and read the other.

*Replication:* the association holds in **all nine** predeclared strata, same direction, between −10.1 pp (qualifying) and −19.3 pp (grass, n = 75 tiebreak matches):

| Stratum | P(3set \| TB) | n | P(3set \| no TB) | n | diff |
|---|---:|---:|---:|---:|---:|
| All | 22.8% | 2,889 | 35.4% | 21,403 | −12.6 |
| Hard | 22.8% | 1,525 | 35.2% | 10,564 | −12.3 |
| Clay | 23.0% | 1,289 | 35.6% | 10,483 | −12.6 |
| Grass | 20.0% | 75 | 39.3% | 356 | −19.3 |
| 2024 | 23.0% | 1,123 | 35.1% | 8,320 | −12.2 |
| 2025 | 22.5% | 1,142 | 35.4% | 8,735 | −12.8 |
| 2026 | 23.1% | 624 | 36.1% | 4,348 | −13.1 |
| Main draw | 23.0% | 1,984 | 37.1% | 13,763 | −14.1 |
| Qualifying | 22.3% | 905 | 32.4% | 7,640 | −10.1 |

Consistency across independent strata makes a sampling artifact less likely, but it **does not** identify a mechanism. It is an observed association, and this study makes no causal claim about it.

### Filter 3 — After winning the first set · **ANALYSED (descriptive)**

Among matches where a player won set 1 (n = 24,292 set-1 winners; one row per match, not two):
- that player won the match in 20,037 cases (82.5%);
- the match ended in straight sets in 16,050 cases.

**Dependence handled:** each match contributes exactly one set-1 winner, so no match is double-counted. The 82.5% is a match-level rate, not a player-level rate.

### Filter 4 — After losing the first set · **ANALYSED (descriptive)**

Defining "comeback" exactly as the specification did — lost set 1 and won the match:
- 4,255 of 24,292 (17.5%, 95% CI 17.0–18.0).

This is the complement of Filter 3 by construction and is reported for completeness, not as an independent finding. It is **not** a claim about any player's or any group's "resilience".

### Filter 5 — Set competitiveness · **ANALYSED**

**Denominators are sets, with contributing matches shown.**

| Set position | Sets (n) | Contributing matches | Mean total games | Median | Mean \|margin\| | Median | Tiebreak sets | TB share | 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 24,292 | 24,292 | 9.68 | 9.0 | 2.80 | 3.0 | 2,889 | 11.9% | 11.5–12.3 |
| 2 | 24,292 | 24,292 | 9.54 | 9.0 | 2.92 | 3.0 | 2,595 | 10.7% | 10.3–11.1 |
| 3 | 8,242 | 8,242 | 9.60 | 9.0 | 2.87 | 3.0 | 1,187 | 14.4% | 13.7–15.2 |

Set 2 has slightly more games and a marginally larger mean margin than set 1; set 3 has the highest tiebreak share. Differences are small. Because sets within a match are **not independent**, no significance test is applied to these set-position differences; they are descriptive only. All three medians being 9.0 shows the distributions are concentrated.

More games does not mean a closer set — a 7-5 set has 12 games and a 2-game margin. The two columns are reported separately for that reason.

### Filter 6 — Tiebreak structure · **ANALYSED**

| Measure | n / denominator | Rate | 95% CI |
|---|---|---:|---|
| Tiebreak sets / conventional sets | 6,671 / 56,826 | 11.7% | 11.5–12.0 |
| Matches with ≥1 tiebreak / matches | 6,114 / 24,292 | 25.2% | 24.6–25.7 |
| Hard: TB sets / sets | 3,557 / 28,240 | 12.6% | 12.2–13.0 |
| Hard: matches with ≥1 TB / matches | 3,227 / 12,089 | 26.7% | 25.9–27.5 |
| Clay: TB sets / sets | 2,949 / 27,569 | 10.7% | 10.3–11.1 |
| Clay: matches with ≥1 TB / matches | 2,739 / 11,772 | 23.3% | 22.5–24.0 |
| Grass: TB sets / sets | 165 / 1,017 | 16.2% | 14.1–18.6 |
| Grass: matches with ≥1 TB / matches | 148 / 431 | 34.3% | 30.0–38.9 |

**Observed:** one conventional set in nine (11.7%) was a tiebreak, and one match in four (25.2%) contained at least one.

**Surface:** the ordering Hard (12.6%) > Clay (10.7%) is consistent across both the set-level and match-level measures, and the confidence intervals do not overlap. Grass shows a higher rate (16.2%) but rests on 1,017 sets from 431 matches; the interval is wide and grass Challenger events are few and seasonally clustered, so this is **exploratory**.

The set-level and match-level denominators are kept separate throughout. The set-level rate is **not** the match-level rate and they must not be used interchangeably.

### Filter 7 — Serve performance by set · **UNAVAILABLE**

**Required:** per-set service counts. **Available in source:** per-match totals only (`w_svpt`, `w_1stIn`, `w_ace`, `w_bpSaved`, and loser equivalents), 99.70% complete.

`PROTOCOL.md` §4 and `FILTER_CATALOG.md` Filter 7 forbid deriving set-level values from match totals, and I did not do so. There is no set-level serve data in this population. **This filter cannot be analysed and no substitute estimate is offered.**

### Filter 8 — Return performance by set · **UNAVAILABLE**

Same reason as Filter 7, in the mirror direction. No set-level return data exists in this source for this population.

### Filter 9 — Deciding-set structure · **ANALYSED**

Denominator: matches that reached a third set (n = 8,242).

| Measure | n / denominator | Rate | 95% CI |
|---|---|---:|---|
| Deciding sets that were tiebreaks | 1,187 / 8,242 | 14.4% | 13.7–15.2 |

**Deciding-set margins** (n = 8,242):

| \|margin\| | n | share |
|---|---:|---:|
| 1 | 1,187 | 14.4% |
| 2 | 2,668 | 32.4% |
| 3 | 1,906 | 23.1% |
| 4 | 1,325 | 16.1% |
| 5 | 849 | 10.3% |
| 6 | 307 | 3.7% |

**Deciding-set scorelines** (n = 8,242): 6-4 1,928 (23.4%), 6-3 1,906 (23.1%), 6-2 1,325 (16.1%), 7-6 1,187 (14.4%), 6-1 849 (10.3%), 7-5 740 (9.0%), 6-0 307 (3.7%).

Deciding sets are marginally more likely to reach a tiebreak (14.4%) than sets 1 or 2 (11.9%, 10.7%), and the modal deciding set is 6-4 rather than 6-3. No claim about "pressure" or "temperament" is made or supported; these are scoreline frequencies.

### Filter 10 — Surface and competition context · **ANALYSED, with limits**

| Context | Available? | Notes |
|---|---|---|
| Surface | Yes, 100% | Hard, Clay, Grass only; no carpet in this window |
| Round | Yes, 100% | R32, R16, QF, SF, F, Q1, Q2 |
| Season | Yes | 2024, 2025, and 2026 to 2026-06-01 |
| Event level | Single by design | All `C` = Challenger |
| Format | Single by design | All best-of-3 |
| Discipline | Single by design | Men's singles only |
| **Indoor/outdoor** | **No** | Not recorded in source; not inferred from event name |
| Draw type | Partly | Inferred from round labels (Q1/Q2 = qualifying; R32–F = main draw). This inference is stated, not silent |

Between-surface differences for structure (Filter 1) are small and inconclusive; for tiebreak frequency (Filter 6) the Hard > Clay ordering is consistent across set- and match-level denominators. Season differences are negligible: 66.3% / 66.1% / 65.5% straight sets for 2024 / 2025 / 2026.

---

## 6. Sensitivity checks

| Check | n | 2 sets | 3 sets |
|---|---:|---:|---:|
| Primary (retirements excluded) | 24,292 | 66.1% | 33.9% |
| Main draw only | 15,747 | 64.7% | 35.3% |
| Qualifying only | 8,545 | 68.7% | 31.3% |
| Excluding 2026 (partial season) | 19,320 | 66.2% | 33.8% |
| 2024 only | 9,443 | 66.3% | 33.7% |
| 2025 only | 9,877 | 66.1% | 33.9% |

**Retirement progress** (separate, not comparable): of 941 excluded retirements, 781 had at least one completed set — 572 stopped during set 2, 209 during set 3, and 160 ended within set 1. Shares of *retirements*, not of matches; retirements cannot enter a 2-vs-3-set distribution because they have no final set count.

**Did conclusions change?** No. The headline 2-set share sits between 64.7% and 68.7% across every reasonable sample variation, and removing the partial 2026 season moves it by 0.1 pp. The main-draw/qualifying split is the largest single shift (4.0 pp) and is reported as a real compositional difference rather than noise, though it does not alter the two-thirds characterisation.

**Dependence caveat.** No sensitivity check removes within-match dependence, because the structure distribution is already one row per match. The set-position comparisons in Filter 5 are the only place where sets are the unit, and no test is applied there.

---

## 7. Main observations

Each statement carries its n and denominator.

1. **Two-thirds of completed Challenger matches were straight-setters.** 16,050 / 24,292 = 66.1% (95% CI 65.5–66.7). Three-setters: 8,242 / 24,292 = 33.9%.
2. **Winning set 1 was followed by winning the match in 82.5% of matches** (20,037 / 24,292). Conversely 17.5% (4,255 / 24,292) of set-1 winners lost.
3. **Sets were closely contested.** Modal absolute margin was 2 games in every set position — 33.5% of first sets, and 32.4% of deciding sets. Mean total games per set stayed between 9.54 and 9.68 across positions.
4. **Tiebreaks occurred in one set in nine and one match in four.** 6,671 / 56,826 sets = 11.7%; 6,114 / 24,292 matches = 25.2%.
5. **Tiebreak frequency ordered Hard > Clay consistently** — 12.6% vs 10.7% of sets, and 26.7% vs 23.3% of matches, with non-overlapping intervals on both measures. Grass was higher still (16.2% of sets) but on 1,017 sets.
6. **A first-set tiebreak was associated with shorter matches,** not longer: 22.8% (659 / 2,889) reached a third set versus 35.4% (7,583 / 21,403) when set 1 was not a tiebreak. The direction held in all nine strata. Mechanism is unidentified and no causal reading is supported.
7. **Deciding sets were slightly more tiebreak-prone** (14.4%, 1,187 / 8,242) than sets 1–2 (11.9%, 10.7%).
8. **Season made almost no difference** to structure: 66.3%, 66.1%, 65.5% straight sets in 2024, 2025, 2026.

---

## 8. Limitations

1. **Single source, tier 3–4, no official cross-check.** Official ATP records were unreachable from the analysis environment. No claim of "official verification" is made anywhere in this report.
2. **Only one dataset.** Agreement between two sources cannot be asserted; the framework's replication requirement is **not** met.
3. **Coverage gap.** Source ends 2026-06-01; the ~5.5 months to the analysis date are absent. 2026 is a partial season and is marked as such throughout.
4. **Filters 7 and 8 missing entirely.** No set-level serve/return analysis is possible in this population. This is the single largest gap in the ten-filter programme.
5. **No opponent-quality adjustment.** Rankings are 99.28% available but were not used; results are unadjusted associations, and player quality is a plausible confounder behind most of them.
6. **No indoor/outdoor, no conditions, no court speed.**
7. **Exploratory subgroup findings.** Round gradients, grass tiebreak rates and the Q1 effect are exploratory; 10 filters × several strata creates a large multiple-comparison surface and no confirmatory test was predeclared.
8. **Qualifying included in the primary sample**, and qualifying matches behave differently (68.7% vs 64.7% straight sets). The primary figure is therefore a blend of two distinguishable populations.
9. **Descriptive only.** No causal design was used and no causal conclusion is drawn.

---

## 9. What this study cannot establish

- It cannot forecast any upcoming match, including its set count or winner.
- It cannot state the probability that a future match finishes in two or three sets. A historical frequency in this sample is not a future probability, and no conversion is offered.
- It cannot attribute the tiebreak–match-length association to any mechanism, player trait, or tactical cause.
- It cannot speak to ATP Tour, Grand Slam, WTA, ITF or doubles tennis.
- It cannot speak to serve or return behaviour by set, at all.
- It cannot speak to the period after 2026-06-01.

---

## 10. Sources and reproducibility

| Source | URL/ID | Fields used | Retrieved | Verification |
|---|---|---|---|---|
| `atp_matches_qual_chall_2024.csv` | GitHub API contents, `Aneeshers/tennis-sackmann-archive` | tourney/round/date, players, score, surface, best_of, level | 2026-11-15 | single source, structural checks passed |
| `atp_matches_qual_chall_2025.csv` | as above | as above | 2026-11-15 | single source, structural checks passed |
| `atp_matches_qual_chall_2026.csv` | as above | as above | 2026-11-15 | single source, structural checks passed |
| Field semantics | `atp/matches_data_dictionary.txt` (same repo) | definitions of `tourney_level`, `best_of`, `score` | 2026-11-15 | read in full |

Per-file SHA-256, byte counts and URLs: `outputs/source_manifest.csv`.

**Reproduce:**
```
# 1. fetch the three CSVs listed in outputs/source_manifest.csv
# 2. verify sha256
# 3. run
python3 tools/study001_pipeline.py --input-dir <dir> --out-dir studies/STUDY-001/outputs
# 4. tests
cd tools && python3 -m unittest test_study001_pipeline -v
```

**Environment:** Python 3.11.2, standard library only. No pandas/numpy required. Wilson intervals implemented in-pipeline. **Unit tests: 21/21 pass**, covering score grammar, tiebreak detection, retirement/walkover/default/abandoned handling, match-tiebreak rejection, set-tally consistency and Wilson bounds against a known value.

**Defects found and fixed during this study**, each recorded as a dated amendment in the specification rather than quietly patched:
- A1 — tiebreak-point parenthetical made optional for TB detection.
- A2 — **status resolution had to precede parse validation**; this was mislabelling all 941 retirements as "unparsed" (E1 0 → 941).
- A3 — `Ret'd` spelling variant (1 record).
- A4 — retirements retain completed sets; the sensitivity row had been meaningless.
- A5 — **an inverted conditional in my own reasoning**: `P(set1 TB)/P(3 sets)` is `P(TB | 3 sets)`, not `P(3 sets | TB)`. Correcting it reversed the direction of the headline association. The pipeline now emits both directions.
- A6 — signed game margin was being labelled `abs_game_margin`; set 1 can be won by the match loser. Fixed, with an assert reconciling signed negatives against the comeback count.

The A2 and A5 errors are worth stating plainly: both would have produced a plausible-looking but wrong report. Neither changed the eligible sample, but A5 would have inverted a substantive finding.

---

## 11. Neutral conclusion

In this sample of **24,292 completed ATP Challenger men's singles matches** played 2024-01-01 to 2026-06-01, **66.1% finished in straight sets** (95% CI 65.5–66.7) and 33.9% in three. Winning the first set was followed by winning the match 82.5% of the time. One set in nine was a tiebreak and one match in four contained one. Surface differences in structure were small and inconclusive; the clearest surface signal was tiebreak frequency, ordered Hard > Clay on both set- and match-level denominators. Seven of the ten filters were analysed; **serve-by-set and return-by-set were unanalysable because the source carries no set-level data for this population**, and no estimate was substituted.

The most notable observation — that a first-set tiebreak was associated with *shorter* matches, consistently across nine strata — is descriptive. This study offers no mechanism for it and explicitly declines to convert it into any statement about a future match.
