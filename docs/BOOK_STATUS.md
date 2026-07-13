# Book Status

> **Book version:** 0.1 — architecture
> **Last meaningful update:** 2026-07-13
> **Current focus:** Chapter 02 architecture is ready for human review; drafting has not begun.

Scores remain `—` until a complete, evidence-backed rubric review exists. Dependencies are editorial guidance inferred from the blueprint; they identify the most important conceptual inputs, not an exhaustive reading order.

| Chapter | Status | Dependency notes | Review score | Last meaningful update | Next recommended action |
|---|---|---|---:|---|---|
| **Part I — Thinking Like a Software Engineer** |  |  |  |  |  |
| 01 — What Software Engineering Actually Is | Planned | None; establishes vocabulary used throughout | — | — | Plan after the central technical voice is established, per the suggested writing order |
| 02 — State, Invariants, and Change | Planning | Chapter 01 helpful but not required; plan defines prerequisites and later-chapter boundaries | 4.25/5 (plan) | 2026-07-13 | Human-review the architecture and resolve its central terminology questions before drafting |
| 03 — Abstraction, Modularity, and Boundaries | Planned | Chapters 01–02 | — | — | Plan after Chapter 02 |
| 04 — Complexity and Engineering Trade-offs | Planned | Chapters 01–03 | — | — | Plan after the rest of Part I |
| **Part II — How Computers Execute Software** |  |  |  |  |  |
| 05 — Runtime Fundamentals | Planned | Chapters 02 and 04 | — | — | Plan after core Part I concepts |
| 06 — Processes, Threads, and the Operating System | Planned | Chapter 05 | — | — | Plan after Chapter 05 |
| 07 — Concurrency, Parallelism, and Coordination | Planned | Chapters 02, 05, and 06 | — | — | Plan after runtime and OS foundations |
| 08 — Networking and Distributed Communication | Planned | Chapters 05–07 | — | — | Plan after Chapter 07 |
| **Part III — Web, APIs, and Application Systems** |  |  |  |  |  |
| 09 — HTTP and the Web | Planned | Chapter 08 | — | — | Plan after networking fundamentals |
| 10 — API Design and Evolution | Planned | Chapters 03 and 09 | — | — | Plan in the blueprint's initial technical sequence after Chapter 16 |
| 11 — Authentication, Authorization, and Trust | Planned | Chapters 03, 08–10 | — | — | Plan after HTTP and API contracts |
| 12 — External Integrations and Unreliable Dependencies | Planned | Chapters 08–10 | — | — | Plan after Chapter 10 |
| **Part IV — Data, Persistence, and Correctness** |  |  |  |  |  |
| 13 — Data Modeling and Domain Modeling | Planned | Chapters 02–03 | — | — | Plan after Chapter 02 in the suggested writing sequence |
| 14 — Relational Databases and SQL | Planned | Chapters 02 and 13 | — | — | Plan after Chapter 13 |
| 15 — Indexes, Query Plans, and Database Performance | Planned | Chapters 04 and 14 | — | — | Plan after relational foundations |
| 16 — Transactions and Concurrency Control | Planned | Chapters 02, 07, and 14 | — | — | Plan after Chapters 14 and 07 concepts are available |
| 17 — Choosing Data Stores | Planned | Chapters 04, 13–16 | — | — | Plan after relational trade-offs are understood |
| **Part V — Reliability, Scale, and Operations** |  |  |  |  |  |
| 18 — Asynchronous Work, Queues, and Messaging | Planned | Chapters 07, 12, and 16 | — | — | Plan after integrations in the suggested writing sequence |
| 19 — Caching and Managing Staleness | Planned | Chapters 08, 14–17 | — | — | Plan after storage and consistency foundations |
| 20 — Distributed Systems Fundamentals | Planned | Chapters 07–08 and 16–19 | — | — | Plan after concurrency, networking, and persistence |
| 21 — Reliability and Designing for Failure | Planned | Chapters 12 and 18–20 | — | — | Plan after distributed-systems foundations |
| 22 — Observability and Systematic Debugging | Planned | Chapters 06, 12, 18, and 21 | — | — | Plan after reliability in the suggested writing sequence |
| 23 — Performance and Capacity | Planned | Chapters 04–08, 15, 19, and 22 | — | — | Plan after observability and performance mechanisms |
| **Part VI — Architecture, Delivery, and Engineering Judgment** |  |  |  |  |  |
| 24 — Testing and Verification | Planned | Chapters 02–04 and representative mechanism chapters | — | — | Plan once recurring examples and contracts are stable |
| 25 — Security as a System Property | Planned | Chapters 03, 08–12, 14, and 21 | — | — | Plan after trust boundaries and system mechanisms |
| 26 — Delivery, Deployment, and Safe Change | Planned | Chapters 06, 14, 21–25 | — | — | Plan after reliability, verification, and security |
| 27 — Architectural Styles and Their Trade-offs | Planned | Chapters 03–04, 12–13, 18, and 20–26 | — | — | Plan after the component trade-offs it synthesizes |
| 28 — System Design as Structured Reasoning | Planned | Chapters 02–27, especially 10, 13, 20–23, and 27 | — | — | Plan as the final chapter in the suggested initial sequence |
| 29 — Product, Economics, and Technical Decisions | Planned | Chapters 01, 04, 23, and 27–28 | — | — | Plan after system-design trade-offs |
| 30 — Communication, Leadership, and Engineering Influence | Planned | Chapters 01, 04, 28–29 | — | — | Plan after decision frameworks are established |
| **Part VII — Becoming an Expert** |  |  |  |  |  |
| 31 — Deliberate Practice and Building Mental Models | Planned | Chapters 01–30 as examples | — | — | Plan after the main technical arc exists |
| 32 — Working Effectively With AI | Planned | Chapters 01, 24, 28, 30–31 | — | — | Plan after verification and judgment chapters |
| 33 — Capstone: Designing and Operating a Complete System | Planned | Chapters 01–32, especially 10–28 | — | — | Plan after all required concepts are approved |

## Cross-chapter review checkpoints

Schedule a terminology, duplication, prerequisite, example-consistency, and cross-link review after each group of three to five approved chapters. Record the date and affected chapters here when the first checkpoint occurs.

## Immediate decision

The blueprint's suggested writing order starts with Chapter 02 rather than Chapter 01. Chapter 02 is now in `Planning`; its architecture review should be approved by a human before a separate drafting task begins.
