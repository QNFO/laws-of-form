---
title: "The Idempotent Core: Quantity as Broken Distinction and the Hidden Assumptions of Arithmetic and Algebra"
author: "Rowan Brad Quni-Gudzinas"
date: "2026-08-13"
license: "QNFO Unified License Agreement (QNFO-ULA)"
doi: "TBD"
status: "draft"
---

## Abstract

Classical arithmetic treats the statement $1+1=2$ as a primitive truth and quantity as a fundamental concept. This paper examines the hidden premise of that statement: the two instances of the numeral $1$ must denote *distinct* marks. In the calculus of indications, the law of calling — idempotence of the mark, $AA = A$ — states that repeating the same mark yields the same mark. If the two occurrences of $1$ were literally the same mark, addition would collapse to $1+1=1$. Quantity therefore presupposes the creation of new distinctions, and the natural numbers are generated not by repetition but by successive acts of distinction. The paper presents this critique as its defensible claim, and then outlines a reconstruction program in which the exponential modality of linear logic provides the controlled duplication that breaks idempotence, yielding the integers as the group completion of the natural numbers object in the coKleisli category of that modality. The reconstruction is labeled conjecture: its central claims are unproven, and the evidential-weight boundary between the critique and the program is stated explicitly. Claims marked `[my conjecture]` carry falsifiability conditions and are not presented as established results.

**Keywords:** idempotence; laws of form; calculus of indications; foundations of arithmetic; linear logic; quantity

## 1. Introduction

The Peano axioms define the natural numbers by a successor operation, but they do not explain what makes one number *distinct* from another. The successor of $n$ is a new object, yet the axiom of extensionality for numerals says nothing about why the successor is new rather than a repetition of the old. Classical arithmetic treats this as a primitive: counting works, and that is the end of the matter.

This paper takes the opposite route. It begins with the simplest formal system in which distinctness is the only primitive — Spencer-Brown's calculus of indications [1, 2] — and examines what that system says about the foundations of arithmetic. The calculus has two primitive acts: drawing a distinction, and the laws that govern repeated indication. The law of calling states that a mark indicated twice is the same as a mark indicated once: $AA = A$. This is idempotence, and it is not a special property of conjunction; it is the mark's refusal to be counted [1, 2].

If idempotence is the primitive law of the mark, then the statement $1+1=2$ carries a hidden assumption: the two marks called "$1$" must be distinguishable. The critique developed in Sections 2–4 is that arithmetic silently imports this distinctness without acknowledging it, and that the entire edifice of quantity is built on the controlled violation of idempotence rather than on an axiom of counting. Section 5 outlines the reconstruction program — the route from the idempotent mark to the ring of integers through linear logic — and labels its central conjectures with their falsifiability conditions. Section 6 connects the resulting picture to valuation theory. Section 7 states the epistemic boundary of the work explicitly.

## 2. The Calculus of Indications as Ground

The calculus of indications begins with the unmarked state: no boundary has been drawn, no distinction made [1]. The first act is the drawing of a distinction, which creates three things at once: a marked state (the inside), an unmarked state (the outside), and the boundary between them [1].

The mark obeys two primitive laws. The law of calling:

$$AA = A$$

states that to call a name again is to call the same name. The law of crossing:

$$\overline{\overline{x}} = x$$

states that a boundary crossed twice returns to the unmarked [1]. The first law is idempotence; the second is involution. Together they define the behavior of the mark as a distinction rather than as a quantity.

The formal content of this section is established in the literature [1, 2]. The interpretive claim — that idempotence is the primitive law from which quantity must be derived — is the thesis of this paper.

## 3. The Hidden Premise of Addition

Consider the statement

$$1+1=2.$$

Standard presentations treat this as an axiom or as an immediate consequence of definitions. The claim of this section is that the statement presupposes that the two occurrences of $1$ are *distinct marks*. The evidence is the law of calling: if the second $1$ were the same mark as the first, idempotence would give $1+1 = 1$, not $1+1 = 2$. `[established — Spencer-Brown 1969]` The law of calling is not controversial; what is often missed is its bearing on the foundations of arithmetic.

For $1+1=2$ to hold, the two marks must be distinguishable by at least one new feature: a position, a label, a time of inscription, or a nesting depth. In the von Neumann construction, the successor of $n$ is $n \cup \{n\}$, which is a genuinely new set because the old set is included as an element; the construction works because it creates a new distinction at every step. The arithmetic that follows inherits that distinctness without naming it.

The critique, stated precisely: **addition is a theorem about distinguishable marks, not a primitive truth about repetition.** `[my conjecture]` This claim is disconfirmed if a formulation of the natural numbers is produced in which the successor of a numeral is the same mark as its predecessor — that is, if repetition alone generates counting without any new distinction. No such formulation is known. The claim is also disconfirmed if the law of calling is shown not to apply to numerals, i.e., if a numeral can be a genuine repeat of another numeral while still producing a new count. `[my conjecture]` Both conditions are concrete and checkable, so the claim is falsifiable.

The relevance of this critique to existing literature is direct. The study of idempotence inside cardinal arithmetic [4, 5] shows that multiplication of infinite cardinals is idempotent ($\kappa \cdot \kappa = \kappa$), which is a genuine idempotence phenomenon *within* arithmetic; the present critique is scoped to finite successor arithmetic of marks and does not claim to explain the infinite-cardinal case, which is set aside as a distinct phenomenon. `[established — Ellentuck 1966; Kopperman 1970]` The finite case, where the successor is a new mark, is where the hidden premise operates.

## 4. Multiplication as Branching

Multiplication is standardly defined by recursive addition, but recursion hides a structural fact: multiplication generates a new dimension of distinctions. The product $a \cdot b$ is the count of pairs, which requires pairing — a new level of distinction between the two factors.

Prime factorization makes the branching explicit. Every positive integer is a finite product of prime powers:

$$n = \prod_{p} p^{v_p(n)}.$$

Each prime is a distinct branch type, and the exponent $v_p(n)$ counts the depth of nesting along that branch. The p-adic valuation is therefore a measure of depth along a prime branch, not a measure of size. `[established — Ostrowski 1916; see also 6]` This reading of valuation as depth is the bridge between the calculus of indications (branching distinctions) and number theory (the tree of prime divisors). The structural correspondence is the subject of Section 6.

## 5. The Reconstruction Program: From the Idempotent Mark to the Integers

This section outlines the research program that would turn the critique of Section 3 into a constructive derivation. **The claims in this section are `[my conjecture]` unless stated otherwise. They are not established results and are not presented as evidence; the evidential-weight gate applied in Section 7 blocks them.**

### 5.1 Controlled duplication via the exponential modality

In linear logic, the exponential modality $!$ licenses *controlled* copying of a formula: $!A$ may be used as many times as needed, but only under explicit permission [10, 13]. Categorically, the coKleisli category $\mathcal{B}_{!}$ of the comonad $!$ over the base category $\mathcal{B}$ is cartesian closed when $!$ is a symmetric monoidal comonad with the Seely isomorphisms. `[established — Girard 1987; Bierman; Mellies; see 10, 13]`

The interpretive step is the following. If $\mathcal{B}$ is the idempotent base of marks (Section 2), then the coKleisli category of $!$ is the *non-idempotent shadow* of that base: maps in $\mathcal{B}_{!}$ may duplicate their input, which is exactly the breaking of idempotence under explicit permission. `[my conjecture]` This claim is disconfirmed if the coKleisli category of $!$ over the idempotent base is shown not to admit the duplication structure required for addition — a checkable categorical computation.

### 5.2 The natural numbers object

A natural numbers object (NNO) in a cartesian closed category $\mathcal{B}_{!}$ would provide the additive structure of the natural numbers. The construction under consideration: $0$ is the empty configuration (the void), and the successor $S$ draws a *new* boundary — a fresh mark distinct from all prior marks.

This construction has a direct precedent in constructive work on the calculus of indications, where the natural numbers are built from nested distinctions in a small number of steps (mark to $1$; calling to the naturals; nested enclosure to the rationals) [2]. The reconstruction program builds on that precedent rather than claiming priority over it. `[established — prior published work]`

### 5.3 The integers by group completion

The passage from the natural numbers to the integers is the Grothendieck group completion of the free monoid: pairs $(a,b)$ of naturals are identified when $a + d = b + d$, producing the additive group of integers. The reconstruction program's central conjecture is:

> **Conjecture C1** `[my conjecture]`: the Grothendieck group completion of the natural numbers object in the coKleisli category $\mathcal{B}_{!}$, with the law of crossing as the canonical involution, is the ring of integers $\mathbb{Z}$ with the standard ring structure.

> **Conjecture C2** `[my conjecture]`: the ring axioms (associativity, distributivity, identity) are *derived* — they hold because the coKleisli category is cartesian closed and the group completion is functorial — not assumed as axioms of the framework.

Conjecture C1 is disconfirmed if the group completion of the NNO fails to recover the additive group of the integers, or if the law of crossing is not a canonical involution on the configurations. Conjecture C2 is disconfirmed if the derivation of the ring axioms requires importing them as unanalysed assumptions (circularity), or if the exponential modality $!$ is eliminable — that is, if the same ring structure can be derived from the idempotent base without linear logic.

These disconfirmation conditions are the KIF-60 boundary conditions of the program: until C1 and C2 are proven, the derivation is a research program, and any claim that the integers have been "derived from the mark" is `[RETRODICTION — not evidence]` in the sense that the framework was constructed to produce this match. The evidential weight of the reconstruction is therefore zero until the proof exists; the critique of Section 3, by contrast, does not depend on the reconstruction and stands on its own.

### 5.4 Related mathematical contexts

The reconstruction program does not occur in a vacuum. Idempotent mathematics — the study of semirings in which addition is idempotent, including tropical geometry — is an established field [3, 6, 7, 8]. The program's claim is not that idempotent structures exist (they demonstrably do) but that the *primitive* structure of the mark is idempotent and that non-idempotent arithmetic is its controlled violation. `[my conjecture]` This claim is disconfirmed if a derivation of the integers from the mark is shown to be possible without any idempotence-breaking mechanism. Homotopy type theory offers a competing foundation for constructive mathematics [12]; the relationship between the two programs is a matter for future work.

## 6. Valuation as Depth

If multiplication is branching (Section 4), then the p-adic valuations $v_p(n)$ are nesting depths along prime branches, and the ultrametric structure of the p-adic numbers is the metric shadow of that branching. The Bruhat–Tits tree provides the geometric model: the tree of balls, in which depth along a branch corresponds to divisibility by higher powers of $p$. `[established — Ostrowski 1916; Bruhat–Tits; see 6]`

Ostrowski's theorem classifies the completions of the rationals: exactly one Archimedean completion and one non-Archimedean completion for each prime. In the present vocabulary, the Archimedean place is the unique loop (the re-entrant mark), and the p-adic places are the generic trees (iterated distinctions). The adelic picture, in which all places are treated on equal footing, is the global object of the program. `[my conjecture]` The interpretive claim that the loop is the self-referential closure of the mark is disconfirmed if a non-Archimedean completion is exhibited that is not tree-like in the required sense.

## 7. Discussion and Limits

The epistemic boundary of this paper is stated in full:

1. **The critique (Sections 2–4) is the defensible claim.** The law of calling is established [1]; the observation that $1+1=2$ presupposes two distinguishable marks is a direct, checkable consequence. The critique does not depend on the reconstruction program.
2. **The reconstruction (Section 5) is a research program.** Conjectures C1 and C2 carry explicit disconfirmation conditions. Until they are proven, they carry zero evidential weight as derivations: the framework was built to produce the integers, so producing them is not yet evidence. This is the retrodiction boundary, applied to the framework's own claims.
3. **The framework has degrees of freedom.** Any structure can, in principle, be re-described as "distinctions plus the exponential modality." The specific constraint is that the ring structure of $\mathbb{Z}$ is a fixed target; the program must show that the ring axioms are derived, not imported. The absorption risk — declaring every counterexample a new duality — is managed by fixing the allowed duality maps in advance.
4. **The claims of Section 6 are interpretive re-descriptions of established mathematics** (Ostrowski, Bruhat–Tits, adeles), not new predictions.

The strategic position of the paper is therefore: the critique stands now; the derivation is a program with a clear proof obligation.

## 8. Conclusion

The hidden premise of addition is that the two marks named "$1$" are distinct. Idempotence — the law of calling — makes that premise visible: if they were the same mark, $1+1$ would collapse to $1$. Quantity is not the repetition of the same; it is the creation of new distinctions. The critique is the paper's claim. The reconstruction of the integers from the idempotent mark through the exponential modality of linear logic is the paper's program, labeled conjecture, with falsifiability conditions stated and the retrodiction boundary drawn. The proof of Conjectures C1 and C2 — or their disproof — is the next step.

## Declarations

**Funding.** This research received no specific grant from any funding agency.

**Competing Interests.** The author declares no competing interests.

**Data Availability.** No new data were generated for this work.

**Code Availability.** No code was produced for this work.

**Author Contributions.** The author is the sole contributor.

**Use of Artificial Intelligence.** This manuscript was drafted with the assistance of an AI language model and reviewed by the author; the author takes full responsibility for the content.

**Ethics Statement.** No ethical approval was required for this work.

**Provenance.** This paper is a companion to the treatise *The Calculus of Re-Entrant Distinctions* [2] and was prepared from the research record of that work.

**License.** This work is licensed under the QNFO Unified License Agreement (QNFO-ULA); see the license text accompanying the published version.

## References

1. G. Spencer-Brown, *Laws of Form*. Allen and Unwin, London, 1969.
2. *The Calculus of Re-Entrant Distinctions: A Unified Treatise on the Loop, the Tree, and the Constants of Self-Reference*. DOI: 10.5281/zenodo.21906728.
3. G. L. Litvinov, "Maslov dequantization, idempotent and tropical mathematics: A brief introduction," *Journal of Mathematical Sciences*, vol. 140, no. 3, pp. 426–444, 2007. DOI: 10.1007/s10958-007-0450-5.
4. E. Ellentuck, "Generalized idempotence in cardinal arithmetic," *Fundamenta Mathematicae*, vol. 58, no. 3, pp. 241–258, 1966. DOI: 10.4064/fm-58-3-241-258.
5. R. D. Kopperman, "Idempotence in cardinal arithmetic," *The American Mathematical Monthly*, vol. 77, no. 6, pp. 610–611, 1970. DOI: 10.1080/00029890.1970.11992609.
6. M. Akian, "Densities of idempotent measures and large deviations," *Transactions of the American Mathematical Society*, vol. 351, no. 11, pp. 4515–4543, 1999. DOI: 10.1090/s0002-9947-99-02153-4.
7. G. Mikhalkin, "Enumerative tropical algebraic geometry in $\mathbb{R}^2$," *Journal of the American Mathematical Society*, vol. 18, no. 2, pp. 313–377, 2005. DOI: 10.1090/s0894-0347-05-00477-7.
8. T. J. Green, G. Karvounarakis, and V. Tannen, "Provenance semirings," in *Proceedings of the 26th ACM SIGMOD-SIGACT-SIGART Symposium on Principles of Database Systems*, 2007, pp. 31–40. DOI: 10.1145/1265530.1265535.
9. R. Meyer, "Arithmetic Formulated Relevantly," *Australasian Journal of Logic*, vol. 18, no. 5, pp. 139–157, 2021. DOI: 10.26686/ajl.v18i5.6905.
10. "Classical linear logic, cobordisms and categorical semantics of categorial grammars," arXiv:1810.02047.
11. "Adequate Losses via Quantitative Linear Logic," arXiv:2605.13348.
12. The Univalent Foundations Program, *Homotopy Type Theory: Univalent Foundations of Mathematics*. arXiv:1308.0729.
13. "Logic and linear algebra: an introduction," arXiv:1407.2650.
14. "Arithmetical properties at the level of idempotence," arXiv:1804.08103.
