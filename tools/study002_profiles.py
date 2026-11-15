#!/usr/bin/env python3
"""
STUDY-002 pipeline: descriptive historical profiles for 18 named players.

Reuses the frozen score grammar and Wilson implementation from
study001_pipeline, so the two studies cannot drift apart in how they
interpret a score string.

This produces DESCRIPTIVE HISTORY ONLY. It deliberately emits no
probability, forecast, verdict or cross-player comparison. See
studies/STUDY-002/STUDY_SPECIFICATION.md section 12.

Usage:
    python3 tools/study002_profiles.py --input-dir /tmp/p2 \
        --out-dir studies/STUDY-002/outputs
"""
from __future__ import annotations

import argparse
import csv
import os
import sys
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from study001_pipeline import parse_score, wilson, pct  # noqa: E402

WINDOW_START = date(2015, 1, 1)
WINDOW_END = date(2026, 6, 1)

PLAYERS = [
    "Oskari Paldanius", "Svyatoslav Gulin", "Kimmer Coppejans", "Adrian Oetzbach",
    "Aaron Funk", "Carlo Alberto Caniato", "Michael Vrbensky", "Vadym Ursu",
    "Jay Clarke", "Arvid Nordquist", "Cezar Cretu", "Felix Alopaeus",
    "John Sperle", "Moez Echargui", "Luka Mikrut", "Iiro Vasa",
    "Sumit Nagal", "Sebastian Gima",
]

SMALL_N = 10        # below this: insufficient to characterise
CAUTION_N = 30      # below this: caution flag

LEVEL_LABEL = {
    "G": "Grand Slam", "M": "Masters 1000", "A": "ATP Tour", "F": "Tour Finals",
    "C": "Challenger", "S": "ITF/Satellite", "D": "Davis Cup", "O": "Olympics",
    # WTA/ITF prize-money levels appearing in the men's futures files:
    "15": "ITF $15k", "25": "ITF $25k", "10": "ITF $10k",
}


SURFACE_MAP = {"hard": "Hard", "clay": "Clay", "grass": "Grass", "carpet": "Carpet",
               "": "unknown", "nan": "unknown"}


def norm_surface(s: str) -> str:
    """Map to the controlled vocabulary (DATA_DICTIONARY: clay/hard/grass/carpet/unknown).

    The source mixes case ('Clay' 144,391 vs 'clay' 1,144 rows) and has 53 empty
    values. Left unnormalised, case variants silently split surface counts.
    Detected 2026-11-15; see STUDY-002 amendment A3.
    """
    return SURFACE_MAP.get((s or "").strip().lower(), "unknown")


def norm_name(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return " ".join(s.lower().replace("-", " ").replace(".", " ").replace("'", "").split())


def load(input_dir: str, manifest: list) -> list[dict]:
    rows = []
    for y in range(2015, 2027):
        for stem in (f"atp_matches_{y}", f"atp_matches_qual_chall_{y}", f"atp_matches_futures_{y}"):
            path = os.path.join(input_dir, stem + ".csv")
            if not os.path.isfile(path):
                continue
            manifest.append({"file": stem + ".csv", "bytes": os.path.getsize(path),
                             "sha256": _sha256(path)})
            with open(path, encoding="utf-8", newline="") as f:
                for r in csv.DictReader(f):
                    r["_file"] = stem
                    rows.append(r)
    return rows


def _sha256(path):
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _parse_date(s):
    try:
        return date(int(s[:4]), int(s[4:6]), int(s[6:8]))
    except (ValueError, TypeError, IndexError):
        return None


@dataclass
class Profile:
    name: str
    ids: set = field(default_factory=set)
    matches: list = field(default_factory=list)     # eligible completed
    excl: Counter = field(default_factory=Counter)
    levels: Counter = field(default_factory=Counter)
    surfaces: Counter = field(default_factory=Counter)
    opponent_levels: Counter = field(default_factory=Counter)
    # Per-format counters. Keeping these on the Profile as single integers
    # pooled best-of-3 and best-of-5 into one number and then printed that same
    # number on both rows (defect A5, fixed 2026-11-15).
    first_set_won: Counter = field(default_factory=Counter)   # keyed by best_of
    first_set_lost: Counter = field(default_factory=Counter)  # keyed by best_of
    tb_matches: Counter = field(default_factory=Counter)      # keyed by best_of
    surname_nearmisses: int = 0
    date_min: date | None = None
    date_max: date | None = None


def build(rows, targets):
    """targets: dict normalised_name -> Profile"""
    surname_index = {np: p for np, p in targets.items()}
    by_surname = defaultdict(list)
    for np in targets:
        by_surname[np.split()[-1]].append(np)

    for r in rows:
        wn, ln = norm_name(r["winner_name"]), norm_name(r["loser_name"])
        # exact full-name membership
        hit = None
        if wn in targets:
            hit, is_winner = wn, True
        elif ln in targets:
            hit, is_winner = ln, False
        else:
            # near-miss bookkeeping (surname match, full name differs)
            for nm in (wn, ln):
                sur = nm.split()[-1] if nm else ""
                if sur in by_surname:
                    for np in by_surname[sur]:
                        if np != nm:
                            surname_index[np].surname_nearmisses += 1
            continue

        p = targets[hit]
        d = _parse_date(r.get("tourney_date", ""))
        if d is None or not (WINDOW_START <= d <= WINDOW_END):
            p.excl["outside_window_or_bad_date"] += 1
            continue

        score = r.get("score") or ""
        if not score.strip():
            p.excl["empty_score"] += 1
            continue
        try:
            _bo = int(r.get("best_of") or 3)
        except ValueError:
            _bo = 3
        parsed = parse_score(score, best_of=_bo)
        if parsed.status == "walkover":
            p.excl["walkover"] += 1
            continue
        if parsed.status == "default":
            p.excl["default"] += 1
            continue
        if parsed.status == "abandoned":
            p.excl["abandoned"] += 1
            continue
        if parsed.status == "retired":
            p.excl["retired"] += 1
            continue
        if parsed.has_match_tiebreak:
            p.excl["match_tiebreak"] += 1
            continue
        if not parsed.ok:
            p.excl["unparsed"] += 1
            continue

        sets = [(s["games_winner"], s["games_loser"], s["tiebreak"]) for s in parsed.sets]
        p.matches.append({
            "date": d, "level": r.get("tourney_level", ""), "surface": norm_surface(r.get("surface", "")),
            "best_of": r.get("best_of", ""), "sets": sets,
            "is_winner": is_winner, "round": r.get("round", ""),
            "opponent": (r["loser_name"] if is_winner else r["winner_name"]),
            "tourney": r.get("tourney_name", ""),
        })
        p.ids.add(r["winner_id"] if is_winner else r["loser_id"])
        p.levels[(r.get("tourney_level") or "unknown").strip() or "unknown"] += 1
        p.surfaces[norm_surface(r.get("surface", ""))] += 1
        p.date_min = d if p.date_min is None else min(p.date_min, d)
        p.date_max = d if p.date_max is None else max(p.date_max, d)

        # first-set context, player perspective
        w, l, _ = sets[0]
        won_s1 = (w > l) if is_winner else (w < l)
        _fmt = r.get("best_of", "3")
        if won_s1:
            p.first_set_won[_fmt] += 1
        else:
            p.first_set_lost[_fmt] += 1
        if any(tb for (_a, _b, tb) in sets):
            p.tb_matches[_fmt] += 1
    return targets


def profile_rows(p: Profile):
    """One row per player per match format.

    Column names are format-relative rather than absolute: `straight_set_*`
    means the minimum number of sets for that format (2 in best-of-3, 3 in
    best-of-5) and `went_distance_*` means the maximum (3 or 5). Reporting
    literal "two set" / "three set" columns for best-of-5 matches would be
    meaningless, so the per-set-count distribution is published separately in
    player_match_structure.csv.
    """
    out = []
    by_format = defaultdict(list)
    for m in p.matches:
        by_format[m["best_of"]].append(m)

    for fmt in sorted(by_format, key=lambda x: (x != "3", x)):
        ms = by_format[fmt]
        n = len(ms)
        try:
            bo = int(fmt)
        except ValueError:
            bo = 3
        min_sets = (bo + 1) // 2
        c = Counter(len(m["sets"]) for m in ms)
        straight = c.get(min_sets, 0)
        distance = c.get(bo, 0)
        middle = n - straight - distance
        flag = ("insufficient" if n < SMALL_N else
                "caution" if n < CAUTION_N else "ok")
        out.append({
            "player": p.name,
            "format": f"best-of-{bo}",
            "n_completed": n,
            "straight_set_n": straight,
            "straight_set_share": pct(straight, n),
            "straight_set_ci95": _ci(straight, n),
            "went_distance_n": distance,
            "went_distance_share": pct(distance, n),
            "went_distance_ci95": _ci(distance, n),
            "intermediate_n": middle,
            "setcount_distribution": ";".join(f"{k}sets:{v}" for k, v in sorted(c.items())),
            "sample_flag": flag,
            "retired_excluded": p.excl["retired"],
            "walkover_excluded": p.excl["walkover"],
            "unparsed_excluded": p.excl["unparsed"],
            "set1_won_n": p.first_set_won.get(fmt, 0),
            "set1_lost_n": p.first_set_lost.get(fmt, 0),
            "matches_with_tiebreak": p.tb_matches.get(fmt, 0),
            "tb_match_share": pct(p.tb_matches.get(fmt, 0), n),
            "date_min": p.date_min.isoformat() if p.date_min else "",
            "date_max": p.date_max.isoformat() if p.date_max else "",
            "source_ids": ";".join(sorted(p.ids)),
            "NOT_A_PROBABILITY": "descriptive history to 2026-06-01; not a forecast",
        })
    if not out:
        out.append({
            "player": p.name, "format": "none", "n_completed": 0,
            "straight_set_n": "", "straight_set_share": "n/a", "straight_set_ci95": "n/a",
            "went_distance_n": "", "went_distance_share": "n/a",
            "went_distance_ci95": "n/a", "intermediate_n": "",
            "setcount_distribution": "", "sample_flag": "insufficient",
            "retired_excluded": p.excl["retired"], "walkover_excluded": p.excl["walkover"],
            "unparsed_excluded": p.excl["unparsed"], "set1_won_n": 0, "set1_lost_n": 0,
            "matches_with_tiebreak": 0, "tb_match_share": "n/a",
            "date_min": "", "date_max": "",
            "source_ids": ";".join(sorted(p.ids)),
            "NOT_A_PROBABILITY": "no eligible completed matches",
        })
    return out


def _ci(k, n):
    if not n:
        return "n/a"
    lo, hi = wilson(k, n)
    return f"{100*lo:.1f}-{100*hi:.1f}%"


def write_csv(path, rows, fields):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", required=True)
    ap.add_argument("--out-dir", default="studies/STUDY-002/outputs")
    a = ap.parse_args(argv)

    manifest = []
    rows = load(a.input_dir, manifest)
    print(f"rows loaded: {len(rows)}")

    targets = {norm_name(n): Profile(n) for n in PLAYERS}
    build(rows, targets)

    prof_rows, level_rows, struct_rows, audit_rows = [], [], [], []
    for nm in sorted(targets, key=lambda k: targets[k].name):
        p = targets[nm]
        prof_rows += profile_rows(p)
        for lv, cnt in p.levels.most_common():
            level_rows.append({"player": p.name, "level_code": lv,
                               "level_label": LEVEL_LABEL.get(lv, lv), "n": cnt,
                               "share": pct(cnt, len(p.matches))})
        for sf, cnt in p.surfaces.most_common():
            level_rows.append({"player": p.name, "level_code": "surface:" + (sf or "?"),
                               "level_label": sf or "unknown", "n": cnt,
                               "share": pct(cnt, len(p.matches))})
        c = Counter(len(m["sets"]) for m in p.matches)
        for k in sorted(c):
            struct_rows.append({"player": p.name, "conventional_sets": k,
                                "n": c[k], "share": pct(c[k], len(p.matches))})
        audit_rows.append({
            "player": p.name, "exact_matches": len(p.matches),
            "surname_only_nearmisses": p.surname_nearmisses,
            "source_ids_found": ";".join(sorted(p.ids)),
            "ids_count": len(p.ids),
            "retired": p.excl["retired"], "walkover": p.excl["walkover"],
            "default": p.excl["default"], "abandoned": p.excl["abandoned"],
            "match_tiebreak": p.excl["match_tiebreak"],
            "unparsed": p.excl["unparsed"],
            "outside_window": p.excl["outside_window_or_bad_date"],
        })

    write_csv(f"{a.out_dir}/player_profiles.csv", prof_rows,
              list(prof_rows[0].keys()))
    write_csv(f"{a.out_dir}/player_level_surface.csv", level_rows,
              ["player", "level_code", "level_label", "n", "share"])
    write_csv(f"{a.out_dir}/player_match_structure.csv", struct_rows,
              ["player", "conventional_sets", "n", "share"])
    write_csv(f"{a.out_dir}/name_matching_audit.csv", audit_rows,
              list(audit_rows[0].keys()))
    write_csv(f"{a.out_dir}/source_manifest.csv", manifest,
              ["file", "bytes", "sha256"])

    print(f"\n{'player':24s}{'fmt':10s}{'n':>6s}{'straight':>10s}{'distance':>10s}{'flag':>13s}{'nearmiss':>9s}")
    for r in prof_rows:
        print(f"{r['player']:24s}{r['format']:10s}{r['n_completed']:>6}"
              f"{r['straight_set_share']:>10}{r['went_distance_share']:>10}"
              f"{r['sample_flag']:>13s}"
              f"{next(x['surname_only_nearmisses'] for x in audit_rows if x['player']==r['player']):>9}")


if __name__ == "__main__":
    main()
