# Governed data access: setting it up at your school

The AI tool should be able to read what the report needs and nothing more. That keeps this a conversation your DBA and security team can say yes to.

## What the tool can touch
- A **reporting copy** of your SIS data (warehouse, replica, or nightly export), never the live production database.
- A **read-only login** created for this purpose, limited to the views the report needs.
- **Fake or de-identified data** while you are building and testing. This kit's sample file is fully fake.

## What it cannot touch
- No write access to production, ever. If the data is wrong, fix the process that feeds it, not the rows.
- No credentials pasted into prompts or saved in the repo.
- No real student records in an AI tool your institution has not approved for that data (FERPA).

## Who approves what
| Decision | Who |
|---|---|
| Which data the report may read | Data owner (e.g., Registrar) |
| The read-only login and its views | DBA or ERP team |
| Which AI tools may see real data | IT / security, per institutional policy |
| Who receives the finished report | Report owner, by role, not a hand-kept list of names |

## A first ask to your DBA
> We'd like a read-only login to the reporting copy, limited to one view: one row per student per term per snapshot date, with school, level, student type, and credit hours. It's for automating the weekly registration report. No write access, no production.
