#!/usr/bin/env python3
"""Regenerate docs/BOOK_STATUS.md from the canonical book manifest."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from book_workflow import STATUS_PATH, load_manifest, render_status


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--check", action="store_true", help="check synchronization without writing")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    try:
        rendered = render_status(load_manifest(root))
        path = root / STATUS_PATH
        current = path.read_text(encoding="utf-8") if path.exists() else ""
        if args.check:
            if current != rendered:
                print(f"status projection is stale: {path}", file=sys.stderr)
                return 1
            print(f"status projection is synchronized: {path}")
            return 0
        path.write_text(rendered, encoding="utf-8", newline="\n")
    except (OSError, UnicodeError, ValueError) as error:
        print(f"status synchronization failed: {error}", file=sys.stderr)
        return 1
    print(f"updated {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
