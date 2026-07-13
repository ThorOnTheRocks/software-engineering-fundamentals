# Chapter Lifecycle

This document defines the evidence-backed lifecycle used by the autonomous editorial workflow. `book-manifest.json` records the current state; repository artifacts must justify it. A filename, word count, or polished appearance never proves phase completion.

## Evidence record

New review files must include one machine-readable block. The main agent is the only process allowed to update it.

```markdown
<!-- ebook-workflow-evidence
{
  "schema_version": 1,
  "architecture": {"plan": "complete", "evaluation": "complete"},
  "draft": {"status": "complete"},
  "reviews": {
    "cycle": 1,
    "technical-reviewer": {"status": "complete"},
    "pedagogy-reviewer": {"status": "complete"},
    "production-reviewer": {"status": "complete"},
    "continuity-editor": {"status": "complete"},
    "source-verifier": {"status": "complete"}
  },
  "revision": {"major_cycles": 1, "unresolved_blocking": 0, "unresolved_major": 0},
  "validation": {"status": "passed", "command": "python scripts/validate_book.py", "date": "YYYY-MM-DD"},
  "rubric": {"status": "complete", "average": 4.2, "minimum": 3.0},
  "candidate_summary": {"status": "complete"},
  "human_approval": {"decision": "pending", "actor": "human", "date": null}
}
-->
```

The surrounding review prose owns the evidence itself: plan, reviewer findings, revision log, score rationales, validation result, candidate summary, and human decision. The JSON block is an index, not a substitute. Reviewer agents return findings; they never edit this block or any repository file.

## Planned

Required evidence: the blueprint contains the chapter and the manifest contains its stable ID, title, part, paths, priorities, dependencies, and initial history entry.

Required artifacts: `book-manifest.json`. A review file may exist while architecture is being developed, but the state remains `Planned` until the plan is both complete and evaluated.

Legal next state: `Architecture Ready`.

Prohibited transitions: directly to drafting, review, candidate, approval, or integration. Chapter prose must not begin before architecture evidence exists.

Validation: dependencies reference stable IDs; paths and numbering are unique; any partial review plan is treated as resumable active work.

## Architecture Ready

Required evidence: the review records purpose, prerequisites, learning outcomes, core mental model, scope boundaries, deferrals, example strategy, cross-chapter relationships, risks, selection reasoning, and an explicit architecture evaluation against the blueprint and rubric.

Required artifacts: the expected review file and completed `architecture.plan` and `architecture.evaluation` evidence.

Legal next states: `Drafting`; backward to `Planned` when architecture evidence is withdrawn.

Prohibited transitions: directly to review, candidate, approval, or integration.

Validation: no chapter prose is required; architecture must resolve or escalate material conceptual conflicts before drafting.

## Drafting

Required evidence: an architecture-ready review and a chapter source whose metadata says `Drafting`. Draft completion requires substantive content satisfying the architecture obligations; existence alone is not completion.

Required artifacts: expected review and chapter files; updated `draft` evidence when the full draft is ready.

Legal next states: `Internal Review`, `Revision Required`, or back to `Architecture Ready` after a structural invalidation.

Prohibited transitions: directly to candidate, approval, or integration.

Validation: expected filename and H1, valid heading hierarchy, no unresolved template placeholders at review entry, and no chapter without a review.

## Internal Review

Required evidence: a complete draft plus independent findings from the technical, pedagogy, production, continuity, and source reviewers. Each finding records severity, location, rationale, and a concrete recommendation.

Required artifacts: chapter, review, five reviewer result sections, aggregated findings, and a review-cycle number.

Legal next states: `Revision Required`, `Candidate for Human Approval`, or back to `Drafting` when review exposes an incomplete draft.

Prohibited transitions: directly to approval or integration.

Validation: every reviewer is read-only; the main agent records findings; missing reviewer results prevent advancement.

## Revision Required

Required evidence: at least one unresolved blocking/major finding, a below-threshold rubric result, a failed material validation, or an explicit restructuring decision. The review records the issue and affected review lenses.

Required artifacts: chapter and review, with unresolved counts and revision-cycle history.

Legal next states: `Drafting`, `Internal Review`, or `Architecture Ready` if the architecture must change.

Prohibited transitions: directly to candidate, approval, or integration. Standards must not be lowered after repeated cycles.

Validation: after each revision, rerun affected reviewers. After three unsuccessful major cycles, remain `Revision Required`, record unresolved issues, and stop with a focused blocker report.

## Candidate for Human Approval

Required evidence: all five reviewer results, no unresolved blocking or major findings, deterministic validation passed, twelve evidence-backed rubric scores averaging at least 4.0 with no score below 3.0, completed revision log, and a concise candidate summary.

Required artifacts: final chapter, complete review, glossary/references as needed, candidate package, `human_gate.status = pending`, and a `human_approval` record whose decision is `pending`.

Legal next states: `Approved` only by a human; `Revision Required` when the human requests changes or new evidence invalidates the candidate.

Prohibited transitions: automated approval, unrelated new chapter work, or integration.

Validation: candidate evidence must be explicit. Length, polish, a filename, or a numerical score without rationale is insufficient.

## Approved

Required evidence: the complete candidate evidence plus an explicit human decision recorded as `human_approval.decision = approved`, `actor = human`, and a date. The manifest history entry for `Candidate for Human Approval → Approved` must also name `actor = human`.

Required artifacts: approved chapter and review metadata, satisfied human gate, approval evidence, and a threshold-passing review.

Legal next states: `Integrated`; exceptionally `Revision Required` after a human editorial decision or material invalidation.

Prohibited transitions: automated creation of approval evidence, bypassing validation, or silently changing approved content during integration.

Validation: approval evidence must be repository evidence, not an agent assertion. Chapter 02 alone uses the migration-only `legacy_status_consensus` baseline adopted from the pre-manifest repository; the workflow must never create that evidence kind for new approvals.

## Integrated

Required evidence: valid approval, successful pre-integration validation, chapter inclusion between stable-ID markers in generated `book.md`, updated cross-references/status where required, and successful full validation after the build.

Required artifacts: approved chapter and review, manifest state/history, synchronized `docs/BOOK_STATUS.md`, and regenerated `book.md`.

Legal next state: `Revision Required` only after a human decision or a material validation failure that invalidates the approved text.

Prohibited transitions: editing `book.md` directly, integrating a candidate, or changing chapter prose as an incidental integration step.

Validation: build order follows manifest chapter numbers; only `Integrated` chapters appear; source text and generated content must match.

## State reconciliation

At invocation start, infer the most advanced state justified by evidence and compare it with the manifest, status projection, metadata, and lifecycle history.

- Repair metadata automatically only when repository evidence makes the correction unique, then validate again.
- Do not advance state merely because a later-looking artifact exists.
- Treat ambiguous conflicts, material source uncertainty, or changes affecting approved chapters as human gates.
- Never manufacture evidence to make recorded state pass validation.
- Append every state change to `lifecycle_history`; never rewrite the historical path to conceal an invalid transition.
