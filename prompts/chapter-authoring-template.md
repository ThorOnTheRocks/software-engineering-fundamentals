# Codex Task — Draft and Review One Ebook Chapter

> **Manual fallback:** The canonical workflow is `$ebook`. This targeted prompt must still obey `book-manifest.json`, `docs/CHAPTER_LIFECYCLE.md`, deterministic validation, and the human-only approval transition.

Replace every value in angle brackets before running.

## Goal

Draft, review, and revise:

**Chapter <NN> — <CHAPTER TITLE>**

The final chapter should reach `Candidate for Human Approval` or clearly remain `Revision Required` with unresolved issues documented. This prompt cannot approve a chapter.

## Context

Read, in this order:

1. `AGENTS.md`
2. `docs/BOOK_BLUEPRINT.md`
3. `docs/QUALITY_RUBRIC.md`
4. `templates/CHAPTER_TEMPLATE.md`
5. `docs/STYLE_GUIDE.md`
6. `docs/EDITORIAL_WORKFLOW.md`
7. `docs/BOOK_STATUS.md`
8. all prerequisite chapters listed for this chapter
9. any existing draft at `chapters/<NN>-<slug>.md`
10. any existing review at `reviews/<NN>-<slug>-review.md`

Do not begin writing until you understand the chapter’s purpose, prerequisites, scope, and relationship to the rest of the book.

## Chapter Purpose

<PASTE THE CHAPTER TOPICS AND CORE QUESTION FROM THE BLUEPRINT>

## Work to Perform

### Pass A — Conceptual Structure

1. Define:
   - target learning outcomes;
   - prerequisite knowledge;
   - core mental model;
   - scope boundaries;
   - concepts explicitly deferred to other chapters.
2. Create or update:
   - `reviews/<NN>-<slug>-review.md`
3. Record the chapter plan before drafting.

### Pass B — Technical Draft and Accuracy Review

4. Draft or revise:
   - `chapters/<NN>-<slug>.md`
5. Follow the chapter template, but adapt headings when doing so improves the explanation.
6. Explain concepts from first principles.
7. Use at least one realistic, industry-neutral system example.
8. Include:
   - mechanism;
   - failure modes;
   - hidden assumptions;
   - trade-offs;
   - alternatives;
   - inappropriate use cases;
   - production implications;
   - product/business implications.
9. Use brief language/framework translations only when they clarify the transferable concept.
10. Research technical claims when necessary, preferring primary sources.
11. Update:
   - `references.md`
   - `glossary.md`
   as needed.

### Pass C — Learning-Quality Review

12. Review whether:
   - the mental model is memorable;
   - the progression is logical;
   - examples genuinely clarify the concept;
   - exercises test reasoning;
   - the mastery checklist is demanding enough;
   - the chapter avoids unnecessary jargon and repetition.
13. Revise weak sections.

### Pass D — Editorial Integration

14. Check:
   - terminology consistency;
   - duplication with existing chapters;
   - prerequisites;
   - internal links;
   - forward references;
   - scope boundaries.
15. Score every quality-rubric criterion with evidence.
16. Revise again if any criterion is below 3/5 or the average is below 4/5.
17. Update `book-manifest.json`, then regenerate `docs/BOOK_STATUS.md` with `python scripts/sync_book_status.py`.
18. Run `python scripts/validate_book.py` before presenting a candidate.

## Constraints

- Do not optimize for length.
- Do not add filler to appear comprehensive.
- Do not present patterns as universally correct.
- Do not fabricate sources, quotations, benchmarks, or production claims.
- Do not turn language examples into framework tutorials.
- Do not edit unrelated chapters unless necessary to fix a contradiction, broken link, or terminology inconsistency.
- Do not mark the chapter `Approved`; only a human may make the candidate-to-approved transition.
- When evidence is uncertain or context-dependent, say so explicitly.
- Keep advanced material connected to practical engineering decisions.

## Done When

The final response must report:

1. files created or changed;
2. final chapter status;
3. quality-rubric score for every criterion;
4. overall average;
5. strongest parts of the chapter;
6. unresolved weaknesses or questions;
7. cross-chapter changes made or recommended;
8. the single highest-value improvement for the next revision.
