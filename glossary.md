# Glossary

This file records canonical definitions for terms used across multiple chapters. Add an entry only when a term is introduced or a shared definition prevents ambiguity.

Keep entries alphabetical. Prefer a concise definition followed by links to the chapters that provide the full explanation.

<!-- Example format:
## Term

Definition. See [Chapter NN](chapters/NN-chapter-slug.md).
-->

## Accepted state

The result to which an accountable boundary has committed after evaluating a proposal under its declared rules and guarantees. It is eligible to serve as authoritative state for the facts that boundary owns; downstream copies may still be stale or incomplete. See [Chapter 02](chapters/02-state-invariants-and-change.md).

## Aliasing

The condition in which multiple access paths reach the same mutable runtime object or shared underlying data, so a change through one path may be observed through another. See [Chapter 02](chapters/02-state-invariants-and-change.md).

## Authoritative source

The representation allowed to resolve disagreement about a named fact. Multiple non-authoritative copies may legitimately exist. “Single source of truth” is common shorthand but can misleadingly suggest one physical store for all facts. See [Chapter 02](chapters/02-state-invariants-and-change.md).

## Derived state

A representation whose value can be obtained from other facts by a declared rule. A stored derivation requires explicit synchronization, acceptable-staleness, detection, and recovery expectations. See [Chapter 02](chapters/02-state-invariants-and-change.md).

## Domain identity

The continuity by which a domain concept is treated as the same entity across changes to its current values. It is distinct from runtime object identity and value equality. See [Chapter 02](chapters/02-state-invariants-and-change.md).

## Invariant

A predicate that must be true for every accepted state within an explicitly declared scope. See [Chapter 02](chapters/02-state-invariants-and-change.md).

## State

The information needed, for a chosen purpose and boundary, to distinguish relevant situations at a point in time. See [Chapter 02](chapters/02-state-invariants-and-change.md).

## State transition

A domain-level movement from one state to another, described by its preconditions, effects, and postconditions. It is distinct from an implementation-level mutation. See [Chapter 02](chapters/02-state-invariants-and-change.md).
