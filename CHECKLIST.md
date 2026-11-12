# Before it ships: the three-question checklist

Ask these three questions of any number an AI tool helped produce, before it reaches a VP, a dean, or a board.

## 1. Source: where did this number come from?
- Name the table, view, or file, and the date it was pulled.
- Confirm the dates the report claims really exist in the data.
- If you cannot name the source, the number does not go out.

## 2. Method: how was it calculated?
- Point to the written rule for each number (`rules/report_rules.md`).
- Recount the headline a second way, with separate code or by hand.
- Check that the parts add up to the total.

## 3. Falsifier: what would prove it wrong?
- Name the one result that would show the number is wrong, and test for it.
- Break a copy on purpose and confirm your check catches it. A check that can never fail is not a check.
- Compare with what the person who knows the data expects. A surprise is a reason to look, not a headline.

## Then a person signs off
The tool drafts. A person who knows the data reads it and approves it before it is sent.

---

In this kit, `check/verify.py` runs questions 1 and 2, and `python check/verify.py --falsify` runs question 3.
