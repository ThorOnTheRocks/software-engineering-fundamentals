# Style Guide

This guide supplements [the book blueprint](BOOK_BLUEPRINT.md) and [chapter template](../templates/CHAPTER_TEMPLATE.md). It standardizes presentation without turning the book into a rigid formula.

## Voice and audience

Write for an experienced mid-level software engineer developing senior-level judgment. Use precise, accessible English and complete sentences. Explain mechanisms and consequences directly; avoid motivational filler, fake certainty, interview trivia, and slogans presented as reasoning.

Teach the mental model before naming tools. State important assumptions and distinguish durable principles from implementation-specific behavior. Connect local design choices to production, product, and business outcomes. Present recommendations as context-dependent trade-offs, not universal laws.

Use a small set of industry-neutral examples consistently: collaborative project management, reservations, orders and payments, developer platforms, and background processing.

## Terminology

Define jargon on first meaningful use, explain why the concept exists, demonstrate it, discuss its trade-offs, and connect it to related concepts. Use one term for one idea. Add terms reused across chapters to `glossary.md`; keep chapter-local definitions in the chapter.

Do not collapse distinct concepts for convenience. When industry usage is inconsistent, state the definition used by the book and acknowledge the relevant alternative.

## Headings

- Use one H1 for the chapter title: `# Chapter NN — Title`.
- Use H2 for major chapter sections and H3 for their subdivisions.
- Do not skip heading levels.
- Prefer descriptive headings that reveal the reasoning path.
- Adapt the chapter template when a clearer progression requires it, while preserving its teaching obligations.
- Avoid a new heading for a paragraph that belongs in the surrounding argument.

## Code blocks

Use code only when it clarifies a mechanism or decision. Keep examples focused and omit irrelevant setup. Every fenced block must use an appropriate language identifier such as `python`, `typescript`, `go`, `ruby`, `sql`, `json`, `text`, or `sh`.

Introduce the purpose and assumptions before the block, then explain the important consequence after it. Prefer correctness and readability over cleverness. Do not include secrets, unstable dependency versions, or output that has not been verified.

## Mermaid and text diagrams

Use a diagram only when relationships, flows, state transitions, boundaries, or failure paths are materially clearer visually. Use Mermaid for structured diagrams and fenced `text` blocks for compact representations that must remain portable.

Keep labels short, direction consistent, and diagrams understandable without color. Explain the conclusion the reader should draw. Store a diagram in `diagrams/` only when it is shared, generated externally, or impractical to maintain inline.

## Callouts

Use blockquotes sparingly for a durable mental model, a consequential warning, or an explicit assumption:

```markdown
> **Mental model:** Durable statement.

> **Warning:** Failure and consequence.

> **Assumption:** Context that bounds the claim.
```

Do not use callouts as decoration or as a substitute for integrating an idea into the explanation.

## Citations and references

Cite claims when evidence adds value, especially for specifications, evolving behavior, or original research. Prefer standards, RFCs, official documentation, original papers, and authoritative project documentation. Never invent a source, quotation, benchmark, or production result.

Use a descriptive inline Markdown link near the supported claim and add the full source under the chapter heading in `references.md`. Keep a consistent entry form: author or organization, linked title, publisher or standards body, and publication year or version when known. Qualify claims whose truth depends on implementation or workload.

## Internal links

Use relative Markdown links with descriptive labels, for example `[Chapter 2](../chapters/02-state-invariants-and-change.md)` from a document under `docs/`. Link to the canonical explanation instead of repeating it. Verify the destination exists before approval; clearly label forward references to chapters not yet drafted and add the link only when the target file exists.

When renaming or renumbering a chapter, update every affected link, review filename, status row, and reference entry in the same change.

## Language-translation sections

Include translations only when comparing TypeScript/Node.js, Python, Ruby/Rails, or Go makes the transferable concept more concrete. Keep each example brief, equivalent in intent, and free of framework setup. Explain semantic differences that affect the mental model; omit languages that add no insight.

These sections are translations, not tutorials or surveys. A concise prose comparison is often better than four near-identical code blocks.
