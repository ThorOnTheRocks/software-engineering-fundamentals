---
name: ebook
description: Continues the Software Engineering Fundamentals ebook from repository evidence, selecting and executing the highest-priority valid editorial action without requiring a chapter number. Use when asked to continue, review, integrate, or autonomously advance this book until a human editorial gate.
---

# Autonomous Ebook Workflow

## Quick start

Normal invocation: `$ebook Continue the book autonomously until the next human decision is required.`

The main agent is the sole repository writer. Never delegate edits. Never draft, revise, approve, or integrate before state discovery identifies that exact action.

## Discover state first

1. Read `AGENTS.md`, `book-manifest.json`, `docs/CHAPTER_LIFECYCLE.md`, `docs/EDITORIAL_WORKFLOW.md`, and `docs/BOOK_STATUS.md`.
2. Run `python scripts/validate_book.py`. Inspect every reported inconsistency before content work.
3. Run `python scripts/next_book_action.py`. Treat its result as deterministic input, not unquestionable truth.
4. Inspect the target chapter/review and relevant blueprint, rubric, style guide, template, prerequisite chapters, glossary, references, and generated book.
5. Compare manifest state with actual plan, draft, findings, revisions, re-checks, validation, rubric, candidate, approval, and integration evidence.
6. Repair only unambiguous metadata drift. Escalate ambiguous or material conflicts.

The documented command name is `python`; when the host exposes the same Python 3 standard library only as `python3`, use that interpreter without changing workflow semantics.

## Selection order

Apply strictly: repository inconsistency; pending human gate; active incomplete work furthest through a valid lifecycle; approved-but-unintegrated work; then a new eligible chapter.

For a new chapter, honor explicit editorial priority, recommended writing priority, satisfied required dependencies, learning coherence, foundational value, and integration needs. Record selection reasoning in its review. Never select by number alone.

## Execute the recommended phase

- `begin_architecture`, `resume_architecture`, `evaluate_architecture`: plan/evaluate only; do not draft before `Architecture Ready`.
- `begin_drafting`, `resume_drafting`: draft from the approved architecture and record draft evidence.
- `complete_internal_review`: spawn the five project agents by name in bounded parallel, wait for all findings, then aggregate them in the review. Agents are read-only and return findings only.
- `resume_revision`: revise blocking/major findings, rerun only affected reviewers, and repeat for at most three major cycles.
- `human_approval_required`: prepare the candidate summary and exact decision request, then stop. Only a human may approve.
- `integrate_approved`: verify human evidence, validate, append the `Integrated` transition, synchronize status, rebuild `book.md`, and run full validation. Do not alter chapter prose.
- `begin_architecture`: start only after all higher-priority categories are empty.

Review agents: `technical-reviewer`, `pedagogy-reviewer`, `production-reviewer`, `continuity-editor`, and `source-verifier`. Run independent lenses in parallel; do not ask them to reconcile one another or edit files.

Before spawning reviewers, confirm their loaded configuration remains read-only and is not weakened by an active runtime override. If read-only execution cannot be guaranteed, stop and report the configuration gate.

## Evidence and synchronization

Follow `docs/CHAPTER_LIFECYCLE.md` exactly. Maintain the review's `ebook-workflow-evidence` JSON block and append manifest history on every state change. Never create `legacy_status_consensus`; it is migration-only.

After manifest changes, run `python scripts/sync_book_status.py`. After integration, run `python scripts/build_book.py`. Finish every mutation with `python scripts/validate_book.py` and re-run `python scripts/next_book_action.py`.

## Overrides

Accept topic priority, re-review, or stop-after-phase requests. Resolve a topic to a manifest stable ID, record a temporary editorial priority or explicit re-review rationale, and preserve all dependencies, legal transitions, reviews, validation, and human gates. An override never authorizes approval or a skipped phase.

## Stop conditions

Stop for candidate approval, cross-book architectural decisions, conflicting requirements, material reviewer disagreement, changes that could invalidate approved chapters, materially uncertain source evidence, or three unsuccessful major revision cycles. Resolve ordinary wording, local structure, example choice, and nonstrategic findings from repository guidance without asking.
