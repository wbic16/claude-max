# claude-max

A persistent knowledge workspace for capturing software development context that would otherwise be lost to time.

Inspired by *Flight of the Navigator* - this repo serves as a shared memory between a developer with 30 years of experience and an AI assistant, preserving insights, decisions, and context that typically evaporate between sessions.

## Purpose

Software development generates enormous amounts of tacit knowledge: why a particular architecture was chosen, what was tried and failed, the subtle constraints that shaped a design. Most of this context lives only in the developer's head and fades over time.

This workspace captures that knowledge in a durable, version-controlled form - a navigational chart for the journey so far and the road ahead.

## 6D UML

The core artifact is `uml6d.phext` - a single phext document encoding an entire software system across 6 dimensions. See [SPEC.md](SPEC.md) for the full specification.

**Coordinate Map:**
- **Collection** (8D) = SDLC Phase (Meta, Requirements, Design, Source, Tests, ...)
- **Volume** (7D) = Sprint/Release
- **Book** (6D) = Module
- **Chapter** (5D) = Component
- **Section** (4D) = File
- **Scroll** (3D) = Unit

An artifact's 5D address (volume.book.chapter/section.scroll) is stable across all SDLC phases. Walk the collection dimension to trace any artifact from requirement to training.

Built on [phext](https://phext.io/) ([libphext-rs](https://github.com/wbic16/libphext-rs)).
