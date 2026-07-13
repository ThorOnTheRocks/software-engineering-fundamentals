#!/usr/bin/env python3
"""Report the deterministic highest-priority valid next editorial action."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

from book_workflow import discover_state, load_manifest, recommendation_text, recommend_next_action


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    try:
        manifest = load_manifest(root)
        evidence, issues = discover_state(root, manifest)
        recommendation = recommend_next_action(manifest, evidence, issues)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"state discovery failed: {error}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(asdict(recommendation), indent=2))
    else:
        print(recommendation_text(recommendation, manifest))
    return 2 if recommendation.action_type in {"resolve_inconsistency", "human_editorial_decision_required"} else 0


if __name__ == "__main__":
    raise SystemExit(main())
