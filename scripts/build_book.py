#!/usr/bin/env python3
"""Build book.md from chapters explicitly marked Integrated in the manifest."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CHAPTERS_DIR = ROOT / "chapters"
OUTPUT_PATH = ROOT / "book.md"
CHAPTER_NAME = re.compile(r"^(?P<number>\d{2})-(?P<slug>[a-z0-9]+(?:-[a-z0-9]+)*)\.md$")
APPROVED_MARKER = "> **Status:** Approved"
GENERATED_NOTICE = "<!-- GENERATED FILE: run python scripts/build_book.py; do not edit directly. -->"
BOOK_TITLE = "# Software Engineering Fundamentals\n\n*A Durable Guide to Understanding, Building, and Operating Software Systems*"
MANIFEST_PATH = ROOT / "book-manifest.json"


class BuildError(Exception):
    """A clear, expected build failure."""


def load_integrated_manifest_chapters() -> dict[str, dict[str, object]]:
    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise BuildError(f"cannot load {MANIFEST_PATH.name}: {error}") from error
    chapters = manifest.get("chapters")
    if not isinstance(chapters, list):
        raise BuildError("manifest chapters must be an array")
    integrated: dict[str, dict[str, object]] = {}
    for chapter in chapters:
        if not isinstance(chapter, dict) or not isinstance(chapter.get("id"), str):
            raise BuildError("every manifest chapter must be an object with a stable id")
        if chapter.get("current_lifecycle_state") == "Integrated":
            integrated[str(chapter["expected_chapter_path"])] = chapter
    return integrated


def discover_chapters() -> list[tuple[int, str, Path, str]]:
    """Return integrated chapters after validating manifest and source metadata."""
    if not CHAPTERS_DIR.is_dir():
        raise BuildError(f"chapter directory does not exist: {CHAPTERS_DIR}")

    seen_numbers: dict[int, Path] = {}
    integrated_manifest = load_integrated_manifest_chapters()
    integrated: list[tuple[int, str, Path, str]] = []

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
        relative_path = str(path.relative_to(ROOT))
        if relative_path in integrated_manifest:
            chapter = integrated_manifest.pop(relative_path)
            if APPROVED_MARKER not in content.splitlines():
                raise BuildError(f"integrated chapter lacks Approved metadata: {path.name}")
            if chapter.get("number") != number:
                raise BuildError(f"manifest number does not match filename for {path.name}")
            integrated.append((number, str(chapter["id"]), path, content))

    if integrated_manifest:
        missing = ", ".join(sorted(integrated_manifest))
        raise BuildError(f"integrated manifest chapters are missing source files: {missing}")

    return sorted(integrated, key=lambda chapter: chapter[0])


def render_book(chapters: list[tuple[int, str, Path, str]]) -> str:
    sections = [GENERATED_NOTICE, BOOK_TITLE]
    if chapters:
        for _, chapter_id, _, content in chapters:
            sections.append(
                f"<!-- BEGIN CHAPTER: {chapter_id} -->\n\n{content}\n\n<!-- END CHAPTER: {chapter_id} -->"
            )
    else:
        sections.append("_No chapters have been integrated yet._")
    return "\n\n".join(sections) + "\n"


def main() -> int:
    try:
        chapters = discover_chapters()
        OUTPUT_PATH.write_text(render_book(chapters), encoding="utf-8", newline="\n")
    except (BuildError, OSError, UnicodeError) as error:
        print(f"build failed: {error}", file=sys.stderr)
        return 1

    noun = "chapter" if len(chapters) == 1 else "chapters"
    print(f"built {OUTPUT_PATH.name} from {len(chapters)} integrated {noun}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
