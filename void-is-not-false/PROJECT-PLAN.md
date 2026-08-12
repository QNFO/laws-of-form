# WBS: QNFO.SLB.002

# The Void Is Not False: Recovering the Unmarked State in Logic from the Calculus of Indications

**Program:** QNFO.SLB (Laws of Form / Spencer-Brown)
**Project:** QNFO.SLB.002
**Slug:** `void-is-not-false`
**Status:** Phase 0 (Init)
**Date:** 2026-08-12
**Parent treatise:** *The Calculus of Re-Entrant Distinctions* — DOI 10.5281/zenodo.21906728 (living-paper canonical; concept-chain includes 10.5281/zenodo.21905186)

---

## 1. Charter

Boolean logic commits a foundational category error: it treats the void — the unmarked state before any distinction — as if it were a member of the system, namely the truth value `false`. This project develops the thesis that `false` is itself a mark, a positive distinction, and that the true void is not a truth value at all. The conflation of void and false produces the static, well-founded, self-reference-free character of classical logic and set theory. Returning to the calculus of indications recovers a logic in which negation is an act of crossing a boundary, excluded middle is a local property of clearly drawn distinctions, and self-reference — far from being a paradox to be banned — generates oscillation, time, and the imaginary truth value.

This is the **void spinoff** of the parent treatise: a standalone critique of Boolean logic (and the set-theoretic treatment of `∅`) from the calculus of indications.

## 2. Locked Core Claim (P6)

`[TERRITORY — claimed identity]` **The unmarked state (the void) is not a truth value; `false` is itself a mark, and Boolean logic's identification of void with `false` is a category error that forces a static, tree-only logic without re-entry.** Negation is the act of crossing a boundary, not the mapping to a second primitive value.

**Falsifiability condition (KIF-60):** The claim is disconfirmed if either (a) a formal account of classical Boolean semantics is produced that treats `false` as genuinely unmarked — i.e., absence of any mark — without losing any Boolean theorem, demonstrating that the reification is eliminable rather than structural; or (b) the re-entrant calculus of indications (with the imaginary truth value) is shown unable to reproduce the valid fragment of classical logic it claims to generalize. Until one of these is demonstrated, the claim remains `[my conjecture]` and is published as such.

**Confirmation-seeking test:** the reconstruction must discriminate against a serious alternative — e.g., intuitionistic or paraconsistent logic, which also reject Boolean bivalence but without any appeal to the unmarked state — and show that the void/false distinction yields a genuinely different (not merely re-labeled) semantics.

## 3. Phases with WBS

| Phase | WBS | Deliverable | Gate |
|:------|:----|:------------|:-----|
| P0 Init | QNFO.SLB.002.P0 | PROJECT-PLAN.md, branch `slb/paper/void-is-not-false`, core claim locked | P1-P11 checklist HARD |
| P1 Due Diligence | QNFO.SLB.002.P1 | KG + D1 + Vectorize + external cross-ref | artifacts/external-search/ |
| P2 Literature | QNFO.SLB.002.P2 | 8-source search, dedup, classify, KIF-18 symmetry template | Mandatory Symmetry Template |
| P3 Citations | QNFO.SLB.002.P3 | verified BibTeX (P3.AUTHOR-GATE) | citation-audit.md |
| P4 Deep Research | QNFO.SLB.002.P4 | formal distinction-logic reconstruction, imaginary truth value, red-team, calibration | bayesian-evidential-weight.md |
| P5 Publication | QNFO.SLB.002.P5 | `<slug>.md` + PDF (CDP pipeline) + Zenodo DOI | BP-1..BP-10 gates |
| P6 Deployment | QNFO.SLB.002.P6 | D1 living-paper, papers-server, KG node, Vectorize | 4-layer verification |
| P7 Dissemination | QNFO.SLB.002.P7 | journal submission, outreach, SEO | QA/UX battery |
| P8 Core Distribution | QNFO.SLB.002.P8 | GitHub tag, Zenodo newversion, R2 archive, closeout verification | Consolidated Closeout |

## 4. Milestones

| Milestone | Gate criteria |
|:----------|:--------------|
| M1 Phase 0 complete | Branch pushed, PROJECT-PLAN.md committed, core claim locked with falsifiability condition |
| M2 Due diligence complete | ≥1 external source constraining/contradicting the claim (KIF-18), evidence files saved |
| M3 Distinction-logic reconstruction complete | formal semantics for a logic of marks (inside/outside/oscillating) written and internally verified |
| M4 Publication | Zenodo DOI resolves HTTP 200; P5.FRESH yaml_ok; 4-layer distribution verified |

## 5. Deliverable Registry

| Deliverable | Path | Status |
|:------------|:-----|:-------|
| PROJECT-PLAN.md | `void-is-not-false/PROJECT-PLAN.md` | ✅ Phase 0 |
| Paper (markdown) | `void-is-not-false/void-is-not-false.md` | pending |
| PDF | `void-is-not-false/void-is-not-false.pdf` | pending |
| HTML | `void-is-not-false/void-is-not-false.html` | pending |
| research-continuity-registry.md | `void-is-not-false/docs/` | pending (Phase 5 trigger) |

## 6. Risk Register

| Risk | Severity | Mitigation |
|:-----|:---------|:-----------|
| KIF-60 retrodiction: the void/false distinction is a re-labeling of intuitionistic/paraconsistent semantics | HIGH | Locked confirmation-seeking test names intuitionistic/paraconsistent logic as the alternative; the reconstruction must show a genuinely different semantics, not a re-labeled one |
| Absorption trap: every counterexample absorbed as "re-entry oscillation" | MEDIUM | Pre-declare allowed duality maps; document which structures the framework FAILS to map |
| Title/filename hygiene (TITLE-DUPLICATION-1, FILE-SLUG-1) | LOW | Scripted gates at P5 build time |

## 7. Success Criteria

1. A formal, internally verified reconstruction of logic on the primacy of distinction and re-entry — syntax (mark, crossing, re-entry), semantics (configurations; void as empty configuration), and dynamics (re-entry as fixed point).
2. Publication with Zenodo DOI, D1/KG/Vectorize integration (PUBLICATION-KG-INDEX-GAP-1 gates).
3. Every cross-domain correspondence claim passes the KIF-60 Bayesian evidential weight gate (Δlog-odds > 0 or labeled `[RETRODICTION — not evidence]`).
