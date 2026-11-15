# STUDY-002 — Descriptive Historical Profiles: 18 Named Players

## 1. Metadata

| Field | Value |
|---|---|
| Study ID | STUDY-002 |
| Report version | 1.0 |
| Protocol version | 1.0.0 |
| Analyst/agent | Arena.ai research agent |
| Extraction and analysis date | 2026-11-15 |
| Study date range | 2015-01-01 → 2026-06-01 |
| Format column semantics | `straight_set` = minimum sets for format (2 in bo3, 3 in bo5); `went_distance` = maximum (3 or 5) |
| Specification | `STUDY_SPECIFICATION.md`, amendments A1–A3 |

> ### This report contains no probabilities
>
> It describes what has already happened in recorded matches. It does **not** state
> the chance of any player winning or losing, in two sets, three sets, or otherwise.
> §9 explains why the numbers below cannot be validly combined into such a statement,
> and §11 records that doing so is prohibited by the research charter.

---

## 2. Question and scope

For each of 18 named players, what is the recorded match history — volume, event
levels, surfaces, and the split of completed matches between the minimum and maximum
number of sets for the format played?

**The 18 players were supplied by the user as a list of fixtures.** This study
analyses each player's own history **independently**. It does not analyse the pairings,
does not compare players within a pairing, and makes no statement about any of those
matches. They are also not a representative sample of any population.

**Window:** 2015-01-01 → 2026-06-01, men's singles, all event levels present in the
source, best-of-3 and best-of-5 reported separately.

---

## 3. Sources and coverage

| Item | Value |
|---|---|
| Source | `Aneeshers/tennis-sackmann-archive` (GitHub mirror of Jeff Sackmann's datasets) |
| Files | 36 CSVs: `atp_matches_YYYY`, `atp_matches_qual_chall_YYYY`, `atp_matches_futures_YYYY`, YYYY = 2015…2026 |
| Rows scanned | **323,673** match records |
| Retrieved | 2026-11-15, `api.github.com` contents API |
| Tier | 3–4 (specialist database). **No official ATP cross-check was possible** |
| Per-file SHA-256 | `outputs/source_manifest.csv` |

**Coverage gap, stated plainly:** the source ends **2026-06-01**. Today is
2026-11-15. Everything below is history up to that date and is **not** current form.
Matches from the last ~5.5 months are simply absent.

---

## 4. Sample construction and name matching

A record was assigned to a player only on an **exact normalised full-name match**
(diacritics stripped, case-folded, punctuation removed). No fuzzy matching, no
surname-only matching, and no manual adjudication.

**Total eligible match-records across the 18 players: 5,349.**

Exclusions per player are in `outputs/name_matching_audit.csv` (retirements,
walkovers, defaults, match tiebreaks and unparsed scores, all counted individually).

### A name-matching case that matters [RUN]

Two of the 18 surnames belong to **two different real players**:

| Player | Same-surname different player | Records wrongly attributable if surname matching were used |
|---|---|---|
| **Iiro Vasa** | **Eero Vasa** | **260** |
| Jay Clarke | Curtis Clarke | 13 |

This is why the exact-name policy is not pedantry. Matching on "Vasa" would have
merged Iiro Vasa's profile with 260 records belonging to his same-surnamed
contemporary — inflating his sample roughly fivefold and contaminating every share in
his row. The 257–260 near-misses for Iiro Vasa in the audit column are exactly this
other player, and were correctly **excluded**.

---

## 5. Per-player structure profiles

Best-of-3 matches only in this table (best-of-5 handled separately in §6).
`n` = eligible completed matches. Shares carry exact 95% Wilson intervals in the CSV;
suppressed here for width.

| Player | n | Straight sets (2) | Went distance (3) | Sample |
|---|---:|---:|---:|---|
| Kimmer Coppejans | 664 | 61.0% | 39.0% | ok |
| Sumit Nagal | 586 | 65.9% | 34.1% | ok |
| Moez Echargui | 583 | 64.2% | 35.8% | ok |
| Jay Clarke | 568 | 68.7% | 31.3% | ok |
| Michael Vrbensky | 483 | 68.3% | 31.7% | ok |
| Vadym Ursu | 400 | 70.0% | 30.0% | ok |
| Cezar Cretu | 387 | 71.6% | 28.4% | ok |
| Sebastian Gima | 361 | 70.6% | 29.4% | ok |
| Adrian Oetzbach | 301 | 68.8% | 31.2% | ok |
| Svyatoslav Gulin | 237 | 67.5% | 32.5% | ok |
| Luka Mikrut | 211 | 67.8% | 32.2% | ok |
| John Sperle | 171 | 67.8% | 32.2% | ok |
| Carlo Alberto Caniato | 126 | 74.6% | 25.4% | ok |
| Arvid Nordquist | 113 | 80.5% | 19.5% | ok |
| Iiro Vasa | 61 | 59.0% | 41.0% | ok |
| Aaron Funk | 41 | 63.4% | 36.6% | ok |
| Oskari Paldanius | 34 | 58.8% | 41.2% | ok |
| **Felix Alopaeus** | **1** | **100.0%** | **0.0%** | **insufficient** |

**Reading the table correctly.** The n column is the *player's own history*, not a
sample from which anything about a future match is drawn. The spread (58.8% to 80.5%)
is wide, and §9 explains why that spread is mostly *not* signal about the players.

**Error bars are narrow only where n is large.** Coppejans (n=664) and Echargui
(n=583) have intervals roughly ±3.5 pp. Paldanius (n=34) and Funk (n=41) have
intervals near ±16 pp. Alopaeus's single match tells you nothing whatsoever and is
flagged rather than silently presented as "100% straight sets".

---

## 6. Best-of-5 matches (separate, as required)

| Player | n | 3 sets | 4 sets | 5 sets | straight (3) | distance (5) | Sample |
|---|---:|---:|---:|---:|---:|---:|---|
| Sumit Nagal | 10 | 6 | 4 | 0 | 60.0% | 0.0% | caution |
| Jay Clarke | 6 | 3 | 2 | 1 | 50.0% | 16.7% | insufficient |
| Kimmer Coppejans | 5 | 2 | 1 | 2 | 40.0% | 40.0% | insufficient |

Only three of the 18 players have any best-of-5 matches in this window, and every one
of those samples is small. Nagal's 0% five-set rate is verified against the raw
records — six 3-setters and four 4-setters, no five-setter — but with n=10 the
interval is wide and no interpretation is offered.

**Best-of-5 and best-of-3 are never pooled anywhere in this study.**

---

## 7. Event level and surface composition

This is the context that makes the §5 numbers hard to compare. Counts per player
(`outputs/player_level_surface.csv`):

| Player | ITF $15k | ITF $25k | Challenger | ATP Tour | Grand Slam | Most common surface |
|---|---:|---:|---:|---:|---:|---|
| Kimmer Coppejans | 10 | 24 | 494 | 38 | 66 | Clay (438 of 664) |
| Sumit Nagal | 0 | 0 | 346 | 60 | 30 | Clay (400 of 586) |
| Moez Echargui | 105 | 94 | 192 | 9 | 1 | Hard (337 of 583) |
| Jay Clarke | 30 | 94 | 288 | 21 | 25 | Hard (274 of 568) |
| Michael Vrbensky | 56 | 104 | 199 | 4 | 0 | Clay (334 of 483) |
| Vadym Ursu | 120 | 44 | 96 | 3 | 0 | Hard (307 of 400) |
| Cezar Cretu | 182 | 100 | 88 | 2 | 0 | Clay (322 of 387) |
| Sebastian Gima | 205 | 70 | 79 | 0 | 0 | Clay (268 of 361) |
| Adrian Oetzbach | 193 | 44 | 35 | 0 | 0 | Clay (187 of 301) |
| Svyatoslav Gulin | 128 | 68 | 41 | 0 | 0 | Clay (198 of 237) |
| Luka Mikrut | 87 | 32 | 88 | 3 | 1 | Clay (174 of 211) |
| John Sperle | 102 | 35 | 34 | 0 | 0 | Clay (142 of 171) |
| Carlo Alberto Caniato | 62 | 31 | 33 | 0 | 0 | Clay (91 of 126) |
| Arvid Nordquist | 76 | 19 | 4 | 0 | 0 | Hard (73 of 113) |
| Iiro Vasa | 44 | 8 | 7 | 0 | 0 | Hard (38 of 61) |
| Aaron Funk | 31 | 10 | 0 | 0 | 0 | Hard (22 of 41) |
| Oskari Paldanius | 27 | 1 | 6 | 0 | 0 | Hard (28 of 34) |
| Felix Alopaeus | 1 | 0 | 0 | 0 | 0 | Hard (1 of 1) |

**This table is the reason the §5 percentages are not comparable.** Kimmer Coppejans's
664 matches are 74% Challenger-level or above and 66% on clay; Aaron Funk's 41 matches
are entirely ITF $15k/$25k. The two players' set-structure figures are measuring
different competitive environments, not different sets of skills.

Surface values were normalised to the controlled vocabulary before counting. The
source mixes case (`Clay` 144,391 vs `clay` 1,144 rows across the full scan) and has
53 empty values; unnormalised, case variants silently split surface totals. Detected
and fixed during this study (amendment A3).

---

## 8. First-set and tiebreak context

| Player | Format | Set 1 won | Set 1 lost | TB share |
|---|---|---:|---:|---:|
| Sumit Nagal | best-of-3 | 360 | 226 | 19.1% |
| Sumit Nagal | best-of-5 | 4 | 6 | 20.0% |
| Kimmer Coppejans | best-of-3 | 359 | 305 | 21.1% |
| Kimmer Coppejans | best-of-5 | 2 | 3 | 20.0% |
| Jay Clarke | best-of-3 | 337 | 231 | 23.2% |
| Jay Clarke | best-of-5 | 1 | 5 | 33.3% |
| Vadym Ursu | best-of-3 | 199 | 201 | 15.8% |
| Svyatoslav Gulin | best-of-3 | 149 | 88 | 16.5% |

*(Full column set, including absolute tiebreak counts, is in `outputs/player_profiles.csv`.
Set-1 won + set-1 lost = n for every player and format; an integrity check on this
identity returns zero violations. Formats are shown separately because pooling
best-of-3 and best-of-5 set-1 counts would mix incomparable denominators.)*

Note that these are **counts of what happened**, not rates of any capacity. A player
with more set-1 wins than losses simply won the first set more often in the recorded
matches; §9 explains what that does and does not imply.

---

## 9. Why these numbers cannot be turned into a per-player probability

This section is the most important one in the report.

Someone could look at Arvid Nordquist's 80.5% straight-set share and Kimmer
Coppejans's 61.0% and conclude that a match between them would probably be short or
long, or that one is "more likely" to win in straight sets. **That inference is
invalid for at least five independent reasons:**

1. **Different opposition.** These shares pool every opponent each player faced.
   Set structure depends heavily on the *opponent* — a strong server facing a weak
   returner produces different sets than two evenly matched players. Aggregate shares
   contain no information about any specific pairing.
2. **Different competitive environments.** As §7 shows, one player's history is
   mostly clay Challengers, another's is hard-court ITF $15k. The percentages measure
   the environment at least as much as the player.
3. **No opponent-interaction data exists in this source.** There is no field describing
   how these two players' games combine, and no head-to-head record for any of the nine
   pairings (verified: zero prior meetings between any of them in 2015–2026).
4. **Selection is not random.** These 18 were named as fixtures, not sampled. They are
   not representative of any population, so no population-level rate applies to them.
5. **The arithmetic does not work.** Win-in-2, lose-in-2, win-in-3 and lose-in-3 are
   not four independent quantities: exactly one occurs per match, so they must sum to 1.
   Deriving them requires P(match winner) *and* P(straight sets | that winner) — a
   forecast plus an interaction term. Neither is present in this data.

Additionally: the window ends 2026-06-01, so none of this is current; and one named
player has a single recorded match.

---

## 10. Limitations

1. **Single tier-3 source; no official cross-check.** Nothing here is "officially
   verified".
2. **Coverage ends 2026-06-01** — approximately 5.5 months before the analysis date.
3. **No opponent-quality adjustment**; ranking fields exist (99%+ complete) but were
   deliberately not used, and would not fix reasons 1–5 above in any case.
4. **Filters 7 and 8 unavailable** — the source carries match-total serve data only,
   so serve and return cannot be described by set for these levels.
5. **Mixed levels and surfaces within every player's history**, in different
   proportions per player.
6. **Small samples** for Alopaeus (1), Paldanius (34) and Funk (41).
7. **Historical aggregates are not stable traits** — the charter explicitly forbids
   treating them as such.
8. **Descriptive only.** No causal design, no hypothesis tests between players.

---

## 11. What this study cannot establish

- It cannot predict any of the nine fixtures, including set counts or winners.
- It cannot produce, and must not be used to produce, per-player probabilities of
  winning or losing in two or three sets. `STUDY_SPECIFICATION.md` §12 prohibits this
  conversion, and the output CSVs carry a `NOT_A_PROBABILITY` column as a machine-
  readable reminder.
- It cannot rank the 18 players or say who is "more likely" to do anything.
- It cannot describe current form, because the data ends 2026-06-01.
- It cannot say anything about serve or return by set.

---

## 12. Defects found during this study

Recorded as dated amendments rather than silently patched.

**A1 — best-of-5 matches were being silently discarded (parser bug in STUDY-001's
shared code).** `parse_score()` hardcoded best-of-3 validation: it required 2–3 sets
and a 2-set winner tally. Every best-of-5 match therefore failed as "unparseable".
This never surfaced in STUDY-001 because that population is 100% best-of-3 — it only
appeared here, on Sumit Nagal's Grand Slam records, when his best-of-5 count came out
as zero. Fixed by parameterising `best_of`; **default behaviour preserved**, and
re-running STUDY-001 produces a byte-identical result (verified by `git diff`: zero
changes, 24,292 eligible either way). Seven regression tests added; suite now 28/28.

**A2 — surname near-miss accounting raised a KeyError**, because the index was keyed
by display name but queried by normalised name. Fixed; no effect on any published
number, but it had been masking the near-miss audit column.

**A3 — surface case inconsistency.** The source contains both `Clay`/`clay` and
`Carpet`/`carpet`. Counting raw values split surface totals (e.g. Aaron Funk appeared
to have both "Clay 11" and "clay 3"). Normalised to the controlled vocabulary; 53
empty values mapped to `unknown`, not to zero.

**A4 — format-relative column naming.** The first version emitted `two_set`/`three_set`
columns for best-of-5 matches, where those categories are meaningless. Replaced with
format-relative `straight_set` (minimum sets) and `went_distance` (maximum sets), with
the full per-set-count distribution published separately.

---

## 13. Reproducibility

```
python3 tools/study002_profiles.py --input-dir <dir> --out-dir studies/STUDY-002/outputs
cd tools && python3 -m unittest test_study001_pipeline -v   # 28 tests
```

Python 3.11.2, standard library only. Parsing and Wilson intervals are shared with
STUDY-001, so the two studies cannot drift apart in how they read a score string.
Raw source rows are **not** committed (CC BY-NC-SA licence, ~61 MB); only aggregates
and the SHA-256 manifest are.

---

## 14. Neutral conclusion

This report describes the recorded histories of 18 named players between 2015-01-01
and 2026-06-01 — 5,349 eligible match-records in total, ranging from 1 to 664 per
player. Straight-set shares range from 58.8% to 80.5% in best-of-3 matches, but that
range principally reflects differences in the level, surface and opposition mix of
each player's history rather than differences between the players.

Three of the 18 have best-of-5 matches, all in small numbers, and these are reported
separately. Nothing in this report is a forecast, a probability, or a ranking, and the
data does not support constructing one for any of the nine fixtures.
