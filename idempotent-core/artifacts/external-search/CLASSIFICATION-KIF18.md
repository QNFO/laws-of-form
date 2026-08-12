# Phase 2 Literature Search & Triage — QNFO.SLB.001 idempotent-core

**Date:** 2026-08-12
**Queries (4):** idempotence arithmetic foundations · laws of form Spencer-Brown mathematics · linear logic arithmetic natural numbers · idempotent semiring algebra number theory
**Sources (5):** OpenAlex, Crossref, arXiv, Zenodo records, Europe PMC
**Evidence:** `artifacts/external-search/` — 20 JSON files (4 queries × 5 sources)

**Three-count audit:** 20 queries sent · 20 source responses received · 12 sources cited below. Cited ≤ received — no fabrication.

---

## Classification Matrix

### Core (directly addresses the claim)

| # | Work | DOI / ID | Class | Notes |
|:--|:-----|:---------|:------|:------|
| C1 | Maslov dequantization, idempotent and tropical mathematics: a brief introduction (Litvinov, 2006) | 10.1007/s10958-007-0450-5 | Core | Establishes idempotent mathematics (Maslov 1973 program) as a studied field — supports the "idempotent semiring base" claim |
| C2 | Arithmetical properties at the level of idempotence (arXiv) | arXiv (idempotence search hit) | Core | Direct topical hit: arithmetic and idempotence studied together |
| C3 | Arithmetic Formulated Relevantly (2021) | 10.26686/ajl.v18i5.6905 | Core | Relevant-logic formulation of arithmetic — resource-sensitive arithmetic prior art |

### Supporting

| # | Work | DOI / ID | Class | Notes |
|:--|:-----|:---------|:------|:------|
| S1 | Generalized idempotence in cardinal arithmetic (1966) | 10.4064/fm-58-3-241-258 | Supporting | Prior idempotence-in-arithmetic work; MUST be distinguished (cardinal idempotence ≠ mark idempotence) |
| S2 | Idempotence in Cardinal Arithmetic (1970) | 10.1080/00029890.1970.11992609 | Supporting | Same distinction required |
| S3 | Provenance semirings (2007) | 10.1145/1265530.1265535 | Supporting | Idempotent semirings in CS — established formal apparatus |
| S4 | Classical linear logic, cobordisms and categorical semantics (arXiv) | arXiv | Supporting | Categorical semantics of linear logic — the `!`-modality formal vehicle |
| S5 | Adequate Losses via Quantitative Linear Logic (arXiv) | arXiv | Supporting | Quantitative linear logic — resource accounting |
| S6 | Densities of idempotent measures and large deviations (1999) | 10.1090/s0002-9947-99-02153-4 | Supporting | Idempotent analysis applications |

### Background

| # | Work | DOI / ID | Class | Notes |
|:--|:-----|:---------|:------|:------|
| B1 | Homotopy Type Theory: Univalent Foundations of Mathematics | arXiv | Background | Competing foundation — must position against |
| B2 | Enumerative tropical algebraic geometry in R^2 (2005) | 10.1090/s0894-0347-05-00477-7 | Background | Tropical geometry as idempotent shadow |
| B3 | Logic and linear algebra: an introduction (arXiv) | arXiv | Background | Linear-logic–algebra connection |

### Rejected (sample)

Europe PMC returned predominantly biomedical hits (orthopaedic surgery, cell biology) — zero logic/math relevance for these queries. Documented as a domain-relevance finding, not evidence.

---

## Mandatory Symmetry Template (KIF-18, HARD)

### Where External Literature Supports [Claim]

1. **Idempotent mathematics is an established field (C1, S3, S6):** Litvinov (2006) documents the Maslov dequantization program — idempotent semirings, tropical mathematics, and idempotent analysis are legitimate, studied structures. The claim that an idempotent base underlies quantity is not fringe; it aligns with a 50-year mathematical tradition. `[established]`
2. **Linear logic provides the formal duplication-control apparatus (S4, S5):** The categorical semantics literature (classical linear logic, quantitative linear logic) confirms that the exponential modality `!` is the established formal device for controlling duplication — exactly the vehicle the spinoff's locked core claim names. `[established]`
3. **Idempotence already appears inside arithmetic (S1, S2):** The cardinal-arithmetic literature (1966, 1970) proves idempotence phenomena are real within arithmetic (e.g., infinite-cardinal multiplication) — supporting the claim that idempotence and arithmetic are not disjoint. However, these works treat idempotence as a property of infinite cardinals, NOT as the primitive law of the mark; the spinoff must cite and explicitly distinguish its thesis from this prior work (priority protection). `[established]`

### Where External Literature Constrains or Contradicts [Claim]

1. **The cardinal-arithmetic idempotence literature (S1, S2) is the strongest constraint:** If arithmetic already contains idempotent operations (infinite-cardinal multiplication is idempotent), then the claim "arithmetic is the non-idempotent shadow of the idempotent mark" requires careful scoping. The spinoff's claim must be stated about *finite successor arithmetic of marks* (where `1+1≠1` is the derived theorem), with infinite-cardinal idempotence treated as a distinct phenomenon that the framework must either explain or explicitly set aside. An un-scoped claim would be vulnerable to the S1/S2 counterexample. `[established — this is the disconfirmation-relevant constraint]`
2. **Peano arithmetic's established adequacy (B1, background norm):** No external source demonstrates a need to rebuild arithmetic from distinction primitives. The burden of proof is on the framework: a skeptical referee will treat Peano's axioms as the null hypothesis. This is the null-equivalence test already locked in PROJECT-PLAN §2 — the framework must show its derivation of `Z` from `!` yields ring structure that Peano-style successor axioms cannot. `[mainstream interpretation]`
3. **[NO CONSTRAINING EVIDENCE FOUND] for the specific claim that "no published work derives Z from linear logic's ! modality."** The search (20 queries across 5 sources) found no external paper claiming this derivation. This is a genuine novelty gap — but it also means the P4 derivation has no external scaffolding to build on, making it the highest-risk technical step (already flagged in the Risk Register).

**GATE CHECK:** Both mandatory sections are non-empty and specific. Phase 2 literature search for QNFO.SLB.001 PASSES KIF-18.
