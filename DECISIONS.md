# Architecture Decision Records — Primordial Mark

## ADR-0001: Project Name — "primordial-mark"

**Status:** Accepted
**Date:** 2026-05-23

### Context

The project was initially created as "Primordial Mark" (with space). When formalizing the project, we needed a proper slug for the directory name. The content across all 5 files centers on Spencer-Brown's "Mark" — the primordial act of distinction — as the fundamental generative engine. The user instructed renaming to a "more suitable project name/slug from contents."

### Decision

We renamed from "Primordial Mark" to "primordial-mark" — keeping the core concept intact while converting to kebab-case. The name accurately reflects the content: the Mark as primordial primitive.

### Consequences

- **Easier:** Git operations, path references, and cross-project linking use a clean slug
- **Harder:** None
- **Risks Accepted:** None

---

## ADR-0002: Differentiation from ultrametric-tree-universality

**Status:** Proposed
**Date:** 2026-05-23

### Context

Due diligence revealed that `ultrametric-tree-universality` (Archive 2026/05) covers the same core topic (ultrametric tree universality, Spencer-Brown, molecular clock) and produced a publication-ready document. The primordial-mark project must differentiate to avoid duplication.

### Decision

We will differentiate by focusing on:
1. **The primitive itself** — formal definition of the Mark as mathematical primitive (not just survey of where trees appear)
2. **Classification of Finite Simple Groups connection** — how CFSG emerges from the Mark (unique to this project)
3. **10-adic / positional ontology** — the "Be 10 by virtue of zero position" insight (unique to this project)
4. **Synthesis across all 5 threads** — producing a unified framework rather than a domain survey

We will NOT re-survey the 8 domains already covered in ultrametric-tree-universality 0.3.md.

### Consequences

- **Easier:** Clear unique contribution, avoiding duplication
- **Harder:** Must carefully reference but not repeat prior work
- **Risks Accepted:** Risk of insufficient differentiation if the synthesis doesn't go deep enough into the primitive

---

## ADR-0003: Keep empty 0.1.5.1.md

**Status:** Proposed
**Date:** 2026-05-23

### Context

The file `0.1.5.1.md` exists but is 0 bytes. It may be an intentional placeholder or a failed write.

### Decision

Keep the file for now as part of the project provenance. If confirmed as unintentional during content audit, it will be deleted.

### Consequences

- **Easier:** Preserves full project history
- **Harder:** None
- **Risks Accepted:** Minimal — 0-byte file has no material impact

---
*Generated from ADR-TEMPLATE.md v1.0*
