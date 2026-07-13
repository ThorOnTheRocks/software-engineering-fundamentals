#!/usr/bin/env python3
"""Shared, deterministic state discovery for the autonomous ebook workflow."""

from __future__ import annotations

import json
import re
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parent.parent
MANIFEST_NAME = "book-manifest.json"
STATUS_PATH = Path("docs/BOOK_STATUS.md")
BOOK_PATH = Path("book.md")
LIFECYCLE_STATES = (
    "Planned",
    "Architecture Ready",
    "Drafting",
    "Internal Review",
    "Revision Required",
    "Candidate for Human Approval",
    "Approved",
    "Integrated",
)
STATE_RANK = {state: index for index, state in enumerate(LIFECYCLE_STATES)}
LEGAL_TRANSITIONS = {
    "Planned": {"Architecture Ready"},
    "Architecture Ready": {"Drafting", "Planned"},
    "Drafting": {"Internal Review", "Revision Required", "Architecture Ready"},
    "Internal Review": {"Revision Required", "Candidate for Human Approval", "Drafting"},
    "Revision Required": {"Drafting", "Internal Review", "Architecture Ready"},
    "Candidate for Human Approval": {"Approved", "Revision Required"},
    "Approved": {"Integrated", "Revision Required"},
    "Integrated": {"Revision Required"},
}
CHAPTER_FILE = re.compile(r"^(?P<number>\d{2})-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
REVIEW_FILE = re.compile(r"^(?P<number>\d{2})-[a-z0-9]+(?:-[a-z0-9]+)*-review\.md$")
STATUS_MARKER = re.compile(r"^> \*\*Status:\*\* (?P<status>.+?)\s*$", re.MULTILINE)
SCORE_PATTERN = re.compile(
    r"(?:Post-revision quality score|Post-revision score|Average):\*\*?\s*(?P<score>[0-5](?:\.\d+)?)/5",
    re.IGNORECASE,
)
WORKFLOW_EVIDENCE = re.compile(
    r"<!--\s*ebook-workflow-evidence\s*\n(?P<json>\{.*?\})\s*\n-->", re.DOTALL
)
URL_PATTERN = re.compile(r"\[[^\]]+\]\((?P<target>[^)]+)\)")
EXTERNAL_URL = re.compile(r"https?://[^\s)>]+")
PLACEHOLDER_PATTERNS = (
    re.compile(r"\b(?:TODO|FIXME|TBD)\b"),
    re.compile(r"\bTo be determined\b", re.IGNORECASE),
    re.compile(r"<(?:(?:NN|CHAPTER TITLE)|[A-Z][A-Z _-]{2,})>"),
    re.compile(r"\{\{[^{}]+\}\}"),
)
RUBRIC_CRITERIA = (
    "Accuracy",
    "First principles",
    "Transferability",
    "Practicality",
    "Trade-offs",
    "Failure awareness",
    "Structure",
    "Clarity",
    "Depth",
    "Scope",
    "Verification",
    "Integration",
)
REVIEWER_NAMES = (
    "technical-reviewer",
    "pedagogy-reviewer",
    "production-reviewer",
    "continuity-editor",
    "source-verifier",
)


@dataclass(frozen=True)
class Issue:
    code: str
    message: str
    repairable: bool = False


@dataclass
class ChapterEvidence:
    chapter: dict[str, Any]
    chapter_path: Path
    review_path: Path
    chapter_exists: bool = False
    review_exists: bool = False
    chapter_text: str = ""
    review_text: str = ""
    chapter_status: str | None = None
    review_status: str | None = None
    structured: dict[str, Any] = field(default_factory=dict)
    architecture_plan: bool = False
    architecture_evaluated: bool = False
    draft_complete: bool = False
    internal_review_complete: bool = False
    unresolved_blocking: int = 0
    unresolved_major: int = 0
    revision_required: bool = False
    candidate_package: bool = False
    human_approval: bool = False
    integrated: bool = False
    review_score: float | None = None
    justified_state: str = "Planned"


@dataclass(frozen=True)
class Recommendation:
    action_type: str
    chapter_id: str | None
    justified_state: str | None
    reason: str
    required_artifacts: tuple[str, ...] = ()


def load_manifest(root: Path = ROOT) -> dict[str, Any]:
    path = root / MANIFEST_NAME
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ValueError(f"missing manifest: {path}") from error
    except json.JSONDecodeError as error:
        raise ValueError(f"invalid JSON in {path}: {error}") from error
    if not isinstance(value, dict):
        raise ValueError(f"manifest root must be an object: {path}")
    return value


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def _status(text: str) -> str | None:
    match = STATUS_MARKER.search(text)
    return match.group("status").strip() if match else None


def _structured_evidence(text: str) -> dict[str, Any]:
    match = WORKFLOW_EVIDENCE.search(text)
    if not match:
        return {}
    try:
        value = json.loads(match.group("json"))
    except json.JSONDecodeError:
        return {"_parse_error": True}
    return value if isinstance(value, dict) else {"_parse_error": True}


def _nested(value: dict[str, Any], *keys: str, default: Any = None) -> Any:
    current: Any = value
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


def _all_rubric_criteria(text: str) -> bool:
    return all(re.search(rf"\|\s*{re.escape(name)}\s*\|", text, re.IGNORECASE) for name in RUBRIC_CRITERIA)


def _score(text: str, structured: dict[str, Any]) -> float | None:
    value = _nested(structured, "rubric", "average")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    matches = list(SCORE_PATTERN.finditer(text))
    return float(matches[-1].group("score")) if matches else None


def _status_projection_state(status_text: str, chapter: dict[str, Any]) -> str | None:
    chapter_id = re.escape(str(chapter["id"]))
    number = int(chapter["number"])
    generated = re.compile(
        rf"^\|\s*{number:02d}\s*\|\s*{chapter_id}\s*\|.*?\|\s*({'|'.join(map(re.escape, LIFECYCLE_STATES))})\s*\|",
        re.MULTILINE,
    )
    match = generated.search(status_text)
    if match:
        return match.group(1)
    legacy = re.compile(
        rf"^\|\s*{number:02d}\s+—.*?\|\s*({'|'.join(map(re.escape, LIFECYCLE_STATES))})\s*\|",
        re.MULTILINE,
    )
    match = legacy.search(status_text)
    return match.group(1) if match else None


def inspect_chapter(root: Path, chapter: dict[str, Any], status_text: str, book_text: str) -> ChapterEvidence:
    evidence = ChapterEvidence(
        chapter=chapter,
        chapter_path=root / chapter["expected_chapter_path"],
        review_path=root / chapter["expected_review_path"],
    )
    evidence.chapter_exists = evidence.chapter_path.is_file()
    evidence.review_exists = evidence.review_path.is_file()
    evidence.chapter_text = _read(evidence.chapter_path)
    evidence.review_text = _read(evidence.review_path)
    evidence.chapter_status = _status(evidence.chapter_text)
    evidence.review_status = _status(evidence.review_text)
    evidence.structured = _structured_evidence(evidence.review_text)

    required_plan_headings = (
        "## Chapter Purpose",
        "## Learning Objectives",
        "## Primary Mental Model",
        "## Explicit Scope Boundaries",
        "## Proposed Chapter Structure",
    )
    evidence.architecture_plan = (
        _nested(evidence.structured, "architecture", "plan") == "complete"
        or all(heading in evidence.review_text for heading in required_plan_headings)
    )
    evidence.architecture_evaluated = (
        _nested(evidence.structured, "architecture", "evaluation") == "complete"
        or (
            "## Quality-Rubric Evaluation of the Plan" in evidence.review_text
            and "Architecture readiness:" in evidence.review_text
        )
    )

    required_draft_headings = (
        "## Learning Objectives",
        "## Exercises",
        "## Mastery Checklist",
        "## Further Study",
    )
    evidence.draft_complete = (
        _nested(evidence.structured, "draft", "status") == "complete"
        or (
            evidence.chapter_exists
            and len(evidence.chapter_text) >= 2000
            and all(heading in evidence.chapter_text for heading in required_draft_headings)
        )
    )

    reviews = _nested(evidence.structured, "reviews", default={})
    structured_reviews_complete = isinstance(reviews, dict) and all(
        _nested(reviews, name, "status") == "complete" for name in REVIEWER_NAMES
    )
    legacy_review_complete = (
        "## Independent Review — Drafted Chapter" in evidence.review_text
        and _all_rubric_criteria(evidence.review_text)
    )
    evidence.internal_review_complete = structured_reviews_complete or legacy_review_complete
    evidence.unresolved_blocking = int(_nested(evidence.structured, "revision", "unresolved_blocking", default=0) or 0)
    evidence.unresolved_major = int(_nested(evidence.structured, "revision", "unresolved_major", default=0) or 0)
    explicit_revision = evidence.review_status == "Revision Required" or bool(
        re.search(r"\*\*Final status:\*\*\s*`?Revision Required`?", evidence.review_text)
    )
    later_approval = "### Final approval status" in evidence.review_text and "**Final status:** `Approved`" in evidence.review_text
    evidence.revision_required = (
        evidence.unresolved_blocking > 0
        or evidence.unresolved_major > 0
        or (explicit_revision and not later_approval)
    )
    evidence.review_score = _score(evidence.review_text, evidence.structured)

    structured_candidate = (
        _nested(evidence.structured, "validation", "status") == "passed"
        and _nested(evidence.structured, "rubric", "status") == "complete"
        and _nested(evidence.structured, "candidate_summary", "status") == "complete"
        and evidence.review_score is not None
        and evidence.review_score >= 4.0
        and float(_nested(evidence.structured, "rubric", "minimum", default=0)) >= 3.0
        and evidence.unresolved_blocking == 0
        and evidence.unresolved_major == 0
    )
    legacy_candidate = (
        "## Focused Revision and Approval Review" in evidence.review_text
        and "### Focused verification" in evidence.review_text
        and "### Final quality-rubric scores" in evidence.review_text
        and evidence.review_score is not None
        and evidence.review_score >= 4.0
        and "no unresolved material accuracy concern" in evidence.review_text.lower()
    )
    evidence.candidate_package = structured_candidate or legacy_candidate

    human_approval = _nested(evidence.structured, "human_approval", default={})
    structured_human_approval = (
        isinstance(human_approval, dict)
        and human_approval.get("decision") == "approved"
        and human_approval.get("actor") == "human"
        and bool(human_approval.get("date"))
    )
    gate = chapter.get("human_gate", {})
    legacy_consensus = (
        gate.get("status") == "satisfied"
        and gate.get("evidence_kind") == "legacy_status_consensus"
        and evidence.chapter_status == "Approved"
        and evidence.review_status == "Approved"
        and _status_projection_state(status_text, chapter) == "Approved"
        and legacy_candidate
    )
    evidence.human_approval = structured_human_approval or legacy_consensus

    begin_marker = f"<!-- BEGIN CHAPTER: {chapter['id']} -->"
    end_marker = f"<!-- END CHAPTER: {chapter['id']} -->"
    evidence.integrated = (
        begin_marker in book_text
        and end_marker in book_text
        and evidence.chapter_text.strip() in book_text
    )

    if evidence.integrated and evidence.human_approval:
        evidence.justified_state = "Integrated"
    elif evidence.human_approval and evidence.candidate_package:
        evidence.justified_state = "Approved"
    elif evidence.candidate_package:
        evidence.justified_state = "Candidate for Human Approval"
    elif evidence.revision_required:
        evidence.justified_state = "Revision Required"
    elif evidence.internal_review_complete:
        evidence.justified_state = "Internal Review"
    elif evidence.chapter_exists:
        evidence.justified_state = "Drafting"
    elif evidence.architecture_plan and evidence.architecture_evaluated:
        evidence.justified_state = "Architecture Ready"
    else:
        evidence.justified_state = "Planned"
    return evidence


def discover_state(root: Path = ROOT, manifest: dict[str, Any] | None = None) -> tuple[list[ChapterEvidence], list[Issue]]:
    manifest = manifest or load_manifest(root)
    status_text = _read(root / STATUS_PATH)
    book_text = _read(root / BOOK_PATH)
    evidence = [inspect_chapter(root, chapter, status_text, book_text) for chapter in manifest.get("chapters", [])]
    issues = validate_repository(root, manifest, evidence, status_text, book_text)
    return evidence, issues


def _issue(issues: list[Issue], code: str, message: str, repairable: bool = False) -> None:
    issues.append(Issue(code, message, repairable))


def validate_manifest(manifest: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    if manifest.get("schema_version") != "1.0.0":
        _issue(issues, "manifest.schema_version", "schema_version must be exactly '1.0.0'")
    book = manifest.get("book")
    if not isinstance(book, dict):
        _issue(issues, "manifest.book", "book must be an object")
    else:
        for field_name in ("id", "title", "version", "status", "last_meaningful_update", "current_focus"):
            if field_name not in book:
                _issue(issues, "manifest.book_field", f"book is missing {field_name!r}")
    chapters = manifest.get("chapters")
    if not isinstance(chapters, list) or not chapters:
        _issue(issues, "manifest.chapters", "chapters must be a non-empty array")
        return issues

    required = (
        "id",
        "number",
        "title",
        "part",
        "recommended_writing_priority",
        "dependencies",
        "current_lifecycle_state",
        "expected_chapter_path",
        "expected_review_path",
        "review_score",
        "last_meaningful_update",
        "human_gate",
        "editorial_priority",
        "lifecycle_history",
    )
    ids: dict[str, int] = {}
    numbers: dict[int, str] = {}
    priorities: dict[int, str] = {}
    for index, chapter in enumerate(chapters):
        if not isinstance(chapter, dict):
            _issue(issues, "manifest.chapter_type", f"chapters[{index}] must be an object")
            continue
        for field_name in required:
            if field_name not in chapter:
                _issue(issues, "manifest.chapter_field", f"chapters[{index}] is missing {field_name!r}")
        chapter_id = chapter.get("id")
        number = chapter.get("number")
        priority = chapter.get("recommended_writing_priority")
        if not isinstance(chapter_id, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", chapter_id):
            _issue(issues, "manifest.chapter_id", f"chapters[{index}].id must be stable kebab-case")
        elif chapter_id in ids:
            _issue(issues, "manifest.duplicate_id", f"duplicate chapter id {chapter_id!r}")
        else:
            ids[chapter_id] = index
        if not isinstance(number, int) or isinstance(number, bool) or not 1 <= number <= 99:
            _issue(issues, "manifest.chapter_number", f"{chapter_id!r} has invalid chapter number {number!r}")
        elif number in numbers:
            _issue(issues, "manifest.duplicate_number", f"duplicate chapter number {number:02d}: {numbers[number]!r} and {chapter_id!r}")
        else:
            numbers[number] = str(chapter_id)
        if not isinstance(priority, int) or isinstance(priority, bool) or priority < 1:
            _issue(issues, "manifest.writing_priority", f"{chapter_id!r} has invalid recommended writing priority")
        elif priority in priorities:
            _issue(issues, "manifest.duplicate_priority", f"duplicate recommended writing priority {priority}: {priorities[priority]!r} and {chapter_id!r}")
        else:
            priorities[priority] = str(chapter_id)
        if chapter.get("current_lifecycle_state") not in LIFECYCLE_STATES:
            _issue(issues, "manifest.lifecycle_state", f"{chapter_id!r} has an unknown lifecycle state")
        for key in ("dependencies", "advisory_dependencies"):
            value = chapter.get(key, [])
            if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
                _issue(issues, "manifest.dependencies", f"{chapter_id!r}.{key} must be an array of chapter IDs")
        gate = chapter.get("human_gate")
        if not isinstance(gate, dict) or gate.get("status") not in {"not_required", "pending", "satisfied", "changes_requested"}:
            _issue(issues, "manifest.human_gate", f"{chapter_id!r} has an invalid human_gate")
        history = chapter.get("lifecycle_history")
        if not isinstance(history, list) or not history:
            _issue(issues, "manifest.lifecycle_history", f"{chapter_id!r} must have lifecycle_history")

    all_ids = set(ids)
    graph: dict[str, list[str]] = {}
    for chapter in chapters:
        if not isinstance(chapter, dict) or not isinstance(chapter.get("id"), str):
            continue
        chapter_id = chapter["id"]
        dependencies = list(chapter.get("dependencies", [])) + list(chapter.get("advisory_dependencies", []))
        graph[chapter_id] = dependencies
        for dependency in dependencies:
            if dependency not in all_ids:
                _issue(issues, "manifest.unknown_dependency", f"{chapter_id!r} depends on unknown chapter {dependency!r}")
            if dependency == chapter_id:
                _issue(issues, "manifest.self_dependency", f"{chapter_id!r} depends on itself")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(chapter_id: str, path: list[str]) -> None:
        if chapter_id in visiting:
            start = path.index(chapter_id)
            _issue(issues, "manifest.dependency_cycle", "dependency cycle: " + " -> ".join(path[start:] + [chapter_id]))
            return
        if chapter_id in visited:
            return
        visiting.add(chapter_id)
        for dependency in graph.get(chapter_id, []):
            if dependency in graph:
                visit(dependency, path + [chapter_id])
        visiting.remove(chapter_id)
        visited.add(chapter_id)

    for chapter_id in graph:
        visit(chapter_id, [])
    return issues


def _validate_history(chapter: dict[str, Any], issues: list[Issue]) -> None:
    history = chapter.get("lifecycle_history", [])
    if not isinstance(history, list) or not history:
        return
    states: list[str] = []
    for index, item in enumerate(history):
        if not isinstance(item, dict):
            _issue(issues, "history.entry", f"{chapter['id']} lifecycle_history[{index}] must be an object")
            continue
        state = item.get("state")
        if state not in LIFECYCLE_STATES:
            _issue(issues, "history.state", f"{chapter['id']} lifecycle_history[{index}] has unknown state {state!r}")
            continue
        states.append(state)
        if item.get("actor") not in {"human", "workflow", "migration"}:
            _issue(issues, "history.actor", f"{chapter['id']} lifecycle_history[{index}] has invalid actor")
        if index and history[index - 1].get("state") == "Candidate for Human Approval" and state == "Approved" and item.get("actor") != "human":
            _issue(issues, "history.automated_approval", f"{chapter['id']} Candidate → Approved transition must have actor 'human'")
        if index and history[index - 1].get("state") in {"Approved", "Integrated"} and state == "Revision Required" and item.get("actor") != "human":
            _issue(issues, "history.approved_invalidation", f"{chapter['id']} invalidating approved work requires actor 'human'")
    for before, after in zip(states, states[1:]):
        if after not in LEGAL_TRANSITIONS[before]:
            _issue(issues, "history.illegal_transition", f"{chapter['id']} has illegal lifecycle transition {before!r} → {after!r}")
    if states and states[-1] != chapter.get("current_lifecycle_state"):
        _issue(issues, "history.current_mismatch", f"{chapter['id']} lifecycle_history ends at {states[-1]!r}, not recorded state {chapter.get('current_lifecycle_state')!r}", True)


def _headings(text: str) -> list[tuple[int, int, str]]:
    result: list[tuple[int, int, str]] = []
    in_fence = False
    in_comment = False
    for line_number, line in enumerate(text.splitlines(), 1):
        if in_comment:
            if "-->" in line:
                in_comment = False
            continue
        if "<!--" in line:
            if "-->" not in line.split("<!--", 1)[1]:
                in_comment = True
            line = line.split("<!--", 1)[0]
            if not line:
                continue
        if line.startswith("```") or line.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = re.match(r"^(#{1,6})\s+(.+)$", line)
        if match:
            result.append((line_number, len(match.group(1)), match.group(2)))
    return result


def _validate_markdown(path: Path, text: str, issues: list[Issue], check_placeholders: bool) -> None:
    headings = _headings(text)
    if not headings or headings[0][1] != 1:
        _issue(issues, "markdown.h1", f"{path}: first heading must be H1")
    if sum(1 for _, level, _ in headings if level == 1) != 1:
        _issue(issues, "markdown.h1_count", f"{path}: expected exactly one H1")
    previous = 0
    for line_number, level, _ in headings:
        if previous and level > previous + 1:
            _issue(issues, "markdown.heading_skip", f"{path}:{line_number}: heading skips from H{previous} to H{level}")
        previous = level
    if text.count("```") % 2:
        _issue(issues, "markdown.fence", f"{path}: unbalanced triple-backtick fence")
    if check_placeholders:
        for pattern in PLACEHOLDER_PATTERNS:
            match = pattern.search(text)
            if match:
                line = text.count("\n", 0, match.start()) + 1
                _issue(issues, "markdown.placeholder", f"{path}:{line}: unresolved placeholder {match.group(0)!r}")


def _validate_links(root: Path, paths: Iterable[Path], issues: list[Issue]) -> None:
    for path in paths:
        text = re.sub(r"<!--.*?-->", "", _read(path), flags=re.DOTALL)
        for match in URL_PATTERN.finditer(text):
            raw_target = match.group("target").strip().split()[0].strip("<>")
            parsed = urlsplit(raw_target)
            if parsed.scheme in {"http", "https", "mailto"} or raw_target.startswith("#"):
                continue
            target = unquote(parsed.path)
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                _issue(issues, "links.outside_root", f"{path}: link escapes repository: {raw_target}")
                continue
            if not resolved.exists():
                _issue(issues, "links.missing", f"{path}: missing link target {raw_target!r}")


def _validate_glossary(root: Path, issues: list[Issue]) -> None:
    path = root / "glossary.md"
    text = _read(path)
    terms = [title.strip() for _, level, title in _headings(text) if level == 2]
    if terms != sorted(terms, key=str.casefold):
        _issue(issues, "glossary.order", "glossary H2 terms must be alphabetical")
    duplicates = {term for term in terms if terms.count(term) > 1}
    for term in sorted(duplicates):
        _issue(issues, "glossary.duplicate", f"duplicate glossary term {term!r}")


def _validate_references(root: Path, evidence: list[ChapterEvidence], issues: list[Issue]) -> None:
    references_text = _read(root / "references.md")
    reference_urls = set(EXTERNAL_URL.findall(references_text))
    for item in evidence:
        if not item.chapter_exists:
            continue
        for url in set(EXTERNAL_URL.findall(item.chapter_text)):
            if url not in reference_urls:
                _issue(issues, "references.missing", f"{item.chapter_path}: cited URL is absent from references.md: {url}")


def _validate_codex_configuration(root: Path, issues: list[Issue]) -> None:
    config_path = root / ".codex/config.toml"
    try:
        config = tomllib.loads(config_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, tomllib.TOMLDecodeError, OSError, UnicodeError) as error:
        _issue(issues, "codex.config", f"cannot parse {config_path}: {error}")
        return
    agents_config = config.get("agents", {})
    if agents_config.get("max_threads") != 6:
        _issue(issues, "codex.max_threads", ".codex/config.toml must set agents.max_threads = 6")
    if agents_config.get("max_depth") != 1:
        _issue(issues, "codex.max_depth", ".codex/config.toml must set agents.max_depth = 1 to disable recursive delegation")

    expected_agents = set(REVIEWER_NAMES)
    for name in sorted(expected_agents):
        path = root / f".codex/agents/{name}.toml"
        try:
            value = tomllib.loads(path.read_text(encoding="utf-8"))
        except (FileNotFoundError, tomllib.TOMLDecodeError, OSError, UnicodeError) as error:
            _issue(issues, "codex.reviewer", f"cannot parse reviewer {path}: {error}")
            continue
        for required in ("name", "description", "developer_instructions"):
            if not isinstance(value.get(required), str) or not value[required].strip():
                _issue(issues, "codex.reviewer_field", f"{path}: missing non-empty {required}")
        if value.get("name") != name:
            _issue(issues, "codex.reviewer_name", f"{path}: name must be {name!r}")
        if value.get("sandbox_mode") != "read-only":
            _issue(issues, "codex.reviewer_sandbox", f"{path}: sandbox_mode must be 'read-only'")

    skill_path = root / ".agents/skills/ebook/SKILL.md"
    skill_text = _read(skill_path)
    frontmatter = re.match(r"^---\n(?P<body>.*?)\n---\n", skill_text, re.DOTALL)
    if not frontmatter:
        _issue(issues, "skill.frontmatter", f"{skill_path}: missing YAML frontmatter")
    else:
        body = frontmatter.group("body")
        if not re.search(r"^name:\s*ebook\s*$", body, re.MULTILINE):
            _issue(issues, "skill.name", f"{skill_path}: frontmatter name must be ebook")
        if not re.search(r"^description:\s*\S.+$", body, re.MULTILINE):
            _issue(issues, "skill.description", f"{skill_path}: frontmatter requires a description")


def render_status(manifest: dict[str, Any]) -> str:
    book = manifest["book"]
    lines = [
        "<!-- GENERATED STATUS VIEW: run python scripts/sync_book_status.py; do not edit chapter rows directly. -->",
        "",
        "# Book Status",
        "",
        f"> **Book version:** {book['version']}",
        f"> **Overall status:** {book['status']}",
        f"> **Last meaningful update:** {book['last_meaningful_update']}",
        f"> **Current focus:** {book['current_focus']}",
        "",
        "The blueprint owns the intellectual architecture. `book-manifest.json` owns workflow state, dependencies, paths, priorities, and gates. This file is its generated human-readable projection; validate synchronization with `python scripts/validate_book.py`.",
        "",
        "| No. | Stable ID | Title | Part | Lifecycle state | Required dependencies | Writing priority | Editorial priority | Review score | Updated | Human gate |",
        "|---:|---|---|---|---|---|---:|---:|---:|---|---|",
    ]
    for chapter in sorted(manifest["chapters"], key=lambda item: item["number"]):
        dependencies = ", ".join(chapter["dependencies"]) or "—"
        editorial = chapter["editorial_priority"] if chapter["editorial_priority"] is not None else "—"
        score = f"{chapter['review_score']:.2f}/5" if chapter["review_score"] is not None else "—"
        updated = chapter["last_meaningful_update"] or "—"
        gate = chapter["human_gate"]["status"]
        lines.append(
            f"| {chapter['number']:02d} | {chapter['id']} | {chapter['title']} | {chapter['part']} | "
            f"{chapter['current_lifecycle_state']} | {dependencies} | {chapter['recommended_writing_priority']} | "
            f"{editorial} | {score} | {updated} | {gate} |"
        )
    lines.extend(
        [
            "",
            "## Synchronization responsibilities",
            "",
            "- `docs/BOOK_BLUEPRINT.md`: planned intellectual architecture and chapter intent.",
            "- `book-manifest.json`: canonical workflow/dependency state and artifact paths.",
            "- `docs/BOOK_STATUS.md`: generated human-readable projection of the manifest.",
            "- `chapters/`: manuscript content and chapter-level metadata.",
            "- `reviews/`: architecture, review, revision, validation, rubric, candidate, and human-decision evidence.",
            "- `book.md`: generated output containing only manifest chapters in `Integrated` state.",
            "",
            "## Cross-chapter review checkpoints",
            "",
            "After each group of three to five integrated chapters, run the terminology, duplication, prerequisite, example-consistency, and cross-link review described in the editorial workflow.",
            "",
        ]
    )
    return "\n".join(lines)


def validate_repository(
    root: Path,
    manifest: dict[str, Any],
    evidence: list[ChapterEvidence],
    status_text: str,
    book_text: str,
) -> list[Issue]:
    issues = validate_manifest(manifest)
    chapters = manifest.get("chapters", []) if isinstance(manifest.get("chapters"), list) else []
    for chapter in chapters:
        if isinstance(chapter, dict) and "id" in chapter:
            _validate_history(chapter, issues)

    expected_status = render_status(manifest) if chapters else ""
    if status_text != expected_status:
        _issue(issues, "status.out_of_sync", "docs/BOOK_STATUS.md is not the exact projection of book-manifest.json; run python scripts/sync_book_status.py", True)

    expected_paths = {str(chapter.get("expected_chapter_path")) for chapter in chapters}
    expected_reviews = {str(chapter.get("expected_review_path")) for chapter in chapters}
    for path in sorted((root / "chapters").glob("*.md")):
        if not CHAPTER_FILE.fullmatch(path.name):
            _issue(issues, "filename.chapter", f"invalid chapter filename: {path.relative_to(root)}")
        if str(path.relative_to(root)) not in expected_paths:
            _issue(issues, "filename.unmanifested_chapter", f"chapter is absent from manifest: {path.relative_to(root)}")
    for path in sorted((root / "reviews").glob("*.md")):
        if not REVIEW_FILE.fullmatch(path.name):
            _issue(issues, "filename.review", f"invalid review filename: {path.relative_to(root)}")
        if str(path.relative_to(root)) not in expected_reviews:
            _issue(issues, "filename.unmanifested_review", f"review is absent from manifest: {path.relative_to(root)}")

    markdown_paths: list[Path] = [root / "glossary.md", root / "references.md"]
    for item in evidence:
        chapter = item.chapter
        recorded = chapter.get("current_lifecycle_state")
        if recorded != item.justified_state:
            _issue(
                issues,
                "state.evidence_mismatch",
                f"{chapter['id']}: manifest records {recorded!r}, but repository evidence justifies {item.justified_state!r}",
                STATE_RANK.get(item.justified_state, -1) < STATE_RANK.get(recorded, -1),
            )
        if item.structured.get("_parse_error"):
            _issue(issues, "evidence.invalid_json", f"{item.review_path}: invalid ebook-workflow-evidence JSON")
        if item.chapter_exists and not item.review_exists:
            _issue(issues, "artifacts.chapter_without_review", f"{chapter['id']}: chapter exists without its review file")
        if recorded in {"Candidate for Human Approval", "Approved", "Integrated"} and not item.candidate_package:
            _issue(issues, "evidence.candidate", f"{chapter['id']}: {recorded} requires a complete candidate package")
        if recorded in {"Approved", "Integrated"} and not item.human_approval:
            _issue(issues, "evidence.approval", f"{chapter['id']}: {recorded} requires explicit human approval evidence")
        if recorded == "Candidate for Human Approval" and chapter.get("human_gate", {}).get("status") != "pending":
            _issue(issues, "gate.pending", f"{chapter['id']}: candidate state requires human_gate.status 'pending'", True)
        if recorded in {"Approved", "Integrated"} and chapter.get("human_gate", {}).get("status") != "satisfied":
            _issue(issues, "gate.satisfied", f"{chapter['id']}: {recorded} requires human_gate.status 'satisfied'", True)
        expected_metadata = "Approved" if recorded == "Integrated" else recorded
        if item.chapter_exists and recorded not in {"Planned", "Architecture Ready"} and item.chapter_status != expected_metadata:
            _issue(issues, "metadata.chapter_status", f"{chapter['id']}: chapter metadata is {item.chapter_status!r}, expected {expected_metadata!r}", True)
        if item.review_exists and item.review_status != expected_metadata:
            _issue(issues, "metadata.review_status", f"{chapter['id']}: review metadata is {item.review_status!r}, expected {expected_metadata!r}", True)
        if chapter.get("review_score") is not None and item.review_score is not None and abs(float(chapter["review_score"]) - item.review_score) > 0.005:
            _issue(issues, "metadata.review_score", f"{chapter['id']}: manifest score {chapter['review_score']} does not match review evidence {item.review_score}", True)
        if item.chapter_exists:
            markdown_paths.append(item.chapter_path)
            _validate_markdown(item.chapter_path, item.chapter_text, issues, True)
            expected_h1 = f"Chapter {chapter['number']:02d} — {chapter['title']}"
            headings = _headings(item.chapter_text)
            if not headings or headings[0][2] != expected_h1:
                _issue(issues, "metadata.chapter_title", f"{chapter['id']}: chapter H1 must be '# {expected_h1}'")
        if item.review_exists:
            markdown_paths.append(item.review_path)
            _validate_markdown(item.review_path, item.review_text, issues, recorded in {"Candidate for Human Approval", "Approved", "Integrated"})

    _validate_links(root, markdown_paths + [root / "README.md", root / "docs/EDITORIAL_WORKFLOW.md", root / "docs/CHAPTER_LIFECYCLE.md"], issues)
    _validate_glossary(root, issues)
    _validate_references(root, evidence, issues)

    integrated = [item for item in evidence if item.chapter.get("current_lifecycle_state") == "Integrated"]
    marker_ids = re.findall(r"<!-- BEGIN CHAPTER: ([a-z0-9-]+) -->", book_text)
    expected_marker_ids = [item.chapter["id"] for item in sorted(integrated, key=lambda item: item.chapter["number"])]
    if marker_ids != expected_marker_ids:
        _issue(issues, "build.order", f"book.md integrated order {marker_ids!r} does not match manifest order {expected_marker_ids!r}")
    for item in evidence:
        if item.chapter.get("current_lifecycle_state") != "Integrated" and f"<!-- BEGIN CHAPTER: {item.chapter['id']} -->" in book_text:
            _issue(issues, "build.unintegrated", f"book.md contains non-integrated chapter {item.chapter['id']}")

    for path in sorted((root / ".codex").glob("**/*.toml")):
        try:
            tomllib.loads(path.read_text(encoding="utf-8"))
        except (tomllib.TOMLDecodeError, OSError, UnicodeError) as error:
            _issue(issues, "toml.invalid", f"{path}: {error}")
    _validate_codex_configuration(root, issues)
    return issues


def _sort_key(item: ChapterEvidence) -> tuple[int, int, int, int]:
    editorial = item.chapter.get("editorial_priority")
    return (
        -STATE_RANK[item.justified_state],
        editorial if isinstance(editorial, int) else 1_000_000,
        int(item.chapter["recommended_writing_priority"]),
        int(item.chapter["number"]),
    )


def recommend_next_action(
    manifest: dict[str, Any], evidence: list[ChapterEvidence], issues: list[Issue]
) -> Recommendation:
    if issues:
        first = issues[0]
        repairable = all(issue.repairable for issue in issues)
        action = "repair_metadata" if repairable else "resolve_inconsistency"
        return Recommendation(action, None, None, first.message, ("Clean validation report",))

    candidates = [item for item in evidence if item.justified_state == "Candidate for Human Approval"]
    if candidates:
        item = sorted(candidates, key=_sort_key)[0]
        return Recommendation(
            "human_approval_required",
            item.chapter["id"],
            item.justified_state,
            "A complete candidate package is waiting at the mandatory human gate; unrelated work is blocked.",
            ("Human decision: approve or request revision", "Decision recorded in review evidence and manifest history"),
        )

    active = [
        item
        for item in evidence
        if item.justified_state in {"Architecture Ready", "Drafting", "Internal Review", "Revision Required"}
        or (item.justified_state == "Planned" and (item.architecture_plan or item.review_exists))
    ]
    if active:
        item = sorted(active, key=_sort_key)[0]
        if item.justified_state == "Revision Required":
            action = "resume_revision"
            reason = f"{item.unresolved_blocking} blocking and {item.unresolved_major} major findings remain, or the review explicitly requires revision."
            artifacts = ("Revised chapter", "Affected reviewer re-checks", "Updated rubric and workflow evidence")
        elif item.justified_state == "Internal Review":
            action = "complete_internal_review"
            reason = "Independent review evidence exists, but revision resolution and candidate evidence are incomplete."
            artifacts = ("Aggregated findings", "Revision decision", "Updated reviewer evidence")
        elif item.justified_state == "Drafting":
            action = "resume_drafting"
            reason = "A chapter artifact exists, but complete draft and review evidence do not."
            artifacts = ("Complete draft", "Draft-complete evidence")
        elif item.justified_state == "Architecture Ready":
            action = "begin_drafting"
            reason = "The chapter architecture is planned and evaluated; drafting is the first incomplete phase."
            artifacts = ("Chapter draft", "Draft-complete evidence")
        elif item.architecture_plan:
            action = "evaluate_architecture"
            reason = "An architecture plan exists but has not been evaluated against scope, dependencies, and the quality rubric."
            artifacts = ("Architecture evaluation", "Architecture-ready evidence")
        else:
            action = "resume_architecture"
            reason = "A review artifact exists but does not contain sufficient architecture evidence."
            artifacts = ("Complete architecture plan", "Selection reasoning")
        return Recommendation(action, item.chapter["id"], item.justified_state, reason, artifacts)

    approved = [item for item in evidence if item.justified_state == "Approved"]
    if approved:
        item = sorted(approved, key=_sort_key)[0]
        return Recommendation(
            "integrate_approved",
            item.chapter["id"],
            item.justified_state,
            "Human approval evidence is valid, but the chapter is absent from the generated integrated book.",
            ("Pre-integration validation", "Integrated lifecycle transition", "Rebuilt book.md", "Full validation"),
        )

    by_id = {item.chapter["id"]: item for item in evidence}
    eligible = [
        item
        for item in evidence
        if item.justified_state == "Planned"
        and not item.review_exists
        and all(by_id[dependency].justified_state == "Integrated" for dependency in item.chapter.get("dependencies", []))
    ]
    if eligible:
        item = sorted(
            eligible,
            key=lambda candidate: (
                candidate.chapter.get("editorial_priority") if isinstance(candidate.chapter.get("editorial_priority"), int) else 1_000_000,
                candidate.chapter["recommended_writing_priority"],
                candidate.chapter["number"],
            ),
        )[0]
        dependencies = item.chapter.get("dependencies", [])
        reason = (
            "No inconsistency, human gate, active work, or approved-unintegrated chapter exists; "
            f"required dependencies are satisfied and this chapter ranks highest by editorial then writing priority."
        )
        if dependencies:
            reason += " Satisfied dependencies: " + ", ".join(dependencies) + "."
        return Recommendation(
            "begin_architecture",
            item.chapter["id"],
            item.justified_state,
            reason,
            ("Review file with selection reasoning", "Architecture plan", "Architecture evaluation"),
        )

    if all(item.justified_state == "Integrated" for item in evidence):
        return Recommendation("book_complete", None, None, "Every planned chapter is integrated.")
    return Recommendation(
        "human_editorial_decision_required",
        None,
        None,
        "No chapter is eligible: remaining planned work has unsatisfied dependencies that cannot be resolved by current repository state.",
        ("Human dependency or architecture decision",),
    )


def recommendation_text(recommendation: Recommendation, manifest: dict[str, Any]) -> str:
    chapter = None
    if recommendation.chapter_id:
        chapter = next(item for item in manifest["chapters"] if item["id"] == recommendation.chapter_id)
    lines = ["NEXT ACTION", f"Type: {recommendation.action_type}"]
    if chapter:
        lines.append(f"Chapter: {chapter['id']}")
        lines.append(f"Title: {chapter['title']}")
    if recommendation.justified_state:
        lines.append(f"Current justified state: {recommendation.justified_state}")
    lines.append(f"Reason: {recommendation.reason}")
    if recommendation.required_artifacts:
        lines.append("Required artifacts:")
        lines.extend(f"- {artifact}" for artifact in recommendation.required_artifacts)
    return "\n".join(lines)
