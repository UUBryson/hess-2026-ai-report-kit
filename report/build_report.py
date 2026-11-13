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

    def delta(now, then):
        d = now - then
        cls = "up" if d > 0 else "down" if d < 0 else "flat"
        return f'<span class="chg {cls}">{d:+,}</span>'

    def tile(label, now, then):
        return (f'<div class="tile"><div class="lbl">{label}</div><div class="num">{now:,}</div>'
                f'<div class="sub">{delta(now, then)} vs {then:,} last year</div></div>')

    def table(title, key):
        keys = sorted(set(t[key]) | set(p[key]))
        body = "".join(
            f"<tr><td>{html.escape(k)}</td><td>{t[key].get(k, 0):,}</td>"
            f"<td>{p[key].get(k, 0):,}</td><td>{delta(t[key].get(k, 0), p[key].get(k, 0))}</td></tr>"
            for k in keys)
        return (f'<section class="card"><h2>By {title.lower()}</h2><table><thead><tr><th>{title}</th><th>This year</th>'
                f"<th>Last year</th><th>Change</th></tr></thead><tbody>{body}</tbody><tfoot><tr><th>Total</th>"
                f"<th>{t['headcount']:,}</th><th>{p['headcount']:,}</th><th>{delta(t['headcount'], p['headcount'])}</th></tr></tfoot></table></section>")

    method = ("Same week of the year and weekday last year" if s["compare_by"] == "week"
              else "Same calendar date last year, nearest earlier snapshot")
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{s['term']} Registration Report</title>
<style>
:root{{--bg:#faf9f6;--card:#fff;--fg:#24252a;--muted:#62646b;--line:#dedad5;--accent:#8c2034;--up:#246653;--down:#8c2034}}
@media (prefers-color-scheme:dark){{:root{{--bg:#15171b;--card:#1d2026;--fg:#ecebe7;--muted:#a4a9b2;--line:#30343c;--accent:#e58a7c;--up:#7fd19b;--down:#f09a8f}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 "Segoe UI",system-ui,-apple-system,sans-serif}}
.wrap{{width:min(100%,960px);margin:0 auto;padding:24px 16px 40px}}
.kicker{{color:var(--accent);font-weight:600;font-size:12px;letter-spacing:.06em;text-transform:uppercase;margin:0}}
h1{{margin:4px 0 6px;font-size:26px}}.meta{{color:var(--muted);margin:0 0 20px}}
.tiles{{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));margin-bottom:16px}}
.tile,.card{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px}}
.lbl{{color:var(--muted);font-size:13px}}.num{{font-size:34px;font-weight:700;line-height:1.2}}.sub{{font-size:13px;color:var(--muted)}}
.chg{{font-weight:700}}.chg.up{{color:var(--up)}}.chg.down{{color:var(--down)}}
.grid{{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(280px,1fr))}}
h2{{font-size:15px;margin:0 0 8px}}table{{width:100%;border-collapse:collapse}}
td,th{{padding:6px 4px;text-align:right;border-bottom:1px solid var(--line)}}td:first-child,th:first-child{{text-align:left}}
thead th{{color:var(--muted);font-weight:600;font-size:13px}}tfoot th{{border-bottom:0}}
.note{{margin-top:16px;color:var(--muted);font-size:13px}}
</style></head><body><div class="wrap">
<p class="kicker">Weekly Registration Report · fake data</p>
<h1>{s['term']} registration as of {t['date']}</h1>
<p class="meta">Compared with {p['date']} ({s['prior_term']}). Method: {method}.</p>
<div class="tiles">{tile("Students registered", t['headcount'], p['headcount'])}{tile("Credit hours", t['credit_hours'], p['credit_hours'])}{tile("Dual enrollment (reported separately)", t['dual_enrollment'], p['dual_enrollment'])}</div>
<div class="grid">{table("School", "by_school")}{table("Level", "by_level")}{table("Student type", "by_type")}</div>
<p class="note">Built by report/build_report.py from data/registrations_sample.csv. Every number here is invented. Run check/verify.py before sharing a report like this.</p>
</div></body></html>"""


if __name__ == "__main__":
    main()
