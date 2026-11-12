"""Build the weekly registration report from the snapshot file.

This is the kind of script an AI assistant writes for you from rules/report_rules.md
and prompts/01_build_report.md. Read it before you trust it, then run check/verify.py.

    python report/build_report.py                      # latest snapshot of 2027SP vs 2026SP
    python report/build_report.py --as-of 2026-11-02
    python report/build_report.py --compare-by calendar  # the common mistake, for the demo
"""
import argparse
import csv
import html
import json
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def same_week_last_year(d):
    """Rule 4: same week of the year (ISO numbering) and weekday, one year back."""
    year, week, weekday = d.isocalendar()
    return date.fromisocalendar(year - 1, week, weekday)


def summarize(rows, term, snap):
    head = set()
    de = set()
    hours = 0
    by_school = defaultdict(int)
    by_level = defaultdict(int)
    by_type = defaultdict(int)
    for r in rows:
        if r["term"] != term or r["snapshot_date"] != snap.isoformat():
            continue
        h = int(r["credit_hours"])
        if h <= 0:                                  # rule 1
            continue
        if r["student_type"] == "Dual Enrollment":  # rule 2
            de.add(r["student_id"])
            continue
        head.add(r["student_id"])
        hours += h                                   # rule 3
        by_school[r["school"]] += 1
        by_level[r["student_level"]] += 1
        by_type[r["student_type"]] += 1
    return {"date": snap.isoformat(), "headcount": len(head), "credit_hours": hours,
            "dual_enrollment": len(de), "by_school": dict(sorted(by_school.items())),
            "by_level": dict(sorted(by_level.items())), "by_type": dict(sorted(by_type.items()))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=ROOT / "data" / "registrations_sample.csv")
    ap.add_argument("--term", default="2027SP")
    ap.add_argument("--prior-term", default="2026SP")
    ap.add_argument("--as-of", help="snapshot date, default = latest for the term")
    ap.add_argument("--compare-by", choices=["week", "calendar"], default="week")
    ap.add_argument("--out", default=ROOT / "report" / "out")
    a = ap.parse_args()

    rows = load(a.data)
    dates = {r["snapshot_date"] for r in rows if r["term"] == a.term}
    as_of = date.fromisoformat(a.as_of) if a.as_of else date.fromisoformat(max(dates))

    if a.compare_by == "week":
        compare = same_week_last_year(as_of)
    else:
        # The mistake: same calendar date last year, then "nearest earlier snapshot" to cover the gap.
        target = as_of.replace(year=as_of.year - 1)
        prior_dates = sorted(r["snapshot_date"] for r in rows if r["term"] == a.prior_term)
        compare = date.fromisoformat(max(d for d in prior_dates if d <= target.isoformat()))

    prior_dates = {r["snapshot_date"] for r in rows if r["term"] == a.prior_term}
    if compare.isoformat() not in prior_dates:     # rule 5
        raise SystemExit(f"No {a.prior_term} snapshot on {compare}. Not substituting another date.")

    now = summarize(rows, a.term, as_of)
    then = summarize(rows, a.prior_term, compare)
    summary = {"term": a.term, "prior_term": a.prior_term, "compare_by": a.compare_by,
               "this_year": now, "last_year": then,
               "change": now["headcount"] - then["headcount"]}

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (out / "report.html").write_text(render(summary), encoding="utf-8")
    print(f"{a.term} as of {as_of}: {now['headcount']:,} students "
          f"({summary['change']:+,} vs {compare}). Wrote {out / 'report.html'}")


def render(s):
    t, p = s["this_year"], s["last_year"]
    def table(title, key):
        keys = sorted(set(t[key]) | set(p[key]))
        body = "".join(
            f"<tr><td>{html.escape(k)}</td><td>{t[key].get(k, 0):,}</td>"
            f"<td>{p[key].get(k, 0):,}</td><td>{t[key].get(k, 0) - p[key].get(k, 0):+,}</td></tr>"
            for k in keys)
        return (f"<h2>{title}</h2><table><tr><th>{title}</th><th>This year</th><th>Last year</th><th>Change</th></tr>{body}"
                f"<tr><th>Total</th><th>{t['headcount']:,}</th><th>{p['headcount']:,}</th><th>{s['change']:+,}</th></tr></table>")
    word = "up" if s["change"] >= 0 else "down"
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>Registration Report {t['date']}</title>
<style>body{{font-family:system-ui,sans-serif;margin:24px;color:#1f2937}}h1{{font-size:22px}}h2{{font-size:16px;margin-top:20px}}
table{{border-collapse:collapse;margin-top:12px}}td,th{{border:1px solid #d1d5db;padding:6px 10px;text-align:right}}
td:first-child,th:first-child{{text-align:left}}.big{{font-size:40px;font-weight:700}}.muted{{color:#6b7280}}</style></head><body>
<h1>{s['term']} Registration Report</h1>
<p class="muted">As of {t['date']}, compared with {p['date']} ({s['prior_term']}). Fake data from the HESS 2026 kit.</p>
<p class="big">{t['headcount']:,}</p>
<p>students registered, {word} {abs(s['change']):,} from the same week last year ({p['headcount']:,}).
Credit hours {t['credit_hours']:,} vs {p['credit_hours']:,}. Dual enrollment, reported separately: {t['dual_enrollment']:,} vs {p['dual_enrollment']:,}.</p>
{table("School", "by_school")}
{table("Level", "by_level")}
{table("Student type", "by_type")}
</body></html>"""


if __name__ == "__main__":
    main()
