# Study Specification — STUDY-002

**Status:** REGISTERED before any outcome was computed.
**Registered:** 2026-11-15T08:12Z
**Protocol version:** 1.0.0
**Analyst/agent:** Arena.ai research agent

> **Declaration of ordering.** Written after inspecting only file availability and
> byte sizes. No player outcome measure had been computed when the analysis window,
> eligibility rules and denominators below were fixed.

> **What this study is NOT.** It is a descriptive historical profile study. It does
> **not** predict any match. It does **not** produce per-player probabilities of
> winning or losing in two or three sets. It is explicitly forbidden from being used
> to construct such a probability, and §12 of the report states this.

---

## 1. Research question

**Primary:** For a named list of 18 players, what does their recorded match history
look like — how many completed singles matches, on which surfaces, at which event
levels — and among those completed matches, what share ended in two versus three
conventional sets?

**Secondary (descriptive, registered):**
- S1: Distribution of event level and surface within each player's history.
- S2: Straight-set share and three-set share with numerator, denominator and exact
  95% Wilson interval.
- S3: First-set outcome record (how often the player who won set 1 in their matches
  was the player in question).
- S4: Which records are too small to characterise, reported explicitly rather than
  suppressed.

**Explicitly excluded:** any probability, forecast, ranking, verdict, or comparison
between players. No cross-player "more likely" statement is produced, because
comparing raw historical aggregates across players with different opponents,
surfaces, levels and eras is not a valid comparison — see §11.

## 2. Named players (the full population of this study)

1. Oskari Paldanius
2. Svyatoslav Gulin
3. Kimmer Coppejans
4. Adrian Oetzbach
5. Aaron Funk
6. Carlo Alberto Caniato
7. Michael Vrbensky
8. Vadym Ursu
9. Jay Clarke
10. Arvid Nordquist
11. Cezar Cretu
12. Felix Alopaeus
13. John Sperle
14. Moez Echargui
15. Luka Mikrut
16. Iiro Vasa
17. Sumit Nagal
18. Sebastian Gima

These 18 names were supplied by the user as a list of fixtures. **This study analyses
each player's own history independently. It does not analyse the pairings, does not
compare players within a pairing, and makes no statement about any of those matches.**

## 3. Population and window

| Item | Value |
|---|---|
| Discipline | Men's singles |
| Event levels | ATP Tour (`A`,`M`,`G`,`F`), Challenger (`C`), ITF/Futures (`S` or equivalent codes present in the futures files) |
| Date window | **2015-01-01 → 2026-06-01** |
| Match status | Completed, conventional scoring |
| Format | Best-of-3 and best-of-5, **always reported separately** |

**Window rationale, fixed before data extraction:** 2015-01-01 was chosen so that even
the least-active player has a usable history, while avoiding an unbounded retrospective
window that would pool materially different eras of the sport. 2026-06-01 is the end
of source coverage and is a property of the data, not a choice.

## 4. Sources

| Item | Value |
|---|---|
| Source | `Aneeshers/tennis-sackmann-archive` (GitHub mirror) |
| Upstream authorship | Jeff Sackmann's tennis datasets |
| Files | `atp/atp_matches_YYYY.csv`, `atp/atp_matches_qual_chall_YYYY.csv`, `atp/atp_matches_futures_YYYY.csv` for YYYY = 2015…2026 |
| Retrieval | `api.github.com` contents API, `Accept: application/vnd.github.raw` |
| Retrieval date | 2026-11-15 |
| Tier | 3–4 (specialist database). **Not** official ATP records |
| Licence | CC BY-NC-SA 4.0 per repository description; raw rows not redistributed |

**Declared coverage gap:** source coverage ends 2026-06-01. Matches played
2026-06-02 → 2026-11-15 (≈5.5 months) are **absent**. Profiles are therefore
historical to 2026-06-01 and must not be described as current.

## 5. Player identification

A record belongs to a player if the normalised full name (NFKD, diacritics stripped,
lower-cased, punctuation removed) matches `winner_name` or `loser_name` **exactly**.

Name-matching policy, fixed in advance:
- **Exact normalised full-name match only.** No surname-only matching, no fuzzy
  matching, no manual adjudication of similar names.
- Where a surname match occurs but the full name does not, the record is **not**
  counted; a count of such near-misses is reported per player so the reader can see
  whether the policy might be dropping real records.
- No player-ID merging is performed. If the source assigns two IDs to one name, both
  are counted and the ID set is reported.

## 6. Eligibility and exclusions

Same exclusion taxonomy as STUDY-001 (E1 retirement, E2 walkover, E3 default,
E4 abandoned, E5 match tiebreak, E6 unparsed), applied per record **involving the
named player**. Each player's table shows their own counts.

Retirements are excluded from the structure distribution and counted separately.

## 7. Denominator rules (frozen)

| Measure | Numerator | Denominator |
|---|---|---|
| Straight-set share | player's completed matches ending in exactly 2 conventional sets, best-of-3 only | player's eligible completed best-of-3 matches |
| Three-set share | completed matches ending in exactly 3 conventional sets, best-of-3 only | player's eligible completed best-of-3 matches |
| Best-of-5 structure | reported separately | best-of-5 eligible matches only |
| Set-1 record | matches where the player won set 1 | player's eligible completed matches |

**Best-of-3 and best-of-5 are never pooled.** A player with both formats gets two
separate rows.

## 8. Pre-declared filter statuses

| Filter | Status | Reason |
|---|---|---|
| 1 Historical structure | **Analysed** (per player) | Score data supports it |
| 2 First-set context | **Analysed** (per player, descriptive) | Derivable from scores |
| 3 After winning set 1 | **Analysed** (per player, descriptive) | Same data |
| 4 After losing set 1 | **Analysed** (per player, descriptive) | Same data |
| 5 Set competitiveness | **Analysed** (per player, set-level denominators) | Games from scores |
| 6 Tiebreak structure | **Analysed** (per player) | TB marker in scores |
| 7 Serve by set | **Unavailable** | Source provides match totals only; no set-level serve data exists for these levels |
| 8 Return by set | **Unavailable** | Same |
| 9 Deciding-set structure | **Analysed** (per player, where n permits) | Conditional on reaching a decider |
| 10 Surface/competition context | **Analysed** (per player, as description of their history) | Surface/level recorded |

## 9. Statistical methods

- Counts and denominators everywhere; shares as derived display only.
- **Wilson 95% intervals** on every proportion, including on small samples, so that
  wide intervals visibly communicate weak evidence.
- **Small-sample thresholds declared now:** n < 10 → "insufficient to characterise" and
  no interval-based language; n = 10–29 → reported with an explicit caution flag;
  n ≥ 30 → reported normally. These thresholds apply to the structure denominators.
- **No hypothesis tests between players.** No player-vs-player comparison is made.
- No imputation, no regression, no adjustment for opponent quality.
- Match-level aggregation; each match counted once per player.

## 10. Outputs

`studies/STUDY-002/outputs/player_profiles.csv` — one row per player per format.
`studies/STUDY-002/outputs/player_level_surface.csv` — level and surface counts.
`studies/STUDY-002/outputs/player_match_structure.csv` — set-count distribution per player.
`studies/STUDY-002/outputs/name_matching_audit.csv` — near-miss counts per player.
`studies/STUDY-002/outputs/source_manifest.csv`
`studies/STUDY-002/REPORT.md`

## 11. Known limitations (declared in advance)

1. **Single tier-3 source; no official cross-check available.**
2. **Coverage ends 2026-06-01.** Not current form; a five-and-a-half-month gap.
3. **No opponent-quality adjustment.** Aggregates pool matches against very different
   opposition. A high straight-set share may reflect weaker typical opposition rather
   than anything intrinsic.
4. **No set-level serve/return data** (Filters 7–8 unavailable).
5. **Mixed levels and surfaces.** ITF and Challenger and tour-level matches are pooled
   only where explicitly separated; where pooled, the mix differs per player and is a
   confounder.
6. **Small samples.** At least one named player has a single recorded match. Such a
   profile carries essentially no information and is flagged as such.
7. **Historical aggregates are not stable traits.** Per the charter, a player's
   historical aggregate must not be treated as a permanent characteristic.
8. **The 18 players were selected by the user as fixtures**, not sampled. They are not
   a representative sample of any population, and no population-level inference is
   made.

## 12. Prohibition on conversion

This study's outputs **must not** be converted into per-match probabilities,
exact-set forecasts, "verdicts", or rankings for any fixture. The charter's rule is
explicit: historical set frequencies are not future probabilities. The report repeats
this prohibition in its conclusion, and the output CSVs carry a `NOT_A_PROBABILITY`
warning column.

---

## 14. Protocol amendments

### A1 — best-of-5 matches were being silently discarded

**Found:** the shared `parse_score()` from STUDY-001 hardcoded best-of-3 validation
(2–3 sets, 2-set winner tally). Every best-of-5 match failed as "unparseable", so
Sumit Nagal's Grand Slam best-of-5 records vanished from his profile.

**Fix:** `parse_score(score, best_of=3)` now validates against the requested format;
the default preserves STUDY-001 behaviour exactly. Seven regression tests added
(suite 28/28). STUDY-001 re-run produced a **byte-identical** result — verified by
`git diff` returning nothing, with 24,292 eligible matches either way.

### A2 — surname near-miss KeyError

Index keyed by display name, queried by normalised name. Fixed; no effect on published
numbers, but it had been suppressing the audit column.

### A3 — surface case normalisation

Source contains both `Clay`/`clay` and `Carpet`/`carpet`. Counting raw values split
surface totals. Normalised to the controlled vocabulary; 53 empty values → `unknown`,
not zero.

### A4 — format-relative column naming

`two_set`/`three_set` columns were meaningless for best-of-5 rows. Replaced with
`straight_set` (minimum sets for format) and `went_distance` (maximum), with the full
set-count distribution published separately.

### A5 — set-1 counters were pooled across formats

**Found:** `set1_won`/`set1_lost` were single integers on the Profile, so a player with
both formats printed the *pooled* total on both rows. Nagal's best-of-5 row claimed
364 first-set wins when the correct figure is 4.

**Fix:** counters keyed by format. Integrity check `set1_won + set1_lost == n` now
passes for every player × format (zero violations).

**Why this matters:** this defect would have produced a table that looked entirely
plausible — plausible numbers, correct row count, correct format split — while
silently misreporting every mixed-format player. It was caught only by asserting the
internal identity, which is now a standing check rather than an ad-hoc one.
