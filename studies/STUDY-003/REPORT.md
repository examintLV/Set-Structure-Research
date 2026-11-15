# STUDY-003 — Hard-Court Historical Profiles: 18 Named Players

## 1. Metadata

| Field | Value |
|---|---|
| Study ID | STUDY-003 |
| Report version | 1.0 |
| Protocol version | 1.0.0 |
| Analyst/agent | Arena.ai research agent |
| Extraction and analysis date | 2026-11-15 |
| Window | 2015-01-01 → 2026-06-01 |
| Surface filter | Hard only (normalised) |
| Rows scanned | 323,673 |
| Raw source | not committed (licence/size); SHA-256 manifest in `outputs/` |

> ### No probabilities in this report
> These are counts of completed hard-court matches. They are **not** the chance of
> any player winning or losing, in two sets, three sets, or otherwise. §8 explains why
> they cannot be converted into that, and §10 records that conversion is prohibited.

---

## 2. Question and scope

For 18 named players, restricted to **hard-court** matches: what does the recorded
history show — volume, share of their overall career, and the split of completed
matches between the minimum and maximum number of sets for the format played?

Nine prior head-to-head meetings were also found and are listed in §6.

**Players were supplied by the user as nine fixtures.** Each is profiled independently.
No pairing is analysed, and no player is ranked or compared against another.

---

## 3. Event identification — read this before using the numbers

The user described these as "ATP Challenger Metz, France Men Singles" on hard courts.
What the source can and cannot confirm:

| Claim | Status |
|---|---|
| Metz hosts men's events | **Confirmed** — 520 records, 14 editions, 2015–2025 |
| Most recent Metz in source: **2025-11-02, ATP Tour level, hard** | **Confirmed** |
| A July 2025 Metz **ITF event on clay** also exists | **Confirmed** — "Metz" alone does not identify an event |
| These fixtures are a **2026 ATP Challenger** at Metz | **NOT confirmed** — the source ends 2026-06-01 and contains no 2026 Metz record |
| The event is on **hard court** | **NOT confirmed by source** — accepted as the user's stated parameter |

**Consequence:** the hard-court filter is applied *because the user specified it*, not
because this study verified the event's surface. Nothing here should be read as a
verified characterisation of a 2026 Metz Challenger.

---

## 4. Sample construction

Exact normalised full-name matching (no fuzzy, no surname-only). Near-misses counted:
Gadamauri 5, Jianu 2, all others 0 — none material.

| | All surfaces | Hard only |
|---|---:|---:|
| Eligible completed matches | 5,560 | **2,690** |
| Best-of-3 hard-court matches | — | **2,675** |

Retirements, walkovers, defaults and unparsed scores excluded per player and itemised
in `outputs/name_matching_audit.csv` (e.g. Grenier 28 retirements, Jianu 32, Taberner 22).

Internal identity checks (`set1_won + set1_lost = n`; `straight + distance +
intermediate = n`) pass for all 21 player-format rows — **zero violations**, enforced by
runtime `assert`.

---

## 5. Hard-court set-structure profiles (best-of-3)

| Player | n | Straight sets | 95% CI | Distance (3 sets) | Tiebreak share |
|---|---:|---:|---|---:|---:|
| Hugo Grenier | 524 | 64.5% | 60.3–68.5 | 35.5% | 26.7% |
| Alibek Kachmazov | 278 | 65.5% | 59.7–70.8 | 34.5% | 25.9% |
| Cyril Vandermeersch | 218 | 66.5% | 60.0–72.4 | 33.5% | 22.9% |
| Luca Nardi | 201 | 63.2% | 56.3–69.5 | 36.8% | 27.9% |
| Ugo Blanchet | 192 | 68.8% | 61.9–74.9 | 31.2% | 27.6% |
| Alejandro Moro Canas | 147 | 57.8% | 49.7–65.5 | 42.2% | 30.6% |
| Jonas Forejtek | 136 | 69.9% | 61.7–76.9 | 30.1% | 23.5% |
| Florent Bax | 133 | 75.2% | 67.2–81.8 | 24.8% | 19.5% |
| Milos Karol | 117 | 68.4% | 59.5–76.1 | 31.6% | 44.4% |
| Buvaysar Gadamauri | 111 | 66.7% | 57.5–74.7 | 33.3% | 17.1% |
| Adrien Gobat | 111 | 76.6% | 67.9–83.5 | 23.4% | 26.1% |
| Robin Catry | 105 | 63.8% | 54.3–72.4 | 36.2% | 22.9% |
| Matthew William Donald | 101 | 76.2% | 67.1–83.5 | 23.8% | 19.8% |
| Filip Cristian Jianu | 87 | 70.1% | 59.8–78.7 | 29.9% | 21.8% |
| Carlos Taberner | 84 | 63.1% | 52.4–72.6 | 36.9% | 33.3% |
| Martin Krumich | 72 | 66.7% | 55.2–76.5 | 33.3% | 31.9% |
| Matisse Bobichon | 52 | 75.0% | 61.8–84.8 | 25.0% | 23.1% |
| **Lenny Couturier** | **6** | **83.3%** | **43.6–97.0** | **16.7%** | 33.3% |

Best-of-5 hard-court matches exist only in tiny numbers and are reported separately:
Nardi 4, Grenier 5, Blanchet 3, Taberner 3 — all flagged `insufficient`.

**Do not read Couturier's 83.3% as a finding.** It is 5 of 6 matches, with an interval
running from 43.6% to 97.0%. It conveys essentially nothing, which is exactly what the
interval is there to show.

---

## 6. Prior head-to-head meetings — 9 records

This is the most informative content in the study, and it is pure record, not inference.

| Pairing | Date | Level | Surface | Score |
|---|---|---|---|---|
| **Donald vs Krumich** | 2023-09-18 | ITF $25k | Clay | Krumich 6-1 6-3 |
| | 2025-09-22 | ITF $25k | Clay | Krumich 7-5 7-5 |
| | **2026-02-02** | **Challenger** | **Hard** | **Krumich 6-4 7-5** |
| **Vandermeersch vs Kachmazov** | 2025-03-10 | Challenger | Hard | Vandermeersch 7-5 6-3 |
| **Gadamauri vs Gobat** | 2025-04-21 | ITF $15k | Hard | Gadamauri 6-2 6-4 |
| **Jianu vs Taberner** | 2022-08-08 | Challenger | Clay | Jianu 6-4 6-3 |
| | 2022-09-05 | Challenger | Clay | Taberner 6-2 6-3 |
| | **2022-10-10** | ATP Tour | **Hard** | **Taberner 7-5 6-7(6) 7-6(5)** |
| | 2024-10-07 | Challenger | Clay | Taberner 6-2 7-6(3) |

Five of the nine pairings have **never met** in the recorded window.

Observation on the records themselves: **all nine meetings finished in straight sets
except one** — Jianu–Taberner on hard in 2022, which went to a third-set tiebreak. Note
that this is a description of nine specific past meetings. Nine matches is not a basis
for characterising a matchup, and the fact that both Donald–Krumich clay meetings were
straight-setters tells you nothing about a hard-court match between other players.

---

## 7. How much of each player's career the hard-court filter actually covers

This is essential context, because the filter cuts very unevenly:

| Player | All matches | Hard | Hard share |
|---|---:|---:|---:|
| Cyril Vandermeersch | 222 | 218 | **98.2%** |
| Robin Catry | 118 | 105 | 89.0% |
| Matisse Bobichon | 62 | 52 | 83.9% |
| Alibek Kachmazov | 335 | 278 | 83.0% |
| Hugo Grenier | 700 | 529 | 75.6% |
| Adrien Gobat | 151 | 111 | 73.5% |
| Luca Nardi | 335 | 205 | 61.2% |
| Ugo Blanchet | 357 | 195 | 54.6% |
| Matthew William Donald | 192 | 101 | 52.6% |
| Milos Karol | 244 | 117 | 48.0% |
| Alejandro Moro Canas | 320 | 147 | 45.9% |
| Florent Bax | 319 | 133 | 41.7% |
| Buvaysar Gadamauri | 289 | 111 | 38.4% |
| Jonas Forejtek | 366 | 136 | 37.2% |
| Martin Krumich | 332 | 72 | 21.7% |
| Filip Cristian Jianu | 542 | 87 | **16.1%** |
| Carlos Taberner | 668 | 87 | **13.0%** |

**For Jianu and Taberner, a "hard-court profile" describes about one match in seven.**
Both are overwhelmingly clay players (451 and 576 clay matches respectively). Their
hard-court rows in §5 are real, but they are a thin slice of two clay-dominated careers,
and the intervals are correspondingly wide. Conversely, Vandermeersch's 98.2% means his
hard-court figure is effectively his whole career.

---

## 8. Why these cannot become per-player probabilities

The same five objections as STUDY-002 apply, plus one specific to this study:

1. **Different opposition** in every match pooled.
2. **Different levels**: these totals mix ITF $15k, ITF $25k and Challenger at very
   different proportions per player.
3. **No opponent-interaction data** exists in the source.
4. **Non-random selection**: named fixtures, not a sample.
5. **The arithmetic doesn't close**: win-in-2, lose-in-2, win-in-3, lose-in-3 sum to 1
   and require P(match winner) plus P(straight sets | winner). Neither is derivable here.
6. **New to this study:** the hard-court filter means several players' figures rest on
   a minority of their career (§7), so even a descriptive hard-court rate is a
   partial-career statistic for them, not a settled one.

---

## 9. Limitations

1. Single tier-3 source; **no official ATP cross-check** was possible.
2. Coverage ends **2026-06-01** — roughly 5.5 months before the analysis date. This is
   history, not current form.
3. **Event level and surface unverified** (§3).
4. Uneven hard-court coverage (§7); Jianu and Taberner especially thin.
5. No opponent-quality adjustment.
6. Filters 7–8 unavailable (no set-level serve/return data).
7. Couturier (8 total matches) cannot be characterised at all.
8. Retirements excluded (up to 32 for Jianu); a player with many retirements has a
   slightly more selected "completed match" set.
9. Descriptive only; no causal claim, no player trait.

---

## 10. What this study cannot establish

- No prediction for any of the nine fixtures, on set count or winner.
- No per-player probability of winning or losing in two or three sets. Prohibited by
  `STUDY_SPECIFICATION.md` §12; CSVs carry a `NOT_A_PROBABILITY` column.
- No ranking of the 18 players.
- No statement about the 2026 Metz event's level, surface or field strength.

---

## 11. Reproducibility

```
python3 tools/study003_hardcourt.py --input-dir <dir> --out-dir studies/STUDY-003/outputs
cd tools && python3 -m unittest test_study001_pipeline -v    # 28 tests
```

Python 3.11.2, stdlib only. Shares the score parser (STUDY-001) and the
name/surface normalisers (STUDY-002) with the earlier studies, so all three read a score
string and a surface label identically. Runtime asserts enforce the two internal
identities before any CSV is written.

---

## 12. Neutral conclusion

Across **2,690 eligible hard-court matches** played by these 18 players between
2015-01-01 and 2026-06-01, straight-set shares in best-of-3 range from 57.8%
(Moro Canas, 147 matches) to 76.6% (Gobat, 111 matches), with wide intervals throughout
and one player (Couturier, 6 matches) too small to characterise.

Nine prior meetings exist among the nine pairings; five pairings have never met. All
nine recorded meetings finished in straight sets bar one three-setter.

The hard-court filter covers 98.2% of Vandermeersch's career and 13.0% of Taberner's,
so these figures describe very different proportions of each player's record. Nothing
in this study is a forecast, a probability or a ranking, and the data does not support
constructing one for any of the nine fixtures.
