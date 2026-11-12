# Weekly Report Kit (HESS 2026)

Take-home kit from **From Demo to System: AI-Augmented Analytics at a Small Private University**, 2026 HESS Consortium National Conference, presented by Union University Enterprise Systems, IT.

Automate one weekly report with AI, and trust the number. Everything runs on fake data with standard Python.

**Start here:** the [kit page](https://uubryson.github.io/hess-2026-ai-report-kit/).

```
python report/build_report.py      # build the report from the fake data
python check/verify.py             # source and method checks; exit 0 = OK to send
python check/verify.py --falsify   # prove the checks can fail
```

| File | What it is |
|---|---|
| `rules/report_rules.md` | The written-down rules for the report. Start here. |
| `prompts/01_build_report.md` | The prompt to give your AI assistant. |
| `report/build_report.py` | Reference script, the kind the prompt produces. |
| `check/verify.py` | Source and method checks, plus a falsifier. |
| `data/registrations_sample.csv` | Fake weekly registration snapshots (regenerate with `data/make_sample_data.py`). |
| `CHECKLIST.md` | Source, method, falsifier: three questions before a number ships. |
| `ACCESS.md` | Governed data access: what the tool can and cannot touch. |

All data is invented. No Union University data is included.

MIT License.
