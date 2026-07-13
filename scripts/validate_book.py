#!/usr/bin/env python3
"""Validate manifest, workflow evidence, Markdown, references, and build state."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from book_workflow import discover_state, load_manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    return parser.parse_args()


def main() -> int:
    root = parse_args().root.resolve()
    try:
        manifest = load_manifest(root)
        evidence, issues = discover_state(root, manifest)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"VALIDATION FAILED\n- {error}", file=sys.stderr)
        return 1

    if issues:
        print(f"VALIDATION FAILED ({len(issues)} issue{'s' if len(issues) != 1 else ''})", file=sys.stderr)
        for issue in issues:
            repair = " [metadata repair is unambiguous]" if issue.repairable else ""
            print(f"- [{issue.code}] {issue.message}{repair}", file=sys.stderr)
        return 1

    states: dict[str, int] = {}
    for item in evidence:
        states[item.justified_state] = states.get(item.justified_state, 0) + 1
    summary = ", ".join(f"{state}: {count}" for state, count in states.items())
    print(f"VALIDATION PASSED: {len(evidence)} chapters; {summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
