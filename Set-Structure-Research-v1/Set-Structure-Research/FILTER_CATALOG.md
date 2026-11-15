# Filter Catalog: Ten Core Dimensions

For every filter, report status, sample size, available fields, missingness, definitions, results, uncertainty, confounders, and reasons for non-analysis.

## 1 — Historical match-structure distribution
**Question:** How many eligible completed matches ended after each number of conventional sets?

**Required:** match ID, status, format, conventional set count, match-tiebreak flag.

**Outputs:** counts and shares by set count; denominators; stratification by tour, level, surface, format, and period where sample sizes allow.

**Rules:** Do not combine best-of-three and best-of-five. A match tiebreak is not an ordinary set. Exclude walkovers from played-match distributions and report retirements separately.

## 2 — First-set outcome context
**Question:** How does final match structure differ descriptively according to who won set one?

**Required:** first-set score/winner, final winner, final set count, status.

**Outputs:** contingency tables of first-set winner identity against final winner and set count. Optionally stratify by predeclared first-set margin categories.

**Rules:** Keep player identity consistent across rows. State whether each row is indexed by first-set winner or eventual match winner. Separate retirements.

## 3 — After winning the first set
**Question:** Among eligible completed matches where a player won set one, what happened in subsequent sets?

**Outputs:** subsequent set score distributions, final winner identity, and match completion structure, with exact denominators.

**Rules:** Do not count both players as independent match observations without accounting for within-match dependence. This is a retrospective conditional description, not a forecast.

## 4 — After losing the first set
**Question:** Among eligible completed matches where a player lost set one, what was observed afterwards?

**Outputs:** comeback counts, final winner identity, subsequent set scores, and completion structure.

**Rules:** Define “comeback” as losing set one and ultimately winning the match. Separate retirements. Do not infer a stable “comeback ability” from small or biased samples.

## 5 — Set competitiveness
**Question:** How close were individual sets, and did observed competitiveness differ by set position?

**Metrics:** games won by each player, absolute game differential, total games, scoreline categories, tiebreak occurrence, set position.

**Rules:** Define categories before analysis. More games does not automatically mean a closer or higher-quality set. Keep tiebreak points distinct from games if the source reports them.

## 6 — Tiebreak structure
**Question:** How often did tiebreaks occur, in which set positions, and what outcomes were recorded?

**Outputs:** tiebreak sets / eligible conventional sets; matches with at least one tiebreak / eligible matches; tiebreaks by set position; score summaries when sourced.

**Rules:** The denominator for a set-level rate is sets; for a match-level rate it is matches. Separate match tiebreaks from conventional set tiebreaks. Do not claim clutch ability from small counts.

## 7 — Serve performance by set
**Potential fields:** service points, first serves in, first-serve points won, second-serve points won, aces, double faults, service games, service games won, break points faced/saved.

**Outputs:** counts and denominators by set; rates only where denominators are valid; within-match changes only when comparable set-level data exists.

**Rules:** Service games won and service points won are different measures. Aces are not first-serve percentage. Do not derive set values from match totals. Account for opponent and surface context.

## 8 — Return performance by set
**Potential fields:** return points, first-serve return points won, second-serve return points won, return games, return games won, break points earned/converted.

**Outputs:** counts, denominators, rates, and within-match changes where directly supported.

**Rules:** Break-point conversion = converted chances / chances earned. Distinguish return points from return games. Do not back-calculate absent set-level data.

## 9 — Deciding-set structure
**Question:** In matches that reached a deciding set, what scores and performance indicators were observed?

**Outputs:** deciding-set scores, total games, game margins, tiebreak occurrence, service/return stats if available.

**Rules:** Only matches reaching a deciding set enter the denominator. Separate best-of-three and best-of-five. Avoid small-sample claims about temperament or pressure.

## 10 — Surface and competition context
**Context:** surface, indoor/outdoor, tour, event level, singles/doubles, format, round, season, and verified environmental conditions.

**Outputs:** stratified tables with group sizes and completeness.

**Rules:** Do not infer indoor/outdoor from event name if conditions vary. Avoid tiny subgroups. Context is a possible confounder, not an explanation by itself.

## Optional secondary filters
Use only when the question is registered and reliable data exists:
- Match duration and time between sets.
- Timing/sequence of service breaks.
- Explicitly defined set-to-set score sequences (not psychological “momentum” claims).
- Historical ranking/seed difference.
- Rest days and schedule density from verified match dates.
- Weather, altitude, and environmental conditions from attributable records.
- Recorded medical timeouts or retirements (do not diagnose).
- Verified handedness matchup.
- Age at match date computed from verified birth date.

## Filter status vocabulary
- **Analysed:** data and method support the planned analysis.
- **Unavailable:** necessary records do not exist or cannot be accessed.
- **Not applicable:** filter does not apply to the defined sample.
- **Excluded:** deliberately excluded under a predeclared rule; explain why.
