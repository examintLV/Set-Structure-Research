#!/usr/bin/env python3
"""
STUDY-001 pipeline: ATP Challenger men's singles set structure, 2024-01-01..2026-06-01.

Implements exactly the frozen rules in studies/STUDY-001/STUDY_SPECIFICATION.md.
Standard library only (Python 3.11+), so results are reproducible without
third-party packages.

Usage:
    python3 tools/study001_pipeline.py --input-dir <dir with the 3 source CSVs> \
        --out-dir studies/STUDY-001/outputs

The raw source CSVs are NOT redistributed. Fetch them with the URLs recorded in
outputs/source_manifest.csv and verify the sha256 values before running.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import math
import os
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import date

# ----------------------------------------------------------------------------
# Frozen constants (spec sections 3-7)
# ----------------------------------------------------------------------------
WINDOW_START = date(2024, 1, 1)
WINDOW_END = date(2026, 6, 1)
LEVEL = "C"
BEST_OF = "3"
SURFACES = {"Hard", "Clay", "Grass"}

SOURCE_FILES = {
    2024: "atp_matches_qual_chall_2024.csv",
    2025: "atp_matches_qual_chall_2025.csv",
    2026: "atp_matches_qual_chall_2026.csv",
}
SOURCE_URL_TMPL = (
    "https://api.github.com/repos/Aneeshers/tennis-sackmann-archive/"
    "contents/atp/{fname}?ref=main"
)

MAIN_DRAW_ROUNDS = {"R32", "R16", "QF", "SF", "F"}
QUALIFYING_ROUNDS = {"Q1", "Q2"}

Z95 = 1.959963984540054


# ----------------------------------------------------------------------------
# Score parsing (spec section 6)
# ----------------------------------------------------------------------------
@dataclass
class Parsed:
    ok: bool
    status: str                      # completed | retired | walkover | default | abandoned | unparsed
    sets: list = field(default_factory=list)   # list of dicts
    n_conventional: int = 0
    has_match_tiebreak: bool = False
    reason: str = ""


SET_RE = re.compile(r"^(\d+)-(\d+)(?:\((\d+)\))?$")
BRACKET_RE = re.compile(r"^\[(\d+)-(\d+)\]$")

STATUS_PATTERNS = [
    ("walkover", ("W/O", "WO", "w/o")),
    ("default", ("DEF", "Def.", "def.")),
    ("abandoned", ("ABD", "Played and abandoned", "Played and unfinished", "Unfinished")),
    # "Ret'd" is a source spelling variant (1 level-C record); found by
    # enumerating status tokens across the frame, not guessed. Spec amendment A3.
    ("retired", ("RET", "Ret'd", "Ret.", "ret.")),
]


def _detect_status(score: str) -> tuple[str, str]:
    """Return (status, residual_score_string)."""
    s = score
    for status, tokens in STATUS_PATTERNS:
        for t in tokens:
            if t in s:
                return status, s.replace(t, " ")
    return "completed", s


def parse_score(score: str, best_of: int = 3) -> Parsed:
    """Parse a winner-perspective score string under the frozen grammar.

    `best_of` defaults to 3, preserving STUDY-001's original behaviour exactly
    (that population is 100% best-of-3). Pass 5 for best-of-5 events.

    Defect fixed 2026-11-15 (STUDY-002, amendment A1): this function previously
    hardcoded best-of-3 validation, so every best-of-5 match was rejected as
    unparseable. It never showed in STUDY-001 because that sample contains no
    best-of-5 matches.
    """
    if score is None or not str(score).strip():
        return Parsed(False, "unparsed", reason="empty score")
    raw = str(score).strip()
    status, residual = _detect_status(raw)

    tokens = [t for t in residual.split() if t]
    sets, has_mtb = [], False
    for tok in tokens:
        m = SET_RE.match(tok)
        if m:
            a, b = int(m.group(1)), int(m.group(2))
            tb_loser = int(m.group(3)) if m.group(3) is not None else None
            valid, why = _validate_conventional_set(a, b, tb_loser)
            if not valid:
                # Preserve the completed sets parsed so far: a retirement ends
                # mid-set, and its earlier completed sets are still real data
                # for the sensitivity analysis (spec amendment A4).
                n_done = sum(1 for s in sets if not s["is_match_tiebreak"])
                if status == "retired":
                    return Parsed(True, status, sets, n_done, has_mtb,
                                  reason=f"retirement, stops at incomplete set '{tok}'")
                return Parsed(False, status, reason=f"invalid set '{tok}': {why}")
            sets.append({
                "games_winner": a, "games_loser": b,
                "tiebreak": (a == 7 and b == 6),
                "tb_loser_points": tb_loser,
                "is_match_tiebreak": False,
            })
            continue
        mb = BRACKET_RE.match(tok)
        if mb:
            has_mtb = True
            sets.append({
                "games_winner": int(mb.group(1)), "games_loser": int(mb.group(2)),
                "tiebreak": False, "tb_loser_points": None, "is_match_tiebreak": True,
            })
            continue
        return Parsed(False, status, reason=f"unrecognised token '{tok}'", has_match_tiebreak=has_mtb)

    n_conv = sum(1 for s in sets if not s["is_match_tiebreak"])

    if status == "completed":
        if has_mtb:
            # A completed match containing a match tiebreak is not a
            # conventional-scoring match: excluded under E5.
            return Parsed(True, status, sets, n_conv, True,
                          reason="match tiebreak present")
        needed = (best_of + 1) // 2          # 2 for bo3, 3 for bo5
        if not (needed <= n_conv <= best_of):
            return Parsed(False, status, sets, n_conv, False,
                          reason=(f"completed best-of-{best_of} match with "
                                  f"{n_conv} conventional sets"))
        # structural check: winner must win exactly `needed` sets
        if _set_wins(sets) != (needed, n_conv - needed):
            return Parsed(False, status, sets, n_conv, False,
                          reason=f"set tally {_set_wins(sets)} inconsistent with score")
    return Parsed(True, status, sets, n_conv, has_mtb)


def _set_wins(sets) -> tuple[int, int]:
    w = sum(1 for s in sets if not s["is_match_tiebreak"] and s["games_winner"] > s["games_loser"])
    l = sum(1 for s in sets if not s["is_match_tiebreak"] and s["games_winner"] < s["games_loser"])
    return w, l


def _validate_conventional_set(a: int, b: int, tb_loser: int | None) -> tuple[bool, str]:
    """A conventional set is won to 6 (by 2) or 7 (tiebreak at 6-6, or 7-5)."""
    hi, lo = max(a, b), min(a, b)
    if a == b:
        return False, "tied games"
    if tb_loser is not None and not (hi == 7 and lo == 6):
        return False, "tiebreak points on a non 7-6 set"
    if hi == 6 and lo <= 4:
        return True, ""
    if hi == 7 and lo in (5, 6):
        if lo == 5 and tb_loser is not None:
            return False, "tiebreak points on 7-5 set"
        return True, ""
    # Frozen spec section 6: a conventional set winner has 6 or 7 games.
    # Extended sets (8-6 etc.) are out of grammar for this population and are
    # surfaced under E6 rather than silently accepted.
    return False, f"games {a}-{b} outside frozen grammar (winner games must be 6 or 7)"


# ----------------------------------------------------------------------------
# Statistics helpers
# ----------------------------------------------------------------------------
def wilson(k: int, n: int, z: float = Z95) -> tuple[float, float]:
    """95% Wilson score interval. Returns (low, high) as proportions."""
    if n <= 0:
        return (float("nan"), float("nan"))
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = (z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))


def pct(k: int, n: int) -> str:
    return f"{100.0 * k / n:.1f}%" if n else "n/a"


def fmt_rate(k: int, n: int) -> str:
    if n == 0:
        return "n/a (denominator 0)"
    lo, hi = wilson(k, n)
    return f"{pct(k, n)} [{100*lo:.1f}-{100*hi:.1f}]"


# ----------------------------------------------------------------------------
# Loading and eligibility
# ----------------------------------------------------------------------------
@dataclass
class Match:
    match_id: str
    year: int
    tourney_name: str
    tourney_id: str
    match_date: date
    surface: str
    round: str
    winner: str
    loser: str
    score: str
    minutes: str
    parsed: Parsed
    # derived
    set1_winner_is_match_winner: bool | None = None
    set_scores: list = field(default_factory=list)   # [(w_games, l_games, tb), ...]


def build_match_id(r: dict) -> str:
    """Stable composite key (spec: no stable source match id is supplied)."""
    return "|".join([r["tourney_id"], r["match_num"], r["winner_id"], r["loser_id"]])


def load_source(input_dir: str, manifest_rows: list) -> tuple[list[Match], dict]:
    """Load, filter to the frame, parse. Returns (matches, counters)."""
    counter = Counter()
    matches: list[Match] = []
    seen_ids = set()

    for year, fname in SOURCE_FILES.items():
        path = os.path.join(input_dir, fname)
        if not os.path.isfile(path):
            raise SystemExit(f"missing source file: {path}")
        sha = _sha256(path)
        manifest_rows.append({
            "file": fname,
            "url": SOURCE_URL_TMPL.format(fname=fname),
            "sha256": sha,
            "bytes": os.path.getsize(path),
            "retrieved_at_utc": "2026-11-15",
            "source_tier": "3-4 (specialist database mirror; not official tour records)",
        })
        with open(path, encoding="utf-8", newline="") as f:
            for r in csv.DictReader(f):
                counter["candidate_rows"] += 1
                if r["tourney_level"] != LEVEL:
                    counter["excl_not_challenger_level"] += 1
                    continue
                if r["best_of"] != BEST_OF:
                    counter["excl_not_best_of_3"] += 1
                    continue
                if r["surface"] not in SURFACES:
                    counter["excl_surface"] += 1
                    continue
                try:
                    d = date(int(r["tourney_date"][:4]), int(r["tourney_date"][4:6]),
                             int(r["tourney_date"][6:8]))
                except (ValueError, IndexError):
                    counter["excl_bad_date"] += 1
                    continue
                if not (WINDOW_START <= d <= WINDOW_END):
                    counter["excl_outside_window"] += 1
                    continue
                if not (r["score"] or "").strip():
                    counter["excl_empty_score"] += 1
                    continue

                mid = build_match_id(r)
                if mid in seen_ids:
                    counter["excl_duplicate_id"] += 1
                    continue
                seen_ids.add(mid)

                p = parse_score(r["score"])
                matches.append(Match(
                    match_id=mid, year=year, tourney_name=r["tourney_name"],
                    tourney_id=r["tourney_id"], match_date=d, surface=r["surface"],
                    round=r["round"], winner=r["winner_name"], loser=r["loser_name"],
                    score=r["score"], minutes=r.get("minutes", ""), parsed=p,
                ))
    return matches, counter


def _sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def classify(matches: list[Match]) -> tuple[list[Match], Counter, list[dict]]:
    """Apply exclusions E1-E6; return eligible primary sample + counters + items."""
    excl = Counter()
    dq_rows = []
    eligible = []

    for m in matches:
        p = m.parsed
        # Status is resolved BEFORE parse validity. A retirement such as
        # "6-1 2-1 RET" contains a legitimately partial set that must fail
        # conventional-set validation; it is an E1 retirement, not an E6
        # unparsed record. (Bug detected 2026-11-15 by inspecting exclusions;
        # see spec amendment A2.)
        if p.status == "walkover":
            excl["E2_walkover"] += 1
            dq_rows.append({"match_id": m.match_id, "score": m.score, "rule": "E2_walkover",
                            "reason": "no played structure", "tourney": m.tourney_name,
                            "date": m.match_date.isoformat()})
            continue
        if p.status == "default":
            excl["E3_default"] += 1
            dq_rows.append({"match_id": m.match_id, "score": m.score, "rule": "E3_default",
                            "reason": "default", "tourney": m.tourney_name,
                            "date": m.match_date.isoformat()})
            continue
        if p.status == "abandoned":
            excl["E4_abandoned"] += 1
            dq_rows.append({"match_id": m.match_id, "score": m.score, "rule": "E4_abandoned",
                            "reason": "abandoned / unfinished", "tourney": m.tourney_name,
                            "date": m.match_date.isoformat()})
            continue
        if p.status == "retired":
            excl["E1_retired"] += 1
            dq_rows.append({"match_id": m.match_id, "score": m.score, "rule": "E1_retired",
                            "reason": "retirement (used only in sensitivity check)",
                            "tourney": m.tourney_name, "date": m.match_date.isoformat()})
            continue
        if p.has_match_tiebreak:
            excl["E5_match_tiebreak"] += 1
            dq_rows.append({"match_id": m.match_id, "score": m.score,
                            "rule": "E5_match_tiebreak", "reason": "match tiebreak in lieu of set 3",
                            "tourney": m.tourney_name, "date": m.match_date.isoformat()})
            continue

        # Completed matches only from here: now parse validity is decisive.
        if not p.ok:
            excl["E6_unparsed"] += 1
            dq_rows.append({"match_id": m.match_id, "score": m.score,
                            "rule": "E6_unparsed", "reason": p.reason,
                            "tourney": m.tourney_name, "date": m.match_date.isoformat()})
            continue

        if not m.set_scores:
            m.set_scores = [(s["games_winner"], s["games_loser"], s["tiebreak"]) for s in p.sets]
        first = m.set_scores[0]
        m.set1_winner_is_match_winner = first[0] > first[1]
        eligible.append(m)

    return eligible, excl, dq_rows


# ----------------------------------------------------------------------------
# Analyses
# ----------------------------------------------------------------------------
def structure_counts(ms: list[Match]) -> dict:
    c = Counter(len(m.set_scores) for m in ms)
    return dict(c)


def write_csv(path: str, rows: list[dict], fieldnames: list[str]):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def analyse(ms: list[Match], outdir: str):
    outputs = {}

    # ---- Filter 1: structure distribution, overall + strata
    rows = []
    def add_structure(label, subset):
        c = structure_counts(subset)
        n = len(subset)
        two, three = c.get(2, 0), c.get(3, 0)
        rows.append({
            "stratum": label, "n_matches": n,
            "two_set_n": two, "three_set_n": three,
            "two_set_share": pct(two, n), "two_set_95ci": _ci(two, n),
            "three_set_share": pct(three, n), "three_set_95ci": _ci(three, n),
        })

    add_structure("ALL eligible", ms)
    for s in ("Hard", "Clay", "Grass"):
        add_structure(f"surface={s}", [m for m in ms if m.surface == s])
    for y in (2024, 2025, 2026):
        add_structure(f"season={y}", [m for m in ms if m.year == y])
    for rnd in ("R32", "R16", "QF", "SF", "F", "Q1", "Q2"):
        add_structure(f"round={rnd}", [m for m in ms if m.round == rnd])
    add_structure("main draw only", [m for m in ms if m.round in MAIN_DRAW_ROUNDS])
    add_structure("qualifying only", [m for m in ms if m.round in QUALIFYING_ROUNDS])
    write_csv(f"{outdir}/f1_structure_distribution.csv", rows,
              ["stratum", "n_matches", "two_set_n", "three_set_n",
               "two_set_share", "two_set_95ci", "three_set_share", "three_set_95ci"])
    outputs["f1"] = rows

    # ---- Filter 2: first-set context
    n = len(ms)
    fsw = sum(1 for m in ms if m.set1_winner_is_match_winner)
    fsl = n - fsw
    # set 1 margin distribution (winner perspective doesn't matter for |margin|)
    # Set 1 may be won by the player who ultimately LOSES the match, so the
    # signed difference is not a margin. Report absolute margin, and use the
    # sign purely as an internal reconciliation check against the comeback
    # count (spec amendment A6).
    margins = Counter()
    signed = Counter()
    s1_tb = 0
    for m in ms:
        w, l, tb = m.set_scores[0]
        margins[abs(w - l)] += 1
        signed[w - l] += 1
        if tb:
            s1_tb += 1
    # reconciliation: set-1 losses by the match winner must equal comebacks
    comebacks_from_signed = sum(v for k, v in signed.items() if k < 0)
    assert comebacks_from_signed == (n - fsw), (
        f"reconciliation failed: signed negatives {comebacks_from_signed} "
        f"vs comebacks {n - fsw}")
    rows2 = [
        {"measure": "set1 winner won match", "numerator": fsw, "denominator": n,
         "rate": pct(fsw, n), "ci95": _ci(fsw, n)},
        {"measure": "set1 loser won match (comeback)", "numerator": fsl, "denominator": n,
         "rate": pct(fsl, n), "ci95": _ci(fsl, n)},
        {"measure": "set1 was a tiebreak", "numerator": s1_tb, "denominator": n,
         "rate": pct(s1_tb, n), "ci95": _ci(s1_tb, n)},
    ]
    write_csv(f"{outdir}/f2_first_set_context.csv", rows2,
              ["measure", "numerator", "denominator", "rate", "ci95"])

    rows2b = [{"abs_game_margin": mg, "n": c, "share": pct(c, n)}
              for mg, c in sorted(margins.items())]
    write_csv(f"{outdir}/f2_set1_margin_distribution.csv", rows2b,
              ["abs_game_margin", "n", "share"])

    # ---- Filter 2b: does a first-set tiebreak relate to match length?
    # Conditional rates, stated in the correct direction. Note that
    # P(set1 TB | 3 sets) is NOT the same quantity as P(3 sets | set1 TB);
    # both are reported explicitly to prevent that inversion.
    tb1 = [m for m in ms if m.set_scores[0][2]]
    nb1 = [m for m in ms if not m.set_scores[0][2]]
    tb1_3 = [m for m in tb1 if len(m.set_scores) == 3]
    nb1_3 = [m for m in nb1 if len(m.set_scores) == 3]
    rows2c = [
        {"measure": "P(3 sets | set1 was a tiebreak)",
         "numerator": len(tb1_3), "denominator": len(tb1),
         "rate": pct(len(tb1_3), len(tb1)), "ci95": _ci(len(tb1_3), len(tb1))},
        {"measure": "P(3 sets | set1 was NOT a tiebreak)",
         "numerator": len(nb1_3), "denominator": len(nb1),
         "rate": pct(len(nb1_3), len(nb1)), "ci95": _ci(len(nb1_3), len(nb1))},
        {"measure": "P(set1 was a tiebreak | 3 sets)  [inverse direction]",
         "numerator": len(tb1_3),
         "denominator": len(tb1_3) + len(nb1_3),
         "rate": pct(len(tb1_3), len(tb1_3) + len(nb1_3)),
         "ci95": _ci(len(tb1_3), len(tb1_3) + len(nb1_3))},
    ]
    write_csv(f"{outdir}/f2b_set1_tiebreak_and_length.csv", rows2c,
              ["measure", "numerator", "denominator", "rate", "ci95"])
    outputs["f2c"] = rows2c

    # ---- Filter 5: competitiveness by set position
    rows5 = []
    for pos in (1, 2, 3):
        tot_games, diffs, tbs, n_sets = [], [], 0, 0
        matches_with = 0
        for m in ms:
            if len(m.set_scores) >= pos:
                w, l, tb = m.set_scores[pos - 1]
                tot_games.append(w + l)
                diffs.append(abs(w - l))
                n_sets += 1
                matches_with += 1
                if tb:
                    tbs += 1
        if n_sets:
            rows5.append({
                "set_position": pos, "n_sets": n_sets,
                "contributing_matches": matches_with,
                "mean_total_games": f"{sum(tot_games)/n_sets:.2f}",
                "median_total_games": _median(tot_games),
                "mean_abs_margin": f"{sum(diffs)/n_sets:.2f}",
                "median_abs_margin": _median(diffs),
                "tiebreak_sets": tbs,
                "tiebreak_set_share": pct(tbs, n_sets),
                "tiebreak_95ci": _ci(tbs, n_sets),
            })
    write_csv(f"{outdir}/f5_competitiveness_by_set_position.csv", rows5,
              ["set_position", "n_sets", "contributing_matches", "mean_total_games",
               "median_total_games", "mean_abs_margin", "median_abs_margin",
               "tiebreak_sets", "tiebreak_set_share", "tiebreak_95ci"])
    outputs["f5"] = rows5

    # ---- Filter 6: tiebreaks
    total_sets = sum(len(m.set_scores) for m in ms)
    tb_sets = sum(1 for m in ms for (_, _, tb) in m.set_scores if tb)
    matches_any_tb = sum(1 for m in ms if any(tb for (_, _, tb) in m.set_scores))
    rows6 = [
        {"measure": "tiebreak sets / conventional sets", "numerator": tb_sets,
         "denominator": total_sets, "rate": pct(tb_sets, total_sets), "ci95": _ci(tb_sets, total_sets)},
        {"measure": "matches with >=1 tiebreak / matches", "numerator": matches_any_tb,
         "denominator": n, "rate": pct(matches_any_tb, n), "ci95": _ci(matches_any_tb, n)},
    ]
    for s in ("Hard", "Clay", "Grass"):
        sub = [m for m in ms if m.surface == s]
        st = sum(len(m.set_scores) for m in sub)
        tbs = sum(1 for m in sub for (_, _, tb) in m.set_scores if tb)
        mats = sum(1 for m in sub if any(tb for (_, _, tb) in m.set_scores))
        rows6.append({"measure": f"surface={s}: tiebreak sets / sets", "numerator": tbs,
                      "denominator": st, "rate": pct(tbs, st), "ci95": _ci(tbs, st)})
        rows6.append({"measure": f"surface={s}: matches with >=1 TB / matches",
                      "numerator": mats, "denominator": len(sub),
                      "rate": pct(mats, len(sub)), "ci95": _ci(mats, len(sub))})
    write_csv(f"{outdir}/f6_tiebreaks.csv", rows6,
              ["measure", "numerator", "denominator", "rate", "ci95"])
    outputs["f6"] = rows6

    # ---- Filter 9: deciding sets
    three_setters = [m for m in ms if len(m.set_scores) == 3]
    n3 = len(three_setters)
    dec_tb = sum(1 for m in three_setters if m.set_scores[2][2])
    dec_margins = Counter(abs(m.set_scores[2][0] - m.set_scores[2][1]) for m in three_setters)
    dec_scores = Counter(
        f"{max(m.set_scores[2][0], m.set_scores[2][1])}-{min(m.set_scores[2][0], m.set_scores[2][1])}"
        for m in three_setters)
    rows9 = [{"measure": "deciding sets that were tiebreaks", "numerator": dec_tb,
              "denominator": n3, "rate": pct(dec_tb, n3), "ci95": _ci(dec_tb, n3)}]
    write_csv(f"{outdir}/f9_deciding_set_summary.csv", rows9,
              ["measure", "numerator", "denominator", "rate", "ci95"])
    write_csv(f"{outdir}/f9_deciding_set_margins.csv",
              [{"abs_game_margin": k, "n": v, "share": pct(v, n3)}
               for k, v in sorted(dec_margins.items())],
              ["abs_game_margin", "n", "share"])
    write_csv(f"{outdir}/f9_deciding_set_scores.csv",
              [{"scoreline": k, "n": v, "share": pct(v, n3)}
               for k, v in dec_scores.most_common()],
              ["scoreline", "n", "share"])
    outputs["f9"] = rows9

    # ---- Completeness
    comp = []
    for fname, key in (("minutes", "minutes"), ("w_svpt", "serve totals")):
        pass  # handled by caller with raw rows
    return outputs


def _median(xs):
    if not xs:
        return "n/a"
    s = sorted(xs)
    n = len(s)
    mid = n // 2
    return f"{s[mid]:.1f}" if n % 2 else f"{(s[mid-1]+s[mid])/2:.1f}"


def _ci(k: int, n: int) -> str:
    if n == 0:
        return "n/a"
    lo, hi = wilson(k, n)
    return f"{100*lo:.1f}-{100*hi:.1f}%"


# ----------------------------------------------------------------------------
def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", required=True)
    ap.add_argument("--out-dir", default="studies/STUDY-001/outputs")
    args = ap.parse_args(argv)

    manifest: list[dict] = []
    matches, counter = load_source(args.input_dir, manifest)
    eligible, excl, dq = classify(matches)

    os.makedirs(args.out_dir, exist_ok=True)
    write_csv(f"{args.out_dir}/source_manifest.csv", manifest,
              ["file", "url", "sha256", "bytes", "retrieved_at_utc", "source_tier"])
    write_csv(f"{args.out_dir}/data_quality_exclusions.csv", dq,
              ["match_id", "score", "rule", "reason", "tourney", "date"])

    # sample construction waterfall
    waterfall = [
        {"stage": "candidate rows", "n": counter["candidate_rows"]},
        {"stage": "excluded: not level C", "n": counter["excl_not_challenger_level"]},
        {"stage": "excluded: not best-of-3", "n": counter["excl_not_best_of_3"]},
        {"stage": "excluded: surface", "n": counter["excl_surface"]},
        {"stage": "excluded: bad date", "n": counter["excl_bad_date"]},
        {"stage": "excluded: outside window", "n": counter["excl_outside_window"]},
        {"stage": "excluded: empty score", "n": counter["excl_empty_score"]},
        {"stage": "excluded: duplicate id", "n": counter["excl_duplicate_id"]},
        {"stage": "in-frame records", "n": len(matches)},
        {"stage": "excluded E1 retirement", "n": excl["E1_retired"]},
        {"stage": "excluded E2 walkover", "n": excl["E2_walkover"]},
        {"stage": "excluded E3 default", "n": excl["E3_default"]},
        {"stage": "excluded E4 abandoned", "n": excl["E4_abandoned"]},
        {"stage": "excluded E5 match tiebreak", "n": excl["E5_match_tiebreak"]},
        {"stage": "excluded E6 unparsed", "n": excl["E6_unparsed"]},
        {"stage": "ELIGIBLE COMPLETED MATCHES", "n": len(eligible)},
    ]
    write_csv(f"{args.out_dir}/sample_construction.csv", waterfall, ["stage", "n"])

    analyse(eligible, args.out_dir)

    # ---- sensitivity checks
    sens = []
    def sens_row(label, subset, note=""):
        c = structure_counts(subset); nn = len(subset)
        two, three = c.get(2, 0), c.get(3, 0)
        sens.append({"check": label, "n": nn, "two_set_n": two, "three_set_n": three,
                     "two_set_share": pct(two, nn), "three_set_share": pct(three, nn),
                     "note": note})
    sens_row("primary (retirements excluded)", eligible)
    sens_row("main draw only", [m for m in eligible if m.round in MAIN_DRAW_ROUNDS])
    sens_row("qualifying only", [m for m in eligible if m.round in QUALIFYING_ROUNDS])
    sens_row("excluding 2026 (partial season)", [m for m in eligible if m.year != 2026])
    sens_row("2024 only", [m for m in eligible if m.year == 2024])
    sens_row("2025 only", [m for m in eligible if m.year == 2025])
    # Retirement handling. A retirement cannot enter a 2-vs-3-set
    # distribution: it has no final set count by construction. What IS
    # informative is how far retirements had progressed, because that
    # describes the excluded records rather than pretending to fold them in.
    rets = [m for m in matches if m.parsed.status == "retired"]
    usable = _retired_as_matches(rets)
    dist = Counter(len(m.set_scores) for m in usable)
    sens.append({
        "check": "retirements: distribution of completed sets at retirement",
        "n": len(usable),
        "two_set_n": dist.get(2, 0),
        "three_set_n": dist.get(3, 0),
        "two_set_share": pct(dist.get(2, 0), len(usable)),
        "three_set_share": pct(dist.get(3, 0), len(usable)),
        "note": (f"{len(rets)} retirements excluded from primary; "
                 f"{len(usable)} had >=1 completed set; "
                 f"{len(rets)-len(usable)} ended in set 1. "
                 "Shares here are of RETIREMENTS, not of matches."),
    })
    write_csv(f"{args.out_dir}/sensitivity_checks.csv", sens,
              ["check", "n", "two_set_n", "three_set_n", "two_set_share",
               "three_set_share", "note"])

    print(f"candidate rows            : {counter['candidate_rows']}")
    print(f"in-frame records          : {len(matches)}")
    print(f"excluded E1 retirement    : {excl['E1_retired']}")
    print(f"excluded E2 walkover      : {excl['E2_walkover']}")
    print(f"excluded E3 default       : {excl['E3_default']}")
    print(f"excluded E4 abandoned     : {excl['E4_abandoned']}")
    print(f"excluded E5 match TB      : {excl['E5_match_tiebreak']}")
    print(f"excluded E6 unparsed      : {excl['E6_unparsed']}")
    print(f"ELIGIBLE                  : {len(eligible)}")
    print(f"outputs written to        : {args.out_dir}")


def _retired_as_matches(ret_matches: list[Match]) -> list[Match]:
    """Retirement rows contribute only their *completed* conventional sets."""
    out = []
    for m in ret_matches:
        complete = []
        for s in m.parsed.sets:
            if s["is_match_tiebreak"]:
                continue
            w, l = s["games_winner"], s["games_loser"]
            if (max(w, l) == 6 and min(w, l) <= 4) or (max(w, l) == 7 and min(w, l) in (5, 6)):
                complete.append((w, l, s["tiebreak"]))
            else:
                break   # incomplete set: stop at first unfinished set
        if len(complete) >= 1:
            m.set_scores = complete
            out.append(m)
    return out


if __name__ == "__main__":
    main()
