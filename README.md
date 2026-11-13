# Weekly Report Kit

**Automate one weekly report with AI, and trust the number.**

A free take-home kit from *From Demo to System: AI-Augmented Analytics at a Small Private University*, presented by Union University Enterprise Systems, IT at the 2026 HESS Consortium National Conference.

👉 **Start with the kit page: [uubryson.github.io/hess-2026-ai-report-kit](https://uubryson.github.io/hess-2026-ai-report-kit/)**

It walks through one report almost every school builds by hand, weekly registration pacing, from manual to automated to verified. Everything runs on fake data with standard Python, so you can try it in about 15 minutes.

## Try it

You need Python 3.9 or later. Nothing else to install. The three commands after `cd` build the report from the fake data, run the 14 checks (exit code 0 means OK to send), and prove the checks can fail.

```
git clone https://github.com/UUBryson/hess-2026-ai-report-kit.git
cd hess-2026-ai-report-kit
python report/build_report.py
python check/verify.py
python check/verify.py --challenge
```

Then watch the checker catch the classic mistake, comparing by calendar date instead of the same week of the year:

```
python report/build_report.py --compare-by calendar --out report/out_mistake
python check/verify.py --summary report/out_mistake/summary.json
```

On Windows, use `py` if `python` isn't found. On a Mac, use `python3`.

## The three essentials

| | Essential | In the kit |
|---|---|---|
| 01 | **Governed data access.** Read-only accounts on a reporting copy, access by role, changes only through your normal process. | [`ACCESS.md`](ACCESS.md) |
| 02 | **Verify before it ships.** Source, method, and a challenge for every number, then a human reviewer signs off. | [`CHECKLIST.md`](CHECKLIST.md), [`check/verify.py`](check/verify.py) |
| 03 | **Knowledge written down.** The rules in one person's head, captured once, so people and AI tools follow the same ones. | [`rules/report_rules.md`](rules/report_rules.md) |

## What's inside

| File | What it is |
|---|---|
| [`rules/report_rules.md`](rules/report_rules.md) | The written-down rules for the report. Start here. |
| [`prompts/01_build_report.md`](prompts/01_build_report.md) | The prompt to give your AI assistant. |
| [`report/build_report.py`](report/build_report.py) | A reference script, the kind the prompt produces. |
| [`check/verify.py`](check/verify.py) | Source and method checks, plus a challenge that proves the checks can fail. |
| [`data/registrations_sample.csv`](data/registrations_sample.csv) | Fake weekly snapshots for two spring terms (rebuild with `data/make_sample_data.py`). |
| [`examples/`](examples/) | The finished sample report, the mistaken one, and its summary. |
| [`CHECKLIST.md`](CHECKLIST.md), [`ACCESS.md`](ACCESS.md) | One-page guides for verification and data access. |

## Make it yours

1. **Pick the report** someone builds by hand every week.
2. **Write the rules down** with the person who builds it, then read them back.
3. **Get read-only access** using the request in `ACCESS.md`. Start with fake data.
4. **Have an approved AI tool draft the script** from the rules file and the prompt.
5. **Verify, then hand it back.** Run the checks; the original builder signs off.

## Contact

Questions or want to go further? Willie George ([wgeorge@uu.edu](mailto:wgeorge@uu.edu)) or Bryson McNichols ([bmcnichols@uu.edu](mailto:bmcnichols@uu.edu)), Union University Enterprise Systems, IT.

All data in this kit is invented. No Union University data is included. [MIT License](LICENSE).
