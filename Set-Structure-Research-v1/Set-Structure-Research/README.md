# Set Structure Research

A reproducible framework for retrospective analysis of **completed tennis matches**. It studies how matches unfold across sets: match length, first-set context, set competitiveness, tiebreaks, set-level service/return performance, deciding sets, and differences by surface and competition context.

This is a research repository, not a match-picking system.

## Non-negotiable scope
- Completed matches only.
- Describe historical observations; do not forecast upcoming match structure.
- No betting advice, gambling markets, staking, or market selection.
- Never collect, store, cite, infer, or use sportsbook odds, bookmaker prices, betting-exchange prices, implied probabilities, or market-derived predictions.
- Never convert historical set frequencies into future-match probabilities.
- Preserve uncertainty, sample sizes, source provenance, missingness, and contradictory evidence.
- Never fabricate statistics or replace missing values with invented estimates.

## Start here
1. `RESEARCH_CHARTER.md`
2. `PROTOCOL.md`
3. `FILTER_CATALOG.md`
4. `DATA_DICTIONARY.md` and `DATA_SCHEMA.json`
5. `SOURCE_STANDARDS.md` and `DATA_COLLECTION_SOP.md`
6. `STATISTICAL_METHODS.md` and `ANALYSIS_PLAYBOOK.md`
7. `REPORT_TEMPLATE.md`
8. `QUALITY_CONTROL.md`
9. `AGENTS.md`

## Repository map
| File | Purpose |
|---|---|
| `RESEARCH_CHARTER.md` | Scope, questions, principles, prohibited inputs |
| `PROTOCOL.md` | End-to-end study design |
| `FILTER_CATALOG.md` | Ten detailed filters and optional extensions |
| `DATA_DICTIONARY.md` | Field definitions, denominators, missingness |
| `DATA_SCHEMA.json` | Canonical JSON record schema |
| `SOURCE_STANDARDS.md` | Source hierarchy and citation rules |
| `DATA_COLLECTION_SOP.md` | Extraction, cleaning, verification, provenance |
| `STATISTICAL_METHODS.md` | Descriptive statistics and uncertainty |
| `ANALYSIS_PLAYBOOK.md` | Standard analysis sequence and tables |
| `REPORT_TEMPLATE.md` | Required report structure |
| `QUALITY_CONTROL.md` | Data, analysis, AI, and release audits |
| `AGENTS.md` | Instructions for AI agents |
| `templates/` | Study, extraction, and correction logs |
| `tools/` | Structural validation utility and tests |

Every report must state its population, time window, format, surface, sample size, denominators, data sources, protocol version, and limitations.
