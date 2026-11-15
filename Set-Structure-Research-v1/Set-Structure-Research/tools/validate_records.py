#!/usr/bin/env python3
"""Structural checks for a matches.csv export; not a source verifier."""
import csv
import sys
from pathlib import Path
from datetime import date

REQUIRED = {"match_id", "match_date", "discipline", "surface", "match_format", "status"}
STATUSES = {"completed", "retired", "walkover", "default", "abandoned", "unknown"}
SURFACES = {"clay", "hard", "grass", "carpet", "unknown"}
DISCIPLINES = {"singles", "doubles", "mixed", "other"}

def validate(path: Path):
    errors, seen = [], set()
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            return ["CSV has no header row"]
        missing = REQUIRED - set(reader.fieldnames)
        if missing:
            return [f"Missing required columns: {', '.join(sorted(missing))}"]
        for line, row in enumerate(reader, 2):
            mid = (row.get("match_id") or "").strip()
            if not mid:
                errors.append(f"Line {line}: empty match_id")
            elif mid in seen:
                errors.append(f"Line {line}: duplicate match_id {mid}")
            seen.add(mid)
            if (row.get("status") or "").strip().lower() not in STATUSES:
                errors.append(f"Line {line}: invalid status")
            if (row.get("surface") or "").strip().lower() not in SURFACES:
                errors.append(f"Line {line}: invalid surface")
            if (row.get("discipline") or "").strip().lower() not in DISCIPLINES:
                errors.append(f"Line {line}: invalid discipline")
            try:
                date.fromisoformat((row.get("match_date") or "").strip())
            except ValueError:
                errors.append(f"Line {line}: match_date must be YYYY-MM-DD")
            if (row.get("status") or "").strip().lower() == "walkover":
                errors.append(f"Line {line}: walkover requires separate handling")
    return errors

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python tools/validate_records.py matches.csv")
        raise SystemExit(2)
    p = Path(sys.argv[1])
    if not p.is_file():
        print(f"File not found: {p}")
        raise SystemExit(2)
    problems = validate(p)
    if problems:
        print("\n".join(problems))
        raise SystemExit(1)
    print("Structural checks passed; source accuracy is not verified.")
