#!/usr/bin/env python3
"""Build book.md from approved, numerically named chapter files."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CHAPTERS_DIR = ROOT / "chapters"
OUTPUT_PATH = ROOT / "book.md"
CHAPTER_NAME = re.compile(r"^(?P<number>\d{2})-(?P<slug>[a-z0-9]+(?:-[a-z0-9]+)*)\.md$")
APPROVED_MARKER = "> **Status:** Approved"
GENERATED_NOTICE = "<!-- GENERATED FILE: run python3 scripts/build_book.py; do not edit directly. -->"
BOOK_TITLE = "# Software Engineering Fundamentals\n\n*A Durable Guide to Understanding, Building, and Operating Software Systems*"


class BuildError(Exception):
    """A clear, expected build failure."""


def discover_chapters() -> list[tuple[int, Path, str]]:
    """Return approved chapters after validating all numeric chapter filenames."""
    if not CHAPTERS_DIR.is_dir():
        raise BuildError(f"chapter directory does not exist: {CHAPTERS_DIR}")

    seen_numbers: dict[int, Path] = {}
    approved: list[tuple[int, Path, str]] = []

    for path in sorted(CHAPTERS_DIR.glob("*.md"), key=lambda item: item.name):
        match = CHAPTER_NAME.fullmatch(path.name)
        if match is None:
            if path.name[:1].isdigit():
                raise BuildError(
                    f"invalid numeric chapter filename {path.name!r}; "
                    "expected NN-kebab-case-title.md"
                )
            continue

        number = int(match.group("number"))
        if number in seen_numbers:
            first = seen_numbers[number]
            raise BuildError(
                f"duplicate chapter number {number:02d}: {first.name} and {path.name}"
            )
        seen_numbers[number] = path

        content = path.read_text(encoding="utf-8").strip()
        if APPROVED_MARKER in content.splitlines():
            approved.append((number, path, content))

    return sorted(approved, key=lambda chapter: chapter[0])


def render_book(chapters: list[tuple[int, Path, str]]) -> str:
    sections = [GENERATED_NOTICE, BOOK_TITLE]
    if chapters:
        sections.extend(content for _, _, content in chapters)
    else:
        sections.append("_No chapters have been approved yet._")
    return "\n\n".join(sections) + "\n"


def main() -> int:
    try:
        chapters = discover_chapters()
        OUTPUT_PATH.write_text(render_book(chapters), encoding="utf-8", newline="\n")
    except (BuildError, OSError, UnicodeError) as error:
        print(f"build failed: {error}", file=sys.stderr)
        return 1

    noun = "chapter" if len(chapters) == 1 else "chapters"
    print(f"built {OUTPUT_PATH.name} from {len(chapters)} approved {noun}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
