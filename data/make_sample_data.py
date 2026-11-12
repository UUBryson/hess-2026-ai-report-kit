"""Make the fake registration snapshots used by the kit.

Every name, ID and number here is invented. Re-running gives the same file (fixed seed).

One row = one student registered for the term as of one snapshot date.
Snapshots are taken every Monday while registration is open.
"""
import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(2026)

SCHOOLS = ["Arts & Sciences", "Business", "Education", "Nursing", "Theology"]
SCHOOL_WEIGHTS = [0.40, 0.20, 0.12, 0.20, 0.08]

# term, first Monday of registration, number of weekly snapshots, final headcount
TERMS = [
    ("2026SP", date(2025, 10, 27), 12, 1480),  # last year: full season
    ("2027SP", date(2026, 10, 26), 3, 1440),   # this year: three Mondays so far
]


def curve(week):
    """Share of final headcount registered by a given week (fast early, then slow)."""
    return min(1.0, 0.48 + 0.11 * week - 0.004 * week * week)


def make_students(term, n):
    students = []
    for i in range(n):
        level = "GR" if random.random() < 0.18 else "UG"
        roll = random.random()
        if roll < 0.06:
            stype = "Dual Enrollment"
        elif roll < 0.16:
            stype = "New"
        else:
            stype = "Returning"
        hours = random.choice([12, 13, 14, 15, 15, 16, 17]) if level == "UG" else random.choice([3, 6, 6, 9])
        if stype == "Dual Enrollment":
            hours = random.choice([3, 3, 6])
        students.append({
            "student_id": f"S{term[:4]}{i:05d}",
            "school": random.choices(SCHOOLS, SCHOOL_WEIGHTS)[0],
            "student_level": level,
            "student_type": stype,
            "credit_hours": hours,
            "order": random.random(),
        })
    students.sort(key=lambda s: s["order"])
    return students


rows = []
for term, first_monday, n_weeks, final_n in TERMS:
    students = make_students(term, final_n)
    for week in range(n_weeks):
        snap = first_monday + timedelta(weeks=week)
        k = int(final_n * curve(week))
        for s in students[:k]:
            hours = s["credit_hours"]
            # about 1.5% of rows are students who dropped everything but still have a row (0 hours)
            if random.random() < 0.015:
                hours = 0
            rows.append([snap.isoformat(), term, s["student_id"], s["school"],
                         s["student_level"], s["student_type"], hours])

out = Path(__file__).with_name("registrations_sample.csv")
with out.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["snapshot_date", "term", "student_id", "school", "student_level", "student_type", "credit_hours"])
    w.writerows(rows)
print(f"wrote {len(rows):,} rows to {out.name}")
