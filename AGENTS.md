# AGENTS.md

## Project Mission

This repository contains a long-form Markdown ebook titled **Software Engineering Fundamentals**.

The book teaches durable, language-independent software engineering mental models to mid-level engineers who want to develop senior-level judgment across backend engineering, systems, architecture, reliability, platform engineering, and AI-assisted development.

The goal is not encyclopedic coverage or framework tutorials. The goal is accurate, practical, transferable engineering judgment.

## Source of Truth

Before planning or editing book content, read the relevant sections of:

- `docs/BOOK_BLUEPRINT.md`
- `docs/QUALITY_RUBRIC.md`
- `templates/CHAPTER_TEMPLATE.md`
- any earlier approved chapters referenced by the chapter being edited
- the corresponding review file in `reviews/`, when one exists

Do not copy the entire blueprint into chapter files. Use it as editorial guidance.

## Editorial Principles

Every chapter must:

1. teach mental models before tools;
2. explain the problem from first principles;
3. remain useful across languages and frameworks;
4. include realistic examples;
5. explain failure modes and hidden assumptions;
6. present trade-offs rather than universal prescriptions;
7. explain when not to use a technique;
8. connect technical choices to production, product, and business consequences;
9. include reasoning-based exercises;
10. end with a mastery checklist and high-quality further study.

Avoid:

- framework-specific recipes as the main teaching method;
- cargo-cult “best practices”;
- fake certainty;
- unnecessary academic detail;
- interview trivia without practical value;
- architecture-pattern worship;
- excessive headings, repetition, filler, or motivational prose;
- invented facts, citations, benchmarks, or quotations.

## Accuracy and Research

For technical claims that may depend on current specifications, library behavior, or evolving industry practice:

- prefer primary sources such as standards, RFCs, official documentation, original papers, and authoritative project documentation;
- distinguish stable computer-science principles from implementation-specific details;
- qualify claims when behavior depends on a runtime, database, framework, deployment model, or workload;
- never fabricate sources;
- add sources to `references.md` using a consistent Markdown format.

Do not turn chapters into literature reviews. Cite only where evidence adds value.

## Writing Style

Write for an experienced mid-level software engineer.

Use:

- precise but accessible English;
- complete sentences;
- concrete examples;
- explicit assumptions;
- diagrams in Mermaid or plain-text form when they improve understanding;
- consistent terminology across chapters.

Prefer explanation over slogans.

When introducing jargon:

1. define it;
2. explain why it exists;
3. show a concrete example;
4. explain trade-offs;
5. connect it to related concepts.

## Chapter Workflow

Do not attempt to write the entire book in one task.

For each chapter:

1. inspect the blueprint, template, quality rubric, and relevant earlier chapters;
2. create or update a chapter plan in `reviews/NN-chapter-slug-review.md`;
3. draft the chapter in `chapters/NN-chapter-slug.md`;
4. self-review it against every quality-rubric criterion;
5. record weaknesses, unresolved questions, duplicated material, and cross-reference opportunities in the review file;
6. revise the chapter until it reaches the quality threshold;
7. update `references.md` and `glossary.md` when needed;
8. do not mark a chapter approved unless the review file shows an average score of at least 4/5 and no criterion below 3/5.

## Scope Control

Before adding a section, ask:

- Is this necessary to achieve the chapter’s learning objectives?
- Is it explained more appropriately in another chapter?
- Does it deepen understanding or merely increase length?

Prefer cross-references over repeating full explanations.

Do not introduce advanced concepts before their prerequisites unless clearly labeled as a preview.

## Examples

Use a small set of recurring, industry-neutral examples when useful:

- collaborative project-management system;
- reservation or booking workflow;
- order and payment workflow;
- developer platform;
- background-processing system.

Examples should illustrate transferable patterns rather than make the book dependent on one industry.

## Language Translation Sections

When useful, briefly show how a concept appears in:

- TypeScript/Node.js;
- Python;
- Ruby/Rails;
- Go.

Keep these examples short. They are translations of the concept, not framework tutorials.

Code examples must be correct, focused, and free of irrelevant setup.

## Review Standard

Use `docs/QUALITY_RUBRIC.md`.

A chapter is not complete merely because it is long or polished.

It should be:

- accurate;
- first-principles driven;
- transferable;
- practical;
- explicit about trade-offs;
- aware of failure modes;
- well structured;
- clear;
- sufficiently deep;
- correctly scoped;
- verifiable through exercises;
- integrated with the rest of the book.

## File Conventions

- Chapters: `chapters/NN-kebab-case-title.md`
- Reviews: `reviews/NN-kebab-case-title-review.md`
- Exercises may remain inside chapters initially; move them to `exercises/` only if a separate workbook is created.
- Use relative Markdown links for internal cross-references.
- Keep heading hierarchy valid and consistent.
- Do not renumber chapters without updating all affected links and references.

## Changes and Reporting

After each task, report:

- files created or changed;
- major editorial decisions;
- quality-rubric scores;
- unresolved questions;
- recommended next action.

Do not modify unrelated chapters unless required to correct a contradiction, terminology issue, or broken cross-reference. If broader changes are needed, explain them first in the review file.
