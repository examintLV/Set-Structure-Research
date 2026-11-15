# Data Collection Standard Operating Procedure

1. **Freeze scope.** Write study ID, date window, tours, levels, discipline, format, surface, and status rules before searching.
2. **Build the universe.** Use official draws/results or a reputable database. Record how the match list was assembled. Do not select matches because their scorelines look interesting.
3. **Assign IDs and deduplicate.** Prefer stable source IDs. Otherwise use a documented composite key from event, date, round, players, and draw. Review collisions manually.
4. **Capture raw facts.** Save metadata, status, winner, all set scores, tiebreak markers, directly sourced set-level stats, source URL/ID, and retrieval time.
5. **Do not fabricate set stats.** If only match totals exist, keep them separate or omit from set-level analysis. Never distribute totals across sets.
6. **Verify anomalies.** Flag implausible scores, set-winner conflicts, duplicate IDs, missing format/surface, tiebreak inconsistencies, match tiebreaks stored as ordinary sets, and status conflicts.
7. **Standardise.** Use controlled categories; retain raw names; do not guess unknown fields.
8. **Audit missingness.** Measure completeness by tour, level, year, surface, and source.
9. **Freeze dataset.** Save a versioned export, row counts, extraction dates, file hashes, schema version, and repository commit.
10. **Maintain corrections.** Record match ID, field, old/new value, reason, evidence URL, reviewer, and date. Never silently erase the original extraction.
