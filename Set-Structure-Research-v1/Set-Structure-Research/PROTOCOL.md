# Research Protocol

## 1. Register the study before extraction
Record study ID, protocol version, question, tour/level, discipline, date range, surface, indoor/outdoor status, match formats, inclusion/exclusion criteria, primary and secondary outcomes, status handling, sources, and planned analyses. Do not change primary definitions after viewing results without a dated amendment.

## 2. Define the population
The default unit is one completed match. Define the target population precisely, for example: men's singles main-draw ATP matches, best-of-three, outdoor hard court, within a specified date window. This is a sample definition, not a universal population.

Keep separate:
- Main draw and qualifying.
- ATP, WTA, Challenger, ITF, and other event tiers.
- Singles, doubles, and mixed.
- Best-of-three and best-of-five.
- Standard sets and match-tiebreak formats.
- Indoor and outdoor, where known.

## 3. Eligibility and match status
For the primary sample, use completed matches with identifiable final results and set scores. Exclude walkovers because no played match structure exists. Record retirements separately and normally exclude them from the primary full-match structure distribution; add a clearly labelled sensitivity analysis if appropriate. Keep defaults and abandoned matches separate. Never silently discard records.

## 4. Extraction
For every match:
1. Assign a stable match ID.
2. Capture event, date, tour/level, round, players, surface, conditions, and format.
3. Capture result, status, and every set score in order.
4. Capture tiebreak scores and set-level stats only when explicitly supplied.
5. Save source name, direct URL or stable ID, retrieval timestamp, and extraction method.
6. Preserve raw source values separately from cleaned values.
7. Mark missing fields explicitly.

Never infer a set score from an incomplete summary. Never allocate match-level statistics across sets and label them set-level.

## 5. Cleaning
- Standardise player and event names while retaining raw spellings.
- Use ISO dates; retain source timezone for timestamps.
- Use controlled surface categories: clay, hard, grass, carpet, unknown.
- Validate set scores against the applicable format.
- Detect duplicates using event, date, players, round, and score; review collisions manually.
- Keep match tiebreaks distinct from conventional sets.
- Store counts and denominators, not percentages alone.
- Distinguish zero from missing.
- Preserve correction history.

## 6. Analysis order
1. Describe sample construction and completeness.
2. Report historical match-structure distribution.
3. Analyse first-set context.
4. Analyse set competitiveness.
5. Analyse tiebreaks.
6. Analyse service and return only where set-level data supports it.
7. Analyse deciding sets.
8. Stratify by surface and competition context.
9. Run sensitivity checks.
10. Write limitations before final conclusions.

## 7. Comparability
Consider format, tour, level, surface, discipline, draw type, time period, scoring-rule changes, match status, and source coverage. Historical rankings may be used only with a documented ranking snapshot tied to the match date. Current rankings are not historical rankings.

## 8. Missing data
Report field-level completeness and whether missingness clusters by tour, year, surface, or source. Do not impute scores or set-level stats for primary descriptive analysis. If an exploratory imputation is ever used, label it separately and compare it with observed records.

## 9. Sensitivity checks
Where sample size allows, repeat core summaries:
- With and without retirements.
- Main draw only versus qualifying included.
- Tours and levels separately.
- Surfaces separately.
- Alternative predeclared date windows.
- Excluding uncertain or incomplete records.
- Primary-source-only versus cross-checked samples.

## 10. Archive
Save study specification, source manifest, compliant dataset or reference, analysis code, outputs, report, quality checklist, software versions, commit hash, and dataset fingerprint. Never overwrite raw data; corrections create a new version.
