# Bayesian Evidential Weight Gate (KIF-60) — QNFO.SLB.001 idempotent-core

**Phase 4 (P4) gate artifact** | **Date:** 2026-08-12
**Applies to:** every cross-domain / structural correspondence claim in this project.

---

## 1. Pre-Registration Record

Timestamped predictions (this session, git-committed in `PROJECT-PLAN.md` §2 and this artifact):

- **P1 (locked P6):** "Idempotence of the mark ($AA = A$) is the primitive law; arithmetic/algebra are derived via deliberately-broken idempotence + the `!` modality." — committed 2026-08-12, branch `slb/paper/idempotent-core`, commit `cbdedac`.
- **P2 (P4 sketch, Conjecture C1):** "The Grothendieck group completion of the NNO in the coKleisli category of `!`, with crossing as the canonical involution, is the ring $\mathbb{Z}$." — committed 2026-08-12 in `docs/deep-research.md`.

## 2. Falsifiability Matrix

| Claim | Disconfirmation condition |
|---|---|
| P1 (primitive idempotence) | A derivation of $\mathbb{Z}$ from `!` is circular (imports ring axioms), OR `!` is eliminable |
| P2 (C1: group completion yields the ring) | The group completion of the NNO does not recover distributivity; or the crossing is not a canonical involution |
| Derived-ring consequence | A Peano-style successor axiomatization without linear logic reproduces the same ring (confirmation-seeking alternative) |

## 3. Surprise Accounting

For the correspondence "idempotence (law of calling) ↔ ring structure of $\mathbb{Z}$":

- **Null model:** random structural similarity between a one-generator idempotent algebra and $\mathbb{Z}$. Prior estimate: $P(\text{match} \mid \text{random}) \lesssim 0.01$ for the *specific* ring structure (associativity + distributivity + inverses) — the correspondence is not trivially expected.
- **However:** the framework was *built* to produce this match (the parent treatise). Under the overfitting null, $P(\text{match} \mid \text{framework built to match})$ ≈ 1.
- **Net:** $\Delta \log\text{-odds} \approx 0$ **at present** — the claim is `[RETRODICTION — not evidence]` until the derivation is a *proven theorem* independent of the framework's construction choices.

## 4. Δlog-odds Summary

| Claim | Δlog-odds | Status |
|---|---|---|
| P1 (idempotence primitive) | ~0 (framework built to match) | `[NOT YET EVIDENCE]` |
| P2 (C1: $\mathbb{Z}$ from `!`) | ~0 (no derivation yet) | `[RETRODICTION — not evidence]` until proven |
| Critique (hidden premise of addition: two distinguishable marks) | > 0 (independent of construction; a genuine observation) | Candidate positive weight — **but is a critique, not a correspondence** |

## 5. Trap Audit

| Trap | Check |
|---|---|
| Overfitting | Degrees of freedom: the framework can re-describe any structure as "distinctions + `!`". Mitigation: the specific ring structure is a *constrained* target; dof vs matches must be re-audited once a derivation exists. |
| Cherry-picking | Denominator: how many structures were checked? Only the ring structure is claimed; p-adic/field completions are explicitly deferred (Phase 5+). No cherry-picking. |
| Absorption | Allowed dualities pre-declared? Not yet — the set of allowed duality maps must be fixed BEFORE counterexamples are examined (P4 open item). |

## 6. Gate Output

**Verdict: BLOCK the correspondence claims as evidence until Step 4 (Conjecture C1/C2) is a proven theorem.** The critique portion (arithmetic's hidden premise) carries candidate positive weight and may proceed as a standalone claim. This gate is the P4 red-team target: any publication that presents "ℤ from `!`" as established without this gate passing is a research-integrity violation.
