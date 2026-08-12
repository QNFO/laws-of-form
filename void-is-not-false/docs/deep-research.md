# Deep Research — QNFO.SLB.002 void-is-not-false

**WBS:** QNFO.SLB.002 | **Phase 4 (P4)** | **Date:** 2026-08-12
**Core claim (locked, PROJECT-PLAN §2):** The unmarked state (the void) is not a truth value; `false` is itself a mark, and Boolean logic's identification of void with `false` is a category error that forces a static, tree-only logic without re-entry.
**Status:** Research sketch. `[my conjecture]` unless labeled otherwise. Not a publication claim.

---

## 1. Domain Assessment

The claim lives at the intersection of:

1. **Calculus of Indications / Laws of Form** (Spencer-Brown 1969): the unmarked state, the mark, crossing, re-entry.
2. **Boolean Logic / Classical Propositional Logic**: the treatment of `false` as a primitive truth value.
3. **Non-classical logics** (intuitionistic, paraconsistent, trivalent): the named alternatives the reconstruction must discriminate against.

Active paradigms: Boolean logic as the default formal semantics (mainstream); paraconsistent logic (Priest; Mortensen) as the leading challenge to bivalence; intuitionistic logic as the constructive alternative. Key question: is there a semantics in which the void is *not* a truth value, negation is *crossing*, and re-entry produces a genuinely new (oscillating) semantic state?

## 2. Reconstruction Sketch: A Logic of Distinctions

### Syntax (established)

Primitive expressions: the mark (a boundary with inside/outside), juxtaposition, the unmarked state (empty configuration). Re-entry: a mark may refer to its own form.

### Semantics — states are configurations of marks (established base)

A *state* is a finite configuration of marks. The **void is the empty configuration** — not a member of the value set, but the background against which configurations exist.

- Truth values are *not* primitives. `true` and `false` are *orientations of a boundary*: inside = true, outside = false, relative to a drawn boundary.
- **Negation is crossing** — the act of passing from inside to outside — not the mapping to a second primitive value. `[established — Spencer-Brown]`

### The category error (the critique)

Boolean logic reifies the void into the value `false` ($0$); set theory does the same with $\emptyset$. Both treat absence as a member of the system. The critique: $0$ and $\emptyset$ are *marks* (positive distinctions), not the unmarked state. `[my conjecture — the interpretive claim]`

### The oscillating state (the novel core)

**`[my conjecture]` Conjecture V1:** the re-entrant equation $f = \overline{f}$ (a mark indicating its own negation) has no static solution but has a *dynamic* solution: the configuration oscillates between marked and unmarked. This "imaginary truth value" (Spencer-Brown's Chapter 11) is neither true nor false — it is a **phase**.

**`[my conjecture]` Conjecture V2:** the semantics of distinctions (inside / outside / oscillating) is genuinely different from:
- **intuitionistic logic** — which rejects excluded middle but keeps all propositions as stable (static) truths; it has no oscillating state;
- **paraconsistent logic** — which rejects explosion but keeps static valuations; it has no unmarked-state-as-background;
- **neutrosophic/trivalent logic** — which adds a third *static* value; the distinction-logic's third state is *dynamic*.

The confirmation-seeking test (locked in PROJECT-PLAN): exhibit a formula whose semantic value in distinction-logic is oscillation while intuitionistic and paraconsistent semantics assign a static value. If no such formula exists, the distinction-logic semantics is a re-labeling — disconfirmed.

### Reproducing the valid classical fragment

Classical Boolean logic is the *restriction of distinction-logic to static configurations* (no re-entry, no oscillation). Excluded middle holds locally for clearly drawn boundaries (every configuration is either inside or outside a given boundary), which recovers the valid classical fragment without treating the void as a value.

## 3. Assumption Audit

| # | Assumption | Type | Status |
|---|---|---|---|
| A1 | The unmarked state is the empty configuration, not a value | Enabling | Established (Spencer-Brown; parent treatise §1.1) |
| A2 | Negation is crossing | Enabling | Established |
| A3 | Re-entry produces a genuine oscillating state | Blocking | **Unproven formal semantics (Conjecture V1)** |
| A4 | The oscillating state discriminates from intuitionistic/paraconsistent | Blocking | **The confirmation-seeking test (Conjecture V2)** |
| A5 | Boolean logic is the static restriction | Enabling | Established (Boundary Algebra literature; Bricken/Meguire) |

## 4. Red-Team Challenge (5 adversary positions)

1. **Null-Hypothesis Defender:** paraconsistent logic already handles "both true and false" — the oscillating state must be shown to be *more* than a paraconsistent dialetheia.
2. **Methodology Skeptic:** "false is a mark, the void is not" may be a terminological re-labeling of the familiar empty-type/empty-set distinction; the framework must show a *logical* (not philosophical) consequence.
3. **Better-Alternative Proposer:** intuitionistic semantics (Kripke models) already handles unproven/unknown states constructively; is distinction-logic genuinely different or a notational variant?
4. **Scaling Pessimist:** a formal semantics with a dynamic (time-indexed) truth value requires a notion of time/phase; importing time risks circularity with the parent treatise's "time from re-entry" claim.
5. **Resource Realist:** building a proof assistant or a complete semantics is a large undertaking; the risk is the reconstruction stays a philosophical narrative.

## 5. Judgment Sensitivity

- **Pessimistic:** the oscillating state collapses into paraconsistent dialetheism → the spinoff reduces to "a paraconsistent logic with a philosophical gloss" (weakest defensible position).
- **Optimistic:** V1 and V2 hold and the semantics is genuinely three-valued-with-dynamics → the spinoff is a new logical framework with the void as background, not a value.
- **Verdict:** CONDITIONAL — depends on V2 (the discrimination).

## 6. Calibration Register

```
[CHECK: 2027-08] Formal semantics for distinction-logic (inside/outside/oscillating)
   with the confirmation-seeking formula exhibited. Strength: [MEDIUM].
[CHECK: 2028-08] Independent formalization showing the oscillating state is not
   reducible to a static three-valued (neutrosophic/trivalent) logic. Strength: [WEAK].
[CHECK: 2030-08] Adoption of "void is not false" terminology in at least one
   external treatment of Laws of Form / paraconsistent logic. Strength: [WEAK].
```

## 7. Research Effort Allocation

| Task | Share |
|---|---|
| Formal semantics for the oscillating state (V1) | 40% |
| Confirmation-seeking discrimination test (V2) | 30% |
| Position against paraconsistent/intuitionistic literature | 15% |
| Classical-fragment recovery proof | 10% |
| Proof-assistant encoding | 5% |

## 8. Practical Applications Extension (Stage 9)

| Domain | Operational signature | Falsifiable claim |
|---|---|---|
| Quantum logic | Superposition as the oscillating state; measurement as boundary crossing | The imaginary truth value corresponds to a phase (not a static third value) |
| Paraconsistent computation | A trivalent/dynamic semantics for inconsistent databases | Distinction-logic handles oscillation where static paraconsistency cannot |
| Foundations of mathematics | Non-well-founded set theory as a loop-logic | Re-entry is a higher inductive type (HoTT connection) |
| Philosophy of logic | The void/false distinction as the ground of bivalence | Boolean logic is the static restriction of distinction-logic |

## 9. Counterfactual Backcasting (Stage 10)

- **Tier 1 (~20 yr):** if no discrimination is shown, the spinoff remains a philosophical critique of Boolean semantics (defensible) without a new logic.
- **Tier 2 (~60 yr):** if V2 holds, the 20th-century ban on self-reference is revealed as a choice, not a necessity — the tree-only logic was one restriction of a loop-capable logic.
- **Tier 4 (alternate axioms):** if the void had been kept distinct from false in early formal logic, the development of paraconsistent and quantum logics would have had a ready-made semantics; the counterfactual table shows ~60 years of separate development (silo cost).

## 10. Strategic Memo

The spinoff's immediate value is the **critique** (void ≠ false is defensible now). The reconstruction (distinction-logic with an oscillating state) is the ambitious core but is `[my conjecture]` until V1/V2 are formalized. Publication strategy: publish the critique first, then the semantics as a follow-up when the confirmation-seeking formula is exhibited. Do NOT claim a new logic before the discrimination is proven.
