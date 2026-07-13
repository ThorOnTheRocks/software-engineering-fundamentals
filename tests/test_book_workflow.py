from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from book_workflow import (  # noqa: E402
    Issue,
    REVIEWER_NAMES,
    discover_state,
    recommend_next_action,
    render_status,
)


class WorkflowScenarioTests(unittest.TestCase):
    def make_root(self, recorded_state: str, evidence_kind: str = "none", number: int = 1) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        for directory in ("chapters", "reviews", "docs", ".codex/agents", ".agents/skills/ebook"):
            (root / directory).mkdir(parents=True, exist_ok=True)
        (root / "README.md").write_text("# Fixture\n", encoding="utf-8")
        (root / "docs/EDITORIAL_WORKFLOW.md").write_text("# Editorial Workflow\n", encoding="utf-8")
        (root / "docs/CHAPTER_LIFECYCLE.md").write_text("# Chapter Lifecycle\n", encoding="utf-8")
        (root / "glossary.md").write_text("# Glossary\n", encoding="utf-8")
        (root / "references.md").write_text("# References\n", encoding="utf-8")
        (root / "book.md").write_text("# Fixture Book\n", encoding="utf-8")
        (root / ".codex/config.toml").write_text("[agents]\nmax_threads = 6\nmax_depth = 1\n", encoding="utf-8")
        for reviewer in REVIEWER_NAMES:
            (root / f".codex/agents/{reviewer}.toml").write_text(
                f'name = "{reviewer}"\n'
                f'description = "Fixture {reviewer}."\n'
                'sandbox_mode = "read-only"\n'
                'developer_instructions = "Return findings only."\n',
                encoding="utf-8",
            )
        (root / ".agents/skills/ebook/SKILL.md").write_text(
            "---\nname: ebook\ndescription: Fixture autonomous ebook workflow.\n---\n\n# Ebook\n",
            encoding="utf-8",
        )

        gate_status = "pending" if recorded_state == "Candidate for Human Approval" else (
            "satisfied" if recorded_state in {"Approved", "Integrated"} else "not_required"
        )
        score = 4.2 if recorded_state in {"Candidate for Human Approval", "Approved", "Integrated"} else None
        chapter = {
            "id": "fixture-topic",
            "number": number,
            "title": "Fixture Topic",
            "part": "Part I — Fixture",
            "recommended_writing_priority": 1,
            "dependencies": [],
            "advisory_dependencies": [],
            "current_lifecycle_state": recorded_state,
            "expected_chapter_path": f"chapters/{number:02d}-fixture-topic.md",
            "expected_review_path": f"reviews/{number:02d}-fixture-topic-review.md",
            "review_score": score,
            "last_meaningful_update": "2026-07-13" if score else None,
            "human_gate": {"status": gate_status, "evidence_kind": None, "evidence": None},
            "editorial_priority": None,
            "lifecycle_history": [
                {"state": recorded_state, "date": "2026-07-13", "actor": "migration", "evidence": "Fixture baseline."}
            ],
        }
        manifest = {
            "schema_version": "1.0.0",
            "book": {
                "id": "fixture-book",
                "title": "Fixture Book",
                "version": "0.1",
                "status": "In Progress",
                "last_meaningful_update": "2026-07-13",
                "current_focus": "Fixture",
            },
            "chapters": [chapter],
        }
        (root / "book-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        (root / "docs/BOOK_STATUS.md").write_text(render_status(manifest), encoding="utf-8")
        self.write_artifacts(root, manifest, evidence_kind)
        return root

    def workflow_data(self, kind: str) -> dict[str, object]:
        data: dict[str, object] = {
            "schema_version": 1,
            "architecture": {"plan": "complete", "evaluation": "complete"},
            "draft": {"status": "in_progress"},
            "revision": {"major_cycles": 0, "unresolved_blocking": 0, "unresolved_major": 0},
        }
        if kind in {"draft_complete", "internal_review", "revision", "candidate", "approved", "integrated"}:
            data["draft"] = {"status": "complete"}
        if kind in {"internal_review", "revision", "candidate", "approved", "integrated"}:
            data["reviews"] = {
                "cycle": 1,
                **{name: {"status": "complete"} for name in REVIEWER_NAMES},
            }
        if kind == "revision":
            data["revision"] = {"major_cycles": 1, "unresolved_blocking": 0, "unresolved_major": 2}
        if kind in {"candidate", "approved", "integrated"}:
            data.update(
                {
                    "validation": {"status": "passed", "command": "python scripts/validate_book.py", "date": "2026-07-13"},
                    "rubric": {"status": "complete", "average": 4.2, "minimum": 3.0},
                    "candidate_summary": {"status": "complete"},
                    "human_approval": {"decision": "pending", "actor": "human", "date": None},
                }
            )
        if kind in {"approved", "integrated"}:
            data["human_approval"] = {"decision": "approved", "actor": "human", "date": "2026-07-13"}
        return data

    def write_artifacts(self, root: Path, manifest: dict[str, object], kind: str) -> None:
        if kind == "none":
            return
        chapter = manifest["chapters"][0]
        recorded = chapter["current_lifecycle_state"]
        metadata_state = "Approved" if recorded == "Integrated" else recorded
        review = (
            "# Fixture Topic Review\n\n"
            f"> **Status:** {metadata_state}\n\n"
            "<!-- ebook-workflow-evidence\n"
            + json.dumps(self.workflow_data(kind), indent=2)
            + "\n-->\n"
        )
        (root / chapter["expected_review_path"]).write_text(review, encoding="utf-8")
        if kind == "architecture":
            return
        chapter_text = (
            f"# Chapter {chapter['number']:02d} — Fixture Topic\n\n"
            f"> **Status:** {metadata_state}\n\n"
            "## Learning Objectives\n\nReason about the fixture.\n\n"
            "## Exercises\n\nExplain the fixture.\n\n"
            "## Mastery Checklist\n\n- [ ] Explain the fixture.\n\n"
            "## Further Study\n\nUse repository guidance.\n"
        )
        (root / chapter["expected_chapter_path"]).write_text(chapter_text, encoding="utf-8")
        if kind == "integrated":
            (root / "book.md").write_text(
                f"# Fixture Book\n\n<!-- BEGIN CHAPTER: {chapter['id']} -->\n\n"
                f"{chapter_text.strip()}\n\n<!-- END CHAPTER: {chapter['id']} -->\n",
                encoding="utf-8",
            )

    def recommendation_for(self, state: str, kind: str, number: int = 1):
        root = self.make_root(state, kind, number)
        manifest = json.loads((root / "book-manifest.json").read_text(encoding="utf-8"))
        evidence, issues = discover_state(root, manifest)
        self.assertEqual([], issues)
        return evidence[0], recommend_next_action(manifest, evidence, issues)

    def test_no_existing_work_begins_architecture_without_number_rule(self) -> None:
        evidence, recommendation = self.recommendation_for("Planned", "none", number=47)
        self.assertEqual("Planned", evidence.justified_state)
        self.assertEqual("begin_architecture", recommendation.action_type)
        self.assertEqual("fixture-topic", recommendation.chapter_id)

    def test_architecture_only_begins_drafting(self) -> None:
        evidence, recommendation = self.recommendation_for("Architecture Ready", "architecture")
        self.assertEqual("Architecture Ready", evidence.justified_state)
        self.assertEqual("begin_drafting", recommendation.action_type)

    def test_incomplete_draft_resumes_drafting(self) -> None:
        evidence, recommendation = self.recommendation_for("Drafting", "draft_incomplete")
        self.assertEqual("Drafting", evidence.justified_state)
        self.assertEqual("resume_drafting", recommendation.action_type)

    def test_internal_review_continues_review(self) -> None:
        evidence, recommendation = self.recommendation_for("Internal Review", "internal_review")
        self.assertEqual("Internal Review", evidence.justified_state)
        self.assertEqual("complete_internal_review", recommendation.action_type)

    def test_revision_required_resumes_revision(self) -> None:
        evidence, recommendation = self.recommendation_for("Revision Required", "revision")
        self.assertEqual("Revision Required", evidence.justified_state)
        self.assertEqual("resume_revision", recommendation.action_type)

    def test_candidate_stops_at_human_gate(self) -> None:
        evidence, recommendation = self.recommendation_for("Candidate for Human Approval", "candidate")
        self.assertEqual("Candidate for Human Approval", evidence.justified_state)
        self.assertEqual("human_approval_required", recommendation.action_type)

    def test_approved_unintegrated_is_selected_for_integration(self) -> None:
        evidence, recommendation = self.recommendation_for("Approved", "approved")
        self.assertEqual("Approved", evidence.justified_state)
        self.assertEqual("integrate_approved", recommendation.action_type)

    def test_fully_integrated_chapter_completes_fixture_book(self) -> None:
        evidence, recommendation = self.recommendation_for("Integrated", "integrated")
        self.assertEqual("Integrated", evidence.justified_state)
        self.assertEqual("book_complete", recommendation.action_type)

    def test_inconsistent_manifest_and_artifacts_are_priority_one(self) -> None:
        root = self.make_root("Planned", "draft_incomplete")
        manifest = json.loads((root / "book-manifest.json").read_text(encoding="utf-8"))
        evidence, issues = discover_state(root, manifest)
        self.assertEqual("Drafting", evidence[0].justified_state)
        self.assertTrue(any(issue.code == "state.evidence_mismatch" for issue in issues))
        recommendation = recommend_next_action(manifest, evidence, issues)
        self.assertIn(recommendation.action_type, {"repair_metadata", "resolve_inconsistency"})

    def test_automated_candidate_to_approved_transition_is_rejected(self) -> None:
        root = self.make_root("Approved", "approved")
        manifest = json.loads((root / "book-manifest.json").read_text(encoding="utf-8"))
        manifest["chapters"][0]["lifecycle_history"] = [
            {"state": "Candidate for Human Approval", "date": "2026-07-12", "actor": "workflow", "evidence": "Candidate."},
            {"state": "Approved", "date": "2026-07-13", "actor": "workflow", "evidence": "Invalid automation."},
        ]
        (root / "book-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        (root / "docs/BOOK_STATUS.md").write_text(render_status(manifest), encoding="utf-8")
        _, issues = discover_state(root, manifest)
        self.assertTrue(any(issue.code == "history.automated_approval" for issue in issues))


if __name__ == "__main__":
    unittest.main()
