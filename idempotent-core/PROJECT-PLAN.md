# WBS: QNFO.SLB.001

# The Idempotent Core: Quantity as Broken Distinction and the Hidden Assumptions of Arithmetic and Algebra

**Program:** QNFO.SLB (Laws of Form / Spencer-Brown)
**Project:** QNFO.SLB.001
**Slug:** `idempotent-core`
**Status:** Phase 0 (Init)
**Date:** 2026-08-12
**Parent treatise:** *The Calculus of Re-Entrant Distinctions* — DOI 10.5281/zenodo.21906728 (living-paper canonical; concept-chain includes 10.5281/zenodo.21905186)

---

## 1. Charter

Classical arithmetic treats `1+1=2` as a primitive axiom and quantity as fundamental. This project develops the inverse thesis: the **distinction** is primitive, and idempotence (`AA = A`, the law of calling) is the first law of the mark. Repetition of the same mark does not produce a second mark; it produces the same mark. Therefore `1+1=2` is a theorem about two *distinguishable* marks, not a primitive truth. Addition, multiplication, the natural numbers, rings, and fields arise only after idempotence is deliberately broken by introducing new boundaries and controlled duplication. The formal vehicle is linear logic, where the exponential modality `!` governs the transition from the idempotent base to the non-idempotent shadow of classical algebra.

This is the **idempotence spinoff** of the parent treatise: a standalone critique of arithmetic and algebra from the calculus of indications.

## 2. Locked Core Claim (P6)

`[TERRITORY — claimed identity]` **Idempotence of the mark (`AA = A`) is the primitive law; classical arithmetic and algebra are derived structures that exist only after idempotence is deliberately broken via new boundaries and controlled duplication formalized by the linear-logic exponential modality `!`.** Quantity is not the repetition of the same; it is the creation of new distinctions.

**Falsifiability condition (KIF-60):** The claim is disconfirmed if either (a) a formal derivation of the ring of integers `Z` (or even `N` with its ring structure) from the `!` modality in a differential linear category is shown to require importing classical arithmetic as an unanalysed axiom — i.e., the derivation is circular — or (b) an idempotent-free derivation of arithmetic from distinction primitives is produced that makes the `!` modality eliminable without loss. Until one of these is demonstrated, the claim remains `[my conjecture]` and is published as such.

**Confirmation-seeking test:** the proposed derivation must discriminate against a serious alternative — e.g., a Peano-style successor axiomatization built directly on distinction primitives WITHOUT linear logic — and show that the `!`-modality path yields ring structure the alternative cannot.

## 3. Phases with WBS

| Phase | WBS | Deliverable | Gate |
|:------|:----|:------------|:-----|
| P0 Init | QNFO.SLB.001.P0 | PROJECT-PLAN.md, branch `slb/paper/idempotent-core`, core claim locked | P1-P11 checklist HARD |
| P1 Due Diligence | QNFO.SLB.001.P1 | KG + D1 + Vectorize + external cross-ref | artifacts/external-search/ |
| P2 Literature | QNFO.SLB.001.P2 | 8-source search, dedup, classify, KIF-18 symmetry template | Mandatory Symmetry Template |
| P3 Citations | QNFO.SLB.001.P3 | verified BibTeX (P3.AUTHOR-GATE) | citation-audit.md |
| P4 Deep Research | QNFO.SLB.001.P4 | formal derivation of `Z` from `!` modality (the critical step), red-team, calibration | bayesian-evidential-weight.md |
| P5 Publication | QNFO.SLB.001.P5 | `<slug>.md` + PDF (CDP pipeline) + Zenodo DOI | BP-1..BP-10 gates |
| P6 Deployment | QNFO.SLB.001.P6 | D1 living-paper, papers-server, KG node, Vectorize | 4-layer verification |
| P7 Dissemination | QNFO.SLB.001.P7 | journal submission (Frontiers in Physics ★), outreach, SEO | QA/UX battery |
| P8 Core Distribution | QNFO.SLB.001.P8 | GitHub tag, Zenodo newversion, R2 archive, closeout verification | Consolidated Closeout |

## 4. Milestones

| Milestone | Gate criteria |
|:----------|:--------------|
| M1 Phase 0 complete | Branch pushed, PROJECT-PLAN.md committed, core claim locked with falsifiability condition |
| M2 Due diligence complete | ≥1 external source constraining/contradicting the claim (KIF-18), evidence files saved |
| M3 Formal derivation complete | `Z`-ring derivation from `!` modality written and internally verified (BP-6 recompute) |
| M4 Publication | Zenodo DOI resolves HTTP 200; P5.FRESH yaml_ok; 4-layer distribution verified |

## 5. Deliverable Registry

| Deliverable | Path | Status |
|:------------|:-----|:-------|
| PROJECT-PLAN.md | `idempotent-core/PROJECT-PLAN.md` | ✅ Phase 0 |
| Paper (markdown) | `idempotent-core/idempotent-core.md` | pending |
| PDF | `idempotent-core/idempotent-core.pdf` | pending |
| HTML | `idempotent-core/idempotent-core.html` | pending |
| research-continuity-registry.md | `idempotent-core/docs/` | pending (Phase 5 trigger) |

## 6. Risk Register

| Risk | Severity | Mitigation |
|:-----|:---------|:-----------|
| KIF-60 retrodiction: derivation of `Z` is circular (imports arithmetic as axiom) | HIGH | Falsifiability condition (a) explicitly states the circularity disconfirmation; the derivation is the first P4 deliverable, red-teamed before any publication claim |
| Confirmation-seeking: `!`-modality path not discriminating against Peano-style alternative | MEDIUM | Locked confirmation-seeking test names the alternative at P6 |
| Title/filename hygiene (TITLE-DUPLICATION-1, FILE-SLUG-1) | LOW | Scripted gates at P5 build time |

## 7. Success Criteria

1. A complete, non-circular formal derivation of the ring structure of `Z` (or at minimum `N` with ring structure) from the `!` modality in a differential linear category, internally verified.
2. Publication with Zenodo DOI, D1/KG/Vectorize integration (PUBLICATION-KG-INDEX-GAP-1 gates).
3. Every cross-domain correspondence claim passes the KIF-60 Bayesian evidential weight gate (Δlog-odds > 0 or labeled `[RETRODICTION — not evidence]`).
