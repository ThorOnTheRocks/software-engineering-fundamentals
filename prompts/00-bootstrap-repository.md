# Initial Codex Task — Bootstrap the Ebook Repository

## Goal

Initialize this repository as a rigorous, long-form Markdown ebook project titled **Software Engineering Fundamentals: A Durable Guide to Understanding, Building, and Operating Software Systems**.

The repository must support writing, reviewing, revising, and compiling the book one chapter at a time.

Do **not** draft the full book in this task.

## Context

The editorial source of truth is:

- `docs/BOOK_BLUEPRINT.md`

Persistent project instructions are:

- `AGENTS.md`

The chapter quality standard is:

- `docs/QUALITY_RUBRIC.md`

The required chapter structure is:

- `templates/CHAPTER_TEMPLATE.md`

Read all four files before making changes.

## Work to Perform

1. Inspect the repository and the four source files.
2. Create any missing base files:
   - `README.md`
   - `book.md`
   - `glossary.md`
   - `references.md`
   - `.gitignore`
3. Ensure these directories exist:
   - `chapters/`
   - `reviews/`
   - `exercises/`
   - `diagrams/`
   - `scripts/`
4. Create `docs/EDITORIAL_WORKFLOW.md` describing:
   - the chapter lifecycle;
   - the four review passes;
   - the approval threshold;
   - how cross-chapter reviews work;
   - how approved chapters are merged into `book.md`.
5. Create `docs/STYLE_GUIDE.md` covering:
   - voice and audience;
   - terminology;
   - headings;
   - code blocks;
   - Mermaid and text diagrams;
   - callouts;
   - citations and references;
   - internal links;
   - rules for concise language-translation sections.
6. Create `docs/BOOK_STATUS.md` containing:
   - all planned parts and chapters;
   - status for each chapter;
   - dependency notes;
   - review score;
   - last meaningful update;
   - next recommended action.
7. Create a small, deterministic script at `scripts/build_book.py` that:
   - discovers approved chapter files in numeric order;
   - combines them into `book.md`;
   - fails clearly if chapter numbering is duplicated;
   - does not modify individual chapters;
   - adds a generated-file notice to `book.md`.
8. Add a documented command to run the build script.
9. Do not add third-party dependencies unless genuinely necessary.
10. Do not draft Chapter 1 or any other chapter yet.

## Constraints

- Keep `AGENTS.md` concise and navigational; detailed guidance belongs in `docs/`.
- Do not duplicate the full blueprint across multiple files.
- Preserve the blueprint’s chapter titles and numbering unless a structural issue is found.
- If you find a structural issue, record it in `docs/EDITORIAL_WORKFLOW.md` under an “Open Editorial Questions” section rather than silently changing the plan.
- The build script must work with the standard Python library.
- Keep the setup understandable to a single author working with Codex.
- Avoid unnecessary automation and over-engineering.

## Done When

The task is complete when:

- the repository structure is ready for chapter-by-chapter authoring;
- all required editorial files exist and are internally consistent;
- the status tracker contains the complete chapter list;
- the book build script works on the current repository;
- no chapter has been prematurely drafted;
- the final response lists every file created or changed, any open editorial questions, and the recommended prompt to begin the first chapter.
