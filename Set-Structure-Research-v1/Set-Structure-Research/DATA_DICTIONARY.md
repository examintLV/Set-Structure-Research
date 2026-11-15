# Data Dictionary

Keep raw source values and cleaned values separately. Prefer relational tables: `matches.csv` (one row per match), `sets.csv` (one row per set), `player_set_stats.csv` (one row per player per set), `sources.csv`, and append-only `corrections.csv`.

## Match metadata
| Field | Meaning |
|---|---|
| match_id | Stable project match identifier |
| source_match_id | Source's own record ID |
| event_name / event_id | Event label and stable ID |
| match_date | Local match date, YYYY-MM-DD |
| match_datetime | ISO 8601 timestamp with timezone if known |
| tour | ATP, WTA, CHALLENGER, ITF, OTHER |
| event_level / draw_type / round | Explicit competition context |
| discipline | singles, doubles, mixed, other |
| surface | clay, hard, grass, carpet, unknown |
| indoor_outdoor | indoor, outdoor, unknown |
| match_format | best-of-three, best-of-five, match-tiebreak format, other |
| player_a_id / player_b_id | Stable player identifiers |
| player_a_name_raw / player_b_name_raw | Original source spellings |
| player_a_name_std / player_b_name_std | Standardised display names |
| status | completed, retired, walkover, default, abandoned, unknown |
| winner_id | Official winner ID, if applicable |
| total_sets_played | Conventional sets played |
| match_tiebreak_used | Whether a match tiebreak replaced a set |

## Set-level fields (one row per set)
| Field | Meaning |
|---|---|
| set_index | Set order, starting at 1 |
| player_a_games / player_b_games | Games won in that set |
| set_winner_id | Set winner |
| tiebreak_played | Conventional tiebreak occurred |
| tiebreak_score_a / tiebreak_score_b | Tiebreak points, if sourced |
| set_is_match_tiebreak | Match tiebreak, not conventional set |
| set_duration_minutes | Directly sourced duration only |
| set_status | completed, retired, abandoned, unknown |

## Player-set performance fields
Store integer counts as source of truth:
- `service_points`
- `first_serves_in`
- `first_serve_points_won`
- `second_serve_points_won`
- `aces`, `double_faults`
- `service_games`, `service_games_won`
- `break_points_faced`, `break_points_saved`
- `return_points`
- `first_serve_return_points_won`, `second_serve_return_points_won`
- `return_games`, `return_games_won`
- `break_points_earned`, `break_points_converted`

## Provenance
Record `source_name`, direct `source_url`, `source_record_id`, `retrieved_at`, `extraction_method`, `extracted_by`, `source_quality`, `verification_status`, and notes.

## Missingness
- `null` means unavailable, not recorded, or not applicable; record the reason when possible.
- Zero is an observed zero only when explicitly supported by the source.
- Never replace missing values with zero.
- Never report 0% when denominator is zero or missing.

## Derived metrics
- Total games in set = games by A + games by B.
- Game differential = A games − B games; report absolute value separately if useful.
- Tiebreak-set share = tiebreak sets / eligible conventional sets.
- Match-with-tiebreak share = matches with ≥1 conventional tiebreak / eligible matches.
- First-serve-in rate = first serves in / service points, only when scopes match.
- First-serve points-won rate = first-serve points won / first serves in.
- Service-games-won rate = service games won / service games played.
- Break-point conversion = converted / earned.
- Break-point save rate = saved / faced.

Store percentages as derived displays, never as the only data.
