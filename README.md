# Software Engineering Fundamentals

**Software Engineering Fundamentals: A Durable Guide to Understanding, Building, and Operating Software Systems** is a long-form Markdown ebook for mid-level engineers developing senior-level judgment across software design, systems, reliability, architecture, delivery, and AI-assisted development.

The book is authored, reviewed, approved, and integrated one chapter at a time. [The book blueprint](docs/BOOK_BLUEPRINT.md) owns the intellectual architecture, [the machine-readable manifest](book-manifest.json) owns workflow state, and [the book status](docs/BOOK_STATUS.md) is the generated human-readable projection.

## Authoring workflow

Before working on a chapter, read:

1. [AGENTS.md](AGENTS.md)
2. [the book blueprint](docs/BOOK_BLUEPRINT.md)
3. [the quality rubric](docs/QUALITY_RUBRIC.md)
4. [the chapter template](templates/CHAPTER_TEMPLATE.md)
5. [the style guide](docs/STYLE_GUIDE.md)
6. [the editorial workflow](docs/EDITORIAL_WORKFLOW.md)
7. [the book status](docs/BOOK_STATUS.md)

The canonical workflow is repository-native and does not require a chapter number:

```text
$ebook Continue the book autonomously until the next human decision is required.
```

It validates repository evidence, selects the highest-priority legal action, resumes existing work, runs read-only specialist reviewers, and stops at human gates. The prompts under `prompts/` remain manual references for targeted work but do not replace the lifecycle or human approval gate.

Chapter files belong in `chapters/`; their plans, evidence, scores, and decisions belong in `reviews/`. Exercises remain in chapters unless a separate workbook is intentionally created.

## Build the book

The build uses only the Python standard library:

```sh
python scripts/build_book.py
```

The script selects chapters whose manifest state is `Integrated`, verifies their source metadata is `Approved`, orders them numerically, and regenerates `book.md`. It rejects missing or duplicate chapter numbers and never modifies source chapters. Do not edit `book.md` directly.

Inspect and validate workflow state with:

```sh
python scripts/next_book_action.py
python scripts/validate_book.py
```

The canonical command name is `python`; on hosts that expose Python 3 only as `python3`, substitute that executable.

## Repository map

- `chapters/`: individual chapter sources
- `reviews/`: chapter plans and review records
- `exercises/`: reserved for a possible separate workbook
- `diagrams/`: shared diagram assets that cannot live inline
- `docs/`: architecture, standards, workflow, and status
- `templates/`: reusable content structures
- `prompts/`: repeatable Codex tasks
- `scripts/`: small, dependency-free project automation
- `.agents/skills/ebook/`: canonical autonomous editorial workflow
- `.codex/agents/`: read-only specialist reviewer definitions
- `book-manifest.json`: canonical machine-readable workflow index
- `glossary.md`: canonical definitions used across chapters
- `references.md`: sources cited by the book
- `book.md`: generated compilation of integrated chapters
