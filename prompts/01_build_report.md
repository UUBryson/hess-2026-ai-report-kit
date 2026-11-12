# Prompt: build the report

Paste this into the AI coding assistant your school allows (Claude, ChatGPT, Copilot, Gemini). Attach `rules/report_rules.md` and the first 50 lines of your data file. Do not paste real student records into a tool your school has not approved for that data. The fake file in this kit is safe anywhere.

---

You are helping me automate a weekly report that a person on our team builds by hand today.

Attached:
1. `report_rules.md`: the rules for this report, written down by the person who builds it. These rules win over anything you assume.
2. A sample of the data file, one row per student per snapshot date.

Write one Python script, standard library only, that:
- reads the full data file,
- builds the report exactly as the rules describe,
- writes `summary.json` (every number in the report) and `report.html` (one page, readable on a phone).

Before you write code:
- List each rule and say in one line how the script will apply it.
- List anything in the rules that is ambiguous and ask me instead of guessing.

After the code:
- Tell me which numbers I should check by hand the first time, and how.

---

## Then
1. Read the script. If you cannot explain a line, ask the assistant what it does.
2. Run it on the fake data and compare with `examples/report_correct.html`.
3. Run `python check/verify.py`. Do not share a report that fails a check.
4. Show the first real report to the person who used to build it by hand. They are the final check.
