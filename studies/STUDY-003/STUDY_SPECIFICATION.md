# Study Specification — STUDY-003

**Status:** REGISTERED before any outcome was computed.
**Registered:** 2026-11-15T08:24Z
**Protocol version:** 1.0.0
**Analyst/agent:** Arena.ai research agent

> **What this study is NOT.** Descriptive historical profiles restricted to hard-court
> matches. It does **not** predict any match, does **not** produce probabilities of
> winning or losing in two or three sets, and does **not** rank or compare players.
> §12 of the report states this and the CSVs carry a `NOT_A_PROBABILITY` column.

---

## 1. Research question

**Primary:** For 18 named players, restricted to **hard-court** matches, what does their
recorded history look like — match volume, event level, and the split of completed
matches between the minimum and maximum number of sets for the format played?

**Secondary:**
- S1: Hard-court match volume per player, and what share of each player's total history
  is hard-court (context for how informative a hard-court filter is for that player).
- S2: Prior head-to-head meetings between the nine named pairings, at any surface, with
  surface and score recorded.
- S3: Explicit small-sample flagging.

**Excluded:** any probability, forecast, verdict, ranking, or player comparison.

## 2. Named players (the whole population of this study)

Luca Nardi, Milos Karol, Matthew William Donald, Martin Krumich, Cyril Vandermeersch,
Alibek Kachmazov, Hugo Grenier, Florent Bax, Buvaysar Gadamauri, Adrien Gobat,
Matisse Bobichon, Ugo Blanchet, Alejandro Moro Canas, Robin Catry, Lenny Couturier,
Jonas Forejtek, Filip Cristian Jianu, Carlos Taberner.

Supplied by the user as a set of nine fixtures at an event they describe as
"ATP Challenger Metz, France Men Singles, hard courts".

## 3. Population and window

| Item | Value |
|---|---|
| Discipline | Men's singles |
| Surface | **Hard only** (after normalisation; see STUDY-002 A3) |
| Event levels | All levels present in source (ATP Tour, Challenger, ITF) — recorded separately |
| Date window | 2015-01-01 → 2026-06-01 |
| Status | Completed, conventional scoring |
| Format | Best-of-3 and best-of-5 reported separately |

## 4. Source

`Aneeshers/tennis-sackmann-archive`, 36 CSVs (`atp_matches_YYYY`,
`atp_matches_qual_chall_YYYY`, `atp_matches_futures_YYYY`, YYYY = 2015…2026),
retrieved 2026-11-15 via the GitHub contents API. Tier 3–4; **no official ATP
cross-check available**. Per-file SHA-256 in `outputs/source_manifest.csv`.

**Coverage ends 2026-06-01.**

## 5. Event identification — what the source does and does not confirm

This must be stated before any result, because it affects how the output may be used.

| Claim | Source status |
|---|---|
| "Metz, France" hosts men's events | **Confirmed** — 520 Metz records across 14 editions, 2015–2025 |
| The most recent Metz event in source is **2025-11-02, level `A` (ATP Tour), hard** | **Confirmed** [RUN] |
| A July 2025 **Metz ITF event on clay** also exists (level `25`) | **Confirmed** [RUN] — a reminder that "Metz" alone does not identify an event |
| This fixture list is an **ATP Challenger** event at Metz | **NOT CONFIRMED** — no 2026 Metz record exists in source; the source's only hard-court Metz event is ATP Tour level |
| The 2026 event is on **hard court** | **NOT CONFIRMED by source** — accepted as the user's stated parameter for filtering only |

**Consequence:** the hard-court filter is applied because the user specified it, not
because this study verified the event's surface or level. The report says so explicitly
and does not describe the fixtures as "Challenger".

## 6. Player identification

Exact normalised full-name match on `winner_name` / `loser_name`. No fuzzy or
surname-only matching. Near-misses counted and reported. Same policy as STUDY-002,
which documented a real case (Iiro Vasa vs **Eero Vasa**, 260 records) where surname
matching would have merged two different players.

## 7. Eligibility and exclusions

E1 retirement, E2 walkover, E3 default, E4 abandoned, E5 match tiebreak, E6 unparsed —
same taxonomy as STUDY-001/002, counted per player.

## 8. Denominator rules (frozen)

| Measure | Numerator | Denominator |
|---|---|---|
| Straight-set share | hard-court completed matches ending in the format's minimum set count (2 for bo3, 3 for bo5) | player's eligible hard-court completed matches **of that format** |
| Went-distance share | ending in the format's maximum set count | same |
| Hard-court share of history | player's hard-court matches | player's matches of all surfaces |

Best-of-3 and best-of-5 never pooled.

## 9. Statistical methods

Counts and denominators throughout; Wilson 95% intervals on every proportion.
Small-sample thresholds pre-declared: n < 10 → "insufficient to characterise";
n = 10–29 → "caution"; n ≥ 30 → "ok". No hypothesis tests between players.
Internal identity checks asserted: `set1_won + set1_lost == n` and
`straight + distance + intermediate == n`, per player per format.

## 10. Known limitations (declared in advance)

1. Single tier-3 source, no official cross-check.
2. Coverage ends five-and-a-half months before the analysis date; **not current form**.
3. **The event's level and surface are not verified by this study** (§5).
4. **Hard-court restriction reduces every sample** and does so unevenly: Filip Cristian
   Jianu has 96 hard-court matches of 584, while Carlos Taberner has 88 of 693 — a
   hard-court profile for these players describes a minority of their careers.
5. No opponent-quality adjustment.
6. No set-level serve/return data (Filters 7–8 unavailable).
7. Historical aggregates are not stable traits.
8. The 18 players were named as fixtures, not sampled; no population inference.
9. At least one player (Lenny Couturier, 8 matches total) cannot be characterised.

## 11. Outputs

`studies/STUDY-003/outputs/hard_court_profiles.csv`
`studies/STUDY-003/outputs/hard_court_share_of_history.csv`
`studies/STUDY-003/outputs/head_to_head.csv`
`studies/STUDY-003/outputs/name_matching_audit.csv`
`studies/STUDY-003/outputs/source_manifest.csv`
`studies/STUDY-003/REPORT.md`

## 12. Prohibition on conversion

Outputs must not be converted into per-match probabilities, exact-set forecasts,
verdicts or rankings for any fixture. Historical hard-court set frequencies are not
future probabilities.

## 13. Protocol amendments

*(none at registration)*
