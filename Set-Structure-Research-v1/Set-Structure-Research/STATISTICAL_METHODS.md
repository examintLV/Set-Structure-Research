# Statistical Methods and Interpretation

## Descriptive first
Begin with counts, denominators, distributions, and missingness. Do not use complex models when sample size or measurement quality cannot support them.

## Denominators
Every rate needs a numerator and denominator. Examples:
- Matches with three conventional sets / eligible completed matches.
- Tiebreak sets / eligible conventional sets.
- Matches with at least one tiebreak / eligible matches.
- Break points converted / break points earned.
- Service games won / service games played.

Do not include records where the field was unobserved in a denominator.

## Uncertainty
For proportions, consider Wilson confidence intervals rather than relying only on normal approximations, especially with small n or extreme proportions. State method and confidence level. Intervals do not correct selection bias. For means, report n and standard deviation; for skewed data, also report median and interquartile range.

## Dependence
Sets within a match are not independent. Two players' records from one match are not independent. Use match-clustered methods or match-level aggregation where appropriate. Do not inflate n by counting every set or player as an independent match.

## Stratification and confounding
Predefine tour, level, surface, format, season, and draw type. Show group sizes. Consider format, player/opponent ability, event round, scoring rules, status, and source coverage. Cross-tabs are not adjusted analyses. If regression is used, state model, covariates, missing-data handling, diagnostics, and limitations.

## Multiple comparisons and small samples
Ten filters plus subgroup analyses create opportunities for chance findings. Predefine primary outcomes; label exploratory findings and seek replication. There is no universal minimum n for all analyses: report actual n and uncertainty. Avoid stable player-trait claims from small samples.

## Missing data
Show missingness by field and subgroup. Do not impute scores or set-level stats in primary descriptive analysis.

## Historical rankings
Use a ranking snapshot tied to match date and cite its source. Current ranking is not historical ranking; ranking is an imperfect proxy for opponent strength.

## Language
Use “in this sample,” “observed,” “descriptive,” and “associated.” Avoid “always,” “proves,” “will,” and “guarantees.”

## No prospective conversion
Do not convert historical distributions into upcoming-match probabilities, exact-set forecasts, confidence ratings, or picks. No betting-market data is a feature, baseline, target, or validation signal.
