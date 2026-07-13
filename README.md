# Software Engineering Fundamentals

**Software Engineering Fundamentals: A Durable Guide to Understanding, Building, and Operating Software Systems** is a long-form Markdown ebook for mid-level engineers developing senior-level judgment across software design, systems, reliability, architecture, delivery, and AI-assisted development.

The book is authored and approved one chapter at a time. Its editorial source of truth is [the book blueprint](docs/BOOK_BLUEPRINT.md), and current progress is tracked in [the book status](docs/BOOK_STATUS.md).

## Authoring workflow

Before working on a chapter, read:

1. [AGENTS.md](AGENTS.md)
2. [the book blueprint](docs/BOOK_BLUEPRINT.md)
3. [the quality rubric](docs/QUALITY_RUBRIC.md)
4. [the chapter template](templates/CHAPTER_TEMPLATE.md)
5. [the style guide](docs/STYLE_GUIDE.md)
6. [the editorial workflow](docs/EDITORIAL_WORKFLOW.md)
7. [the book status](docs/BOOK_STATUS.md)

Use [the chapter-authoring prompt](prompts/chapter-authoring-template.md) for one chapter at a time. Use [the independent-review prompt](prompts/independent-review-template.md) in a separate Codex thread when a draft needs an adversarial review.

Chapter files belong in `chapters/`; their plans, evidence, scores, and decisions belong in `reviews/`. Exercises remain in chapters unless a separate workbook is intentionally created.

## Build the book

The build uses only the Python standard library:

```sh
python3 scripts/build_book.py
```

The script selects chapter files whose metadata contains the exact line `> **Status:** Approved`, orders them numerically, and regenerates `book.md`. It rejects duplicate chapter numbers and never modifies source chapters. Do not edit `book.md` directly.

## Repository map

- `chapters/`: individual chapter sources
- `reviews/`: chapter plans and review records
- `exercises/`: reserved for a possible separate workbook
- `diagrams/`: shared diagram assets that cannot live inline
- `docs/`: architecture, standards, workflow, and status
- `templates/`: reusable content structures
- `prompts/`: repeatable Codex tasks
- `scripts/`: small, dependency-free project automation
- `glossary.md`: canonical definitions used across chapters
- `references.md`: sources cited by the book
- `book.md`: generated compilation of approved chapters
# software-engineering-fundamentals
