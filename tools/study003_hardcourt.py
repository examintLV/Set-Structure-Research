#!/usr/bin/env python3
"""
STUDY-003 pipeline: hard-court descriptive profiles for 18 named players,
plus prior head-to-head records for the nine named pairings.

DESCRIPTIVE HISTORY ONLY. Emits no probability, forecast, verdict or ranking.
See studies/STUDY-003/STUDY_SPECIFICATION.md section 12.

Reuses the score parser and Wilson implementation from study001_pipeline and
the name/surface normalisation from study002_profiles, so no study can drift
from another in how it reads a score string or a surface label.

Usage:
    python3 tools/study003_hardcourt.py --input-dir /tmp/p2 \
        --out-dir studies/STUDY-003/outputs
"""
from __future__ import annotations

import argparse
import csv
import os
import sys
from collections import Counter, defaultdict
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from study001_pipeline import parse_score, wilson, pct          # noqa: E402
from study002_profiles import norm_name, norm_surface, load, _parse_date, LEVEL_LABEL  # noqa: E402

WINDOW_START = date(2015, 1, 1)
WINDOW_END = date(2026, 6, 1)
SMALL_N, CAUTION_N = 10, 30

PLAYERS = [
    "Luca Nardi", "Milos Karol", "Matthew William Donald", "Martin Krumich",
    "Cyril Vandermeersch", "Alibek Kachmazov", "Hugo Grenier", "Florent Bax",
    "Buvaysar Gadamauri", "Adrien Gobat", "Matisse Bobichon", "Ugo Blanchet",
    "Alejandro Moro Canas", "Robin Catry", "Lenny Couturier", "Jonas Forejtek",
    "Filip Cristian Jianu", "Carlos Taberner",
]

PAIRS = [
    ("Luca Nardi", "Milos Karol"),
    ("Matthew William Donald", "Martin Krumich"),
    ("Cyril Vandermeersch", "Alibek Kachmazov"),
    ("Hugo Grenier", "Florent Bax"),
    ("Buvaysar Gadamauri", "Adrien Gobat"),
    ("Matisse Bobichon", "Ugo Blanchet"),
    ("Alejandro Moro Canas", "Robin Catry"),
    ("Lenny Couturier", "Jonas Forejtek"),
    ("Filip Cristian Jianu", "Carlos Taberner"),
]


def _ci(k, n):
    if not n:
        return "n/a"
    lo, hi = wilson(k, n)
    return f"{100*lo:.1f}-{100*hi:.1f}%"


def flag(n):
    return "insufficient" if n < SMALL_N else "caution" if n < CAUTION_N else "ok"


def write_csv(path, rows, fields):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", required=True)
    ap.add_argument("--out-dir", default="studies/STUDY-003/outputs")
    a = ap.parse_args(argv)

    manifest = []
    rows = load(a.input_dir, manifest)
    print(f"rows loaded: {len(rows)}")

    targets = {norm_name(p): p for p in PLAYERS}
    by_surname = defaultdict(list)
    for np in targets:
        by_surname[np.split()[-1]].append(np)

    # collected per player
    hist = {p: {"all": 0, "hard": defaultdict(list), "excl": Counter(),
                "surfaces": Counter(), "nearmiss": 0, "ids": set()} for p in PLAYERS}
    h2h = []

    for r in rows:
        wn, ln = norm_name(r["winner_name"]), norm_name(r["loser_name"])
        d = _parse_date(r.get("tourney_date", ""))
        in_win = d is not None and WINDOW_START <= d <= WINDOW_END

        # ---- head-to-head, both directions, any surface
        for A, B in PAIRS:
            na, nb = norm_name(A), norm_name(B)
            if {wn, ln} == {na, nb} and in_win:
                a_won = (wn == na)
                parsed = parse_score(r.get("score") or "", best_of=int(r.get("best_of") or 3))
                sets = [(s["games_winner"], s["games_loser"], s["tiebreak"]) for s in parsed.sets]
                h2h.append({
                    "pairing": f"{A} vs {B}",
                    "date": d.isoformat(),
                    "tourney": r.get("tourney_name", ""),
                    "level": LEVEL_LABEL.get((r.get("tourney_level") or "").strip(), r.get("tourney_level", "")),
                    "round": r.get("round", ""),
                    "surface": norm_surface(r.get("surface", "")),
                    "best_of": r.get("best_of", ""),
                    "score": r.get("score", ""),
                    "winner": r.get("winner_name", ""),
                    "loser": r.get("loser_name", ""),
                    "sets_played": len(sets),
                    "parse_ok": parsed.ok,
                    "winner_is_first_named": a_won,
                })

        # ---- per-player accumulation
        hit = None
        is_winner = None
        if wn in targets:
            hit, is_winner = wn, True
        elif ln in targets:
            hit, is_winner = ln, False
        else:
            if in_win:
                for nm in (wn, ln):
                    sur = nm.split()[-1] if nm else ""
                    for np_ in by_surname.get(sur, []):
                        if np_ != nm:
                            targets[np_].strip if False else None
                            hist[targets[np_]]["nearmiss"] += 1
            continue

        p = targets[hit]
        if not in_win:
            hist[p]["excl"]["outside_window_or_bad_date"] += 1
            continue

        # count all surfaces for the "share of history" denominator
        score = r.get("score") or ""
        parsed = parse_score(score, best_of=int(r.get("best_of") or 3))
        if parsed.status == "walkover":
            hist[p]["excl"]["walkover"] += 1
            continue
        if parsed.status == "default":
            hist[p]["excl"]["default"] += 1
            continue
        if parsed.status == "abandoned":
            hist[p]["excl"]["abandoned"] += 1
            continue
        if parsed.status == "retired":
            hist[p]["excl"]["retired"] += 1
            continue
        if parsed.has_match_tiebreak:
            hist[p]["excl"]["match_tiebreak"] += 1
            continue
        if not parsed.ok:
            hist[p]["excl"]["unparsed"] += 1
            continue

        surf = norm_surface(r.get("surface", ""))
        hist[p]["all"] += 1
        hist[p]["surfaces"][surf] += 1
        hist[p]["ids"].add(r["winner_id"] if is_winner else r["loser_id"])

        sets = [(s["games_winner"], s["games_loser"], s["tiebreak"]) for s in parsed.sets]
        w, l, _ = sets[0]
        won_s1 = (w > l) if is_winner else (w < l)
        rec = {
            "sets": sets, "best_of": r.get("best_of", "3"),
            "level": (r.get("tourney_level") or "").strip(),
            "won_s1": won_s1,
            "tb": any(tb for (_a, _b, tb) in sets),
            "is_winner": is_winner,
        }
        if surf == "Hard":
            hist[p]["hard"][r.get("best_of", "3")].append(rec)

    # ---- build hard-court profile rows
    prof_rows, share_rows, audit_rows = [], [], []
    for p in PLAYERS:
        h = hist[p]
        hard_total = sum(len(v) for v in h["hard"].values())
        share_rows.append({
            "player": p,
            "all_surfaces_n": h["all"],
            "hard_n": hard_total,
            "hard_share_of_history": pct(hard_total, h["all"]),
            "clay_n": h["surfaces"].get("Clay", 0),
            "grass_n": h["surfaces"].get("Grass", 0),
            "carpet_n": h["surfaces"].get("Carpet", 0),
            "unknown_surface_n": h["surfaces"].get("unknown", 0),
        })
        if not h["hard"]:
            prof_rows.append({
                "player": p, "format": "none", "n_hard": 0,
                "straight_set_n": "", "straight_set_share": "n/a",
                "straight_set_ci95": "n/a", "went_distance_n": "",
                "went_distance_share": "n/a", "went_distance_ci95": "n/a",
                "intermediate_n": "", "setcount_distribution": "",
                "set1_won_n": "", "set1_lost_n": "", "matches_with_tiebreak": "",
                "tb_match_share": "n/a", "sample_flag": "insufficient",
                "NOT_A_PROBABILITY": "descriptive hard-court history; not a forecast",
            })
        for fmt in sorted(h["hard"], key=lambda x: (x != "3", x)):
            ms = h["hard"][fmt]
            n = len(ms)
            bo = int(fmt) if fmt.isdigit() else 3
            min_sets, max_sets = (bo + 1) // 2, bo
            c = Counter(len(m["sets"]) for m in ms)
            straight, distance = c.get(min_sets, 0), c.get(max_sets, 0)
            prof_rows.append({
                "player": p,
                "format": f"best-of-{bo}",
                "n_hard": n,
                "straight_set_n": straight,
                "straight_set_share": pct(straight, n),
                "straight_set_ci95": _ci(straight, n),
                "went_distance_n": distance,
                "went_distance_share": pct(distance, n),
                "went_distance_ci95": _ci(distance, n),
                "intermediate_n": n - straight - distance,
                "setcount_distribution": ";".join(f"{k}sets:{v}" for k, v in sorted(c.items())),
                "set1_won_n": sum(1 for m in ms if m["won_s1"]),
                "set1_lost_n": sum(1 for m in ms if not m["won_s1"]),
                "matches_with_tiebreak": sum(1 for m in ms if m["tb"]),
                "tb_match_share": pct(sum(1 for m in ms if m["tb"]), n),
                "sample_flag": flag(n),
                "NOT_A_PROBABILITY": "descriptive hard-court history; not a forecast",
            })
        audit_rows.append({
            "player": p, "hard_matches": hard_total, "all_matches": h["all"],
            "surname_only_nearmisses": h["nearmiss"],
            "source_ids": ";".join(sorted(h["ids"])),
            "retired": h["excl"]["retired"], "walkover": h["excl"]["walkover"],
            "default": h["excl"]["default"], "match_tiebreak": h["excl"]["match_tiebreak"],
            "unparsed": h["excl"]["unparsed"],
            "outside_window": h["excl"]["outside_window_or_bad_date"],
        })

    write_csv(f"{a.out_dir}/hard_court_profiles.csv", prof_rows,
              list(prof_rows[0].keys()))
    write_csv(f"{a.out_dir}/hard_court_share_of_history.csv", share_rows,
              list(share_rows[0].keys()))
    write_csv(f"{a.out_dir}/head_to_head.csv", h2h,
              ["pairing", "date", "tourney", "level", "round", "surface", "best_of",
               "score", "winner", "loser", "sets_played", "parse_ok",
               "winner_is_first_named"])
    write_csv(f"{a.out_dir}/name_matching_audit.csv", audit_rows,
              list(audit_rows[0].keys()))
    write_csv(f"{a.out_dir}/source_manifest.csv", manifest, ["file", "bytes", "sha256"])

    # ---- integrity asserts (fail loudly rather than publish a wrong table)
    for r in prof_rows:
        if r["format"] == "none":
            continue
        n = r["n_hard"]
        assert r["set1_won_n"] + r["set1_lost_n"] == n, f"set1 identity failed {r}"
        assert r["straight_set_n"] + r["went_distance_n"] + r["intermediate_n"] == n, \
            f"structure identity failed {r}"
    print("integrity asserts passed")

    print(f"\n{'player':26s}{'fmt':10s}{'nHard':>6s}{'hard%hist':>10s}"
          f"{'straight':>10s}{'distance':>10s}{'flag':>13s}")
    share = {r['player']: r for r in share_rows}
    for r in prof_rows:
        print(f"{r['player']:26s}{r['format']:10s}{r['n_hard']:>6}"
              f"{share[r['player']]['hard_share_of_history']:>10}"
              f"{r['straight_set_share']:>10}{r['went_distance_share']:>10}"
              f"{r['sample_flag']:>13s}")
    print(f"\nhead-to-head records found: {len(h2h)}")


if __name__ == "__main__":
    main()
