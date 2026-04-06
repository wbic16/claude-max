# 6D UML Specification v0.1

## Overview

6D UML is a living software engineering framework built on phext. It encodes the entire
lifecycle of a software system — from requirements through training — in a single phext
document. Artifacts are addressed in 5D (volume/book/chapter/section/scroll), and the
6th dimension (collection) selects the SDLC phase.

Walking from one collection to the next at the same 5D address traces an artifact from
its requirement through design, implementation, testing, and documentation. Traceability
is structural, not annotated.

## Coordinate Map

| Dimension  | Phext Dim | Role           | Delimiter | Hex  |
|------------|-----------|----------------|-----------|------|
| Collection | 8D        | SDLC Phase     | GS        | 0x1D |
| Volume     | 7D        | Sprint/Release | FS        | 0x1C |
| Book       | 6D        | Module         | SUB       | 0x1A |
| Chapter    | 5D        | Component      | EM        | 0x19 |
| Section    | 4D        | File           | CAN       | 0x18 |
| Scroll     | 3D        | Unit           | ETB       | 0x17 |

Series (0x1E), Shelf (0x1F), and Library (0x01) are user-managed outer dimensions.

## Collection Assignments

| Collection | Phase        | Description                              |
|------------|--------------|------------------------------------------|
| 1          | Meta         | System settings, coordinate maps, config |
| 2          | Requirements | User requirements and use cases          |
| 3          | Design       | Architecture, UML diagrams               |
| 4          | Source       | Implementation code                      |
| 5          | Tests        | Unit tests, integration tests            |
| 6          | Regressions  | Regression test suites                   |
| 7          | Docs         | Developer and user documentation         |
| 8          | Whitepapers  | Technical papers and research            |
| 9          | Training     | Onboarding and training materials        |

Collection assignments are configurable at runtime via Collection 1 (Meta).

## 5D Artifact Address

An artifact's identity is its 5D address: `volume.book.chapter/section.scroll`

| Component | Dimension | Meaning        | Example            |
|-----------|-----------|----------------|--------------------|
| Volume    | 7D        | Sprint/Release | 1 = Sprint 1       |
| Book      | 6D        | Module         | 1 = Auth            |
| Chapter   | 5D        | Component      | 1 = LoginForm       |
| Section   | 4D        | File           | 1 = login.rs        |
| Scroll    | 3D        | Unit           | 1 = validate()      |

## Full 6D Address Format

```
collection/volume.book.chapter/section.scroll
```

Example: `4/2.3.1/1.2` = Source code / Sprint 2, Module 3, Component 1 / File 1, Unit 2

The same artifact at `2/2.3.1/1.2` is its requirement. At `5/2.3.1/1.2`, its test.

## Phext Encoding

A 6D UML document is a valid phext file. The outer dimensions (series/shelf/library)
default to 1.1.1 unless the user structures them otherwise. Content is organized as:

```
1.1.1/[collection].[volume].[book]/[chapter].[section].[scroll]
```

The full 9D phext coordinate maps to 6D UML as:

```
series.shelf.library / collection.volume.book / chapter.section.scroll
       (user)              (SDLC + time)          (artifact structure)
```

## Stack Model

At each point in the 6D space, the system maintains a stack of assets. The stack
represents the vertical trace through collections at a fixed 5D address:

```
[Training  ] <- collection 9
[Whitepapers] <- collection 8
[Docs      ] <- collection 7
[Regressions] <- collection 6
[Tests     ] <- collection 5
[Source    ] <- collection 4
[Design   ] <- collection 3
[Requirements] <- collection 2
[Meta     ] <- collection 1  (bottom)
```

Push: adding a new SDLC phase for an artifact (e.g., writing the test after the code).
Peek: viewing any layer without changing context.
Walk: advancing collection to trace an artifact through its lifecycle.

## UML Integration

Collections 2 (Requirements) and 3 (Design) are UML-dominant:

- Use case diagrams, activity diagrams in Collection 2
- Class diagrams, sequence diagrams, component diagrams in Collection 3

These diagrams are *live entry points*. A class in a design diagram at `3/1.2.1/1.1`
links structurally to its source at `4/1.2.1/1.1`, tests at `5/1.2.1/1.1`, and docs
at `7/1.2.1/1.1` — same 5D address, different collection.

## Design Principles

1. **One file**: The entire system lives in a single phext document.
2. **Structural traceability**: The coordinate system IS the traceability matrix.
3. **Living system**: Diagrams are portals, not pictures.
4. **Runtime configurable**: Collection assignments and artifact mappings are stored
   in Collection 1 (Meta) and can be updated without restructuring the document.
5. **Git-friendly**: Plain text with version control.
