# Codex Task — Independent Chapter Quality Review

## Goal

Perform a critical editorial and technical review of:

- `chapters/<NN>-<slug>.md`

Do not assume the existing self-review is correct.

## Context

Read:

- `AGENTS.md`
- `docs/BOOK_BLUEPRINT.md`
- `docs/QUALITY_RUBRIC.md`
- `templates/CHAPTER_TEMPLATE.md`
- `docs/STYLE_GUIDE.md`
- the target chapter;
- its prerequisite chapters;
- its existing review file.

## Review Lenses

Review the chapter independently for:

1. technical accuracy;
2. misleading simplifications;
3. missing prerequisites;
4. quality of first-principles explanation;
5. transferability across technologies;
6. practical usefulness;
7. production realism;
8. failure-mode coverage;
9. fairness of trade-offs;
10. unnecessary repetition;
11. scope creep;
12. teaching quality;
13. exercise quality;
14. terminology consistency;
15. cross-chapter integration.

## Work to Perform

1. Add an `Independent Review` section to:
   - `reviews/<NN>-<slug>-review.md`
2. Identify findings by severity:
   - `Blocking`
   - `Major`
   - `Minor`
   - `Optional`
3. For every blocking or major finding:
   - cite the relevant chapter section;
   - explain why it matters;
   - propose a concrete revision.
4. Re-score all quality-rubric criteria independently.
5. Do not rewrite the chapter in this task unless explicitly instructed.
6. Recommend either:
   - `Approve`;
   - `Revise`;
   - `Restructure`.

## Done When

Report:

- recommendation;
- blocking findings;
- major findings;
- rubric scores;
- the three highest-value revisions.
