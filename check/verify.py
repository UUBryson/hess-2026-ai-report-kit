"""Check a report before anyone sees it. Source, method, and a challenge.

It recomputes the numbers from the raw file with separate code, then checks the rules.
Exit code 0 = every check passed. Anything else = do not send.

    python check/verify.py                       # checks report/out/summary.json
    python check/verify.py --summary examples/summary_with_mistake.json
    python check/verify.py --challenge           # prove the checks can fail
"""
import argparse
import copy
import csv
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def recount(rows, term, snap):
    """Independent recount: count students, not rows, and apply the written rules."""
    students = {}
    for r in rows:
        if r["term"] == term and r["snapshot_date"] == snap:
            students[r["student_id"]] = r
    keep = [r for r in students.values() if int(r["credit_hours"]) > 0 and r["student_type"] != "Dual Enrollment"]
    return len(keep), sum(int(r["credit_hours"]) for r in keep)


def run_checks(s, rows):
    results = []

    def check(name, ok, detail):
        results.append((name, ok, detail))

    t, p = s["this_year"], s["last_year"]
    snaps = {(r["term"], r["snapshot_date"]) for r in rows}

    # SOURCE: the dates the report claims really exist in the data.
    check("Source: as-of snapshot exists", (s["term"], t["date"]) in snaps, t["date"])
    check("Source: compare snapshot exists", (s["prior_term"], p["date"]) in snaps, p["date"])

    # METHOD: rule 4, same ISO week and weekday.
    a, c = date.fromisoformat(t["date"]), date.fromisoformat(p["date"])
    aw, cw = a.isocalendar(), c.isocalendar()
    check("Method: compare date is same week and weekday last year",
          cw[0] == aw[0] - 1 and cw[1] == aw[1] and cw[2] == aw[2],
          f"{a} is week {aw[1]} day {aw[2]}; {c} is week {cw[1]} day {cw[2]}")

    # METHOD: headline and hours match an independent recount.
    for label, side, term in (("this year", t, s["term"]), ("last year", p, s["prior_term"])):
        n, h = recount(rows, term, side["date"])
        check(f"Method: {label} headcount matches recount", side["headcount"] == n, f"report {side['headcount']:,}, recount {n:,}")
        check(f"Method: {label} credit hours match recount", side["credit_hours"] == h, f"report {side['credit_hours']:,}, recount {h:,}")
        for part in ("by_school", "by_level", "by_type"):
            name = {"by_school": "schools", "by_level": "levels", "by_type": "student types"}[part]
            check(f"Method: {label} {name} add up to headline", sum(side[part].values()) == side["headcount"],
                  f"{name} {sum(side[part].values()):,}, headline {side['headcount']:,}")

    check("Method: change = this year - last year", s["change"] == t["headcount"] - p["headcount"], f"{s['change']:+,}")
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=ROOT / "data" / "registrations_sample.csv")
    ap.add_argument("--summary", default=ROOT / "report" / "out" / "summary.json")
    ap.add_argument("--challenge", action="store_true", help="break a copy on purpose and confirm the checks catch it")
    a = ap.parse_args()

    with open(a.data, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    s = json.loads(Path(a.summary).read_text(encoding="utf-8"))

    if a.challenge:
        # CHALLENGE: a check that can never fail is not a check. Break things and expect failures.
        broken = copy.deepcopy(s)
        broken["this_year"]["headcount"] += 7
        bad_week = copy.deepcopy(s)
        bad_week["last_year"]["date"] = date.fromisoformat(s["this_year"]["date"]).replace(
            year=date.fromisoformat(s["this_year"]["date"]).year - 1).isoformat()
        caught = [not all(ok for _, ok, _ in run_checks(x, rows)) for x in (broken, bad_week)]
        print(f"Challenge: headcount off by 7 caught = {caught[0]}; calendar-date compare caught = {caught[1]}")
        sys.exit(0 if all(caught) else 1)

    results = run_checks(s, rows)
    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'}  {name}  ({detail})")
    failed = sum(not ok for _, ok, _ in results)
    print(f"\n{len(results) - failed} of {len(results)} checks passed." + ("" if not failed else " Do not send this report."))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
