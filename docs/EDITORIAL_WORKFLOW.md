# Editorial Workflow

This document turns the principles in [the book blueprint](BOOK_BLUEPRINT.md) and [quality rubric](QUALITY_RUBRIC.md) into a repeatable chapter workflow. `AGENTS.md` remains the concise project entrypoint; this document owns the operational detail.

## Chapter lifecycle

Each chapter moves through these states:

1. **Planned** — the blueprint defines the chapter, but no chapter-specific review plan exists.
2. **Planning** — `reviews/NN-slug-review.md` records purpose, prerequisites, learning outcomes, scope boundaries, deferred concepts, and risks.
3. **Draft** — `chapters/NN-slug.md` exists and is undergoing the four review passes.
4. **Revision Required** — review found blocking work or the approval threshold has not been met.
5. **Approved** — every approval condition is satisfied and both the chapter and review metadata say `Approved`.

Update [the status tracker](BOOK_STATUS.md) after any meaningful state change. Dates use ISO `YYYY-MM-DD`. A score is blank until all twelve rubric criteria have evidence-backed scores.

Do not create chapter prose before the planning record establishes boundaries. A chapter can move backward whenever later review exposes a substantive problem.

## Four review passes

### Pass A — Conceptual structure

Confirm that the chapter teaches the right problem in a defensible order. Record its purpose, prerequisites, core mental model, learning outcomes, scope boundaries, explicitly deferred concepts, example plan, and cross-chapter relationships in its review file before drafting.

### Pass B — Technical quality

Check claims, mechanisms, assumptions, examples, trade-offs, alternatives, inappropriate uses, and production failure modes. Qualify runtime-, database-, vendor-, and workload-dependent behavior. Research evolving or contestable claims from primary sources and add only cited material to `references.md`.

### Pass C — Learning quality

Test whether the mental model is memorable and whether the progression helps an experienced mid-level engineer reason rather than memorize. Exercises must cover explanation, diagnosis, and design. Remove filler, premature jargon, and language translations that do not clarify a transferable idea.

### Pass D — Editorial integration

Check terminology against `glossary.md`, prerequisites, internal links, duplication, forward references, and alignment with the blueprint. Score all twelve rubric criteria with evidence in the review file. Update the status tracker and shared references or glossary entries when needed.

An independent review may be run after self-review, especially for foundational or high-risk chapters. Its findings are recorded in the same review file and do not replace the chapter author's evidence.

## Approval threshold

A chapter may be marked `Approved` only when:

- its average rubric score is at least **4.0/5**;
- no individual criterion is below **3/5**;
- all accuracy concerns and placeholders are resolved;
- required references and cross-links exist;
- the review file records final scores, evidence, completed revisions, and any non-blocking improvements;
- chapter and review metadata both say `Approved`.

The twelve criteria are Accuracy, First principles, Transferability, Practicality, Trade-offs, Failure awareness, Structure, Clarity, Depth, Scope, Verification, and Integration. Length and polish do not substitute for evidence against them.

## Cross-chapter review

After every three to five approved chapters, review the set as a learning path:

1. identify repeated explanations and choose a canonical home;
2. standardize terms and update `glossary.md`;
3. verify prerequisites occur before dependent explanations or are clearly marked as previews;
4. add or repair relative cross-links;
5. check recurring examples for contradictory domain rules;
6. update dependency notes and next actions in `BOOK_STATUS.md`;
7. record any proposed structural change before renumbering or moving content.

Prefer cross-references over copying explanations. Do not silently revise the blueprint's chapter sequence during this pass.

## Merging approved chapters into `book.md`

Run:

```sh
python3 scripts/build_book.py
```

The build script treats an exact `> **Status:** Approved` line in chapter metadata as the machine-readable inclusion marker. Setting that marker is an editorial action and is permitted only after the corresponding review satisfies the threshold. The script checks all numerically named chapter files for duplicate numbers, then concatenates approved chapters in ascending order and replaces `book.md` with a generated artifact. It does not modify chapter sources.

Commit chapter sources and their review records as the durable editorial history. Treat `book.md` as reproducible output and never make chapter edits there.

## Open Editorial Questions

1. **Drafting order:** the blueprint recommends beginning with Chapter 2 and establishing the central technical voice before writing Chapter 1. The numbered order remains unchanged, but the author should confirm whether to follow that suggested drafting sequence.
2. **Review filename example:** the blueprint's recommended tree uses examples such as `chapter-02-review.md`, while `AGENTS.md` requires `reviews/NN-kebab-case-title-review.md`. The repository uses the binding `AGENTS.md` convention.
3. **Part dividers in the compiled book:** the current build concatenates approved chapters and does not synthesize part-title pages. Add a small manifest or chapter-to-part mapping only if part dividers become necessary for the reading artifact.

None of these questions blocks chapter planning or drafting.
