# Report rules: Weekly Registration Report

This file is the most important part of the kit. It is the knowledge that usually lives in one person's head. Write it down once, and both your team and your AI tools follow the same rules.

The rules below are filled in for the fake "Example University" data in this kit. Replace them with your own.

## Who knows this
- **Owner of the rules:** Registrar's office (the person who builds this report by hand today)
- **How we captured it:** a 20-minute voice memo while they walked through last Monday's report, transcribed and turned into the list below, then read back to them to confirm
- **Last confirmed:** 2026-11-09

## What the report answers
How many students are registered for next term today, compared with the same point last year?

## Rules
1. **Headcount** = distinct students with more than 0 credit hours on the snapshot. A row with 0 hours is a student who dropped everything; do not count them.
2. **Dual enrollment** (high school students) is reported on its own line. It is NOT in the headline headcount.
3. **Credit hours** = sum of credit hours for the students in the headcount.
4. **Compare to last year using the same week and weekday, never the same calendar date.** Monday 2026-11-09 compares to Monday 2025-11-10 (both ISO week 46). The same calendar date last year (2025-11-09) was a Sunday, and there is no snapshot that day.
5. **If the compare snapshot does not exist, say so.** Do not quietly use the nearest date.
6. **Groups must add up.** The school lines must sum to the headline headcount.
7. **Report the as-of date on the page,** and the compare date next to it.

## Data source
- File in the kit: `data/registrations_sample.csv` (fake)
- At your school: a read-only view or export from your reporting copy of the SIS, one row per student per snapshot date. See `ACCESS.md`.

| column | meaning |
|---|---|
| snapshot_date | the Monday the snapshot was taken (YYYY-MM-DD) |
| term | term code, e.g. 2027SP |
| student_id | ID (fake in the kit) |
| school | academic school |
| student_level | UG or GR |
| student_type | New, Returning, or Dual Enrollment |
| credit_hours | registered hours on that date |
