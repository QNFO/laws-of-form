# Project Learnings — Primordial Mark

> **Kaizen engine:** Every lesson is a prevented future mistake.
> Newest lessons at top (highest L-number). Re-number when archiving.
> Lessons tagged "Cross-Project: YES" are candidates for promotion to
> `G:\My Drive\projects\_shared\CROSS-PROJECT-LEARNINGS.md`.

## L2: Never use `write` on a pre-existing content file without first reading it

- **Category:** METHODOLOGY
- **Issue:** During S2 (content audit), I wrote the audit to `0.1.5.1.md`, overwriting the original Consilient Synthesis Outline — a key file containing the publication roadmap. I had read the file minutes earlier and still overwrote it because I treated it as a generic output slot rather than recognizing it as pre-existing project content.
- **Solution:** Recovered from git via `git checkout 187da93 -- 0.1.5.1.md`. Wrote audit to new versioned file `0.2.md` instead.
- **Prevention:** Before ANY `write` to a file in the project directory: (a) check if the file already exists via `Test-Path`; (b) if it exists, READ it first and confirm whether overwrite is intentional; (c) for content audits, analysis, or any derivative work, ALWAYS create a new versioned file rather than overwriting source material. The source files are PERMANENT (§0.6.6).
- **Cross-Project:** YES — Same pattern observed in other projects (accidental overwrite of source material). The rule "read before write" and "source files are PERMANENT" should be universal.

## L1: Prior work overlap risk — ultrametric-tree-universality is direct predecessor

- **Category:** METHODOLOGY
- **Issue:** The primordial-mark project (especially 0.1.1.md "Ultrametric Tree Universality and Breakdowns") overlaps significantly with the recently-completed `ultrametric-tree-universality` project (Archive 2026/05), which produced a publication-ready document covering ultrametric tree breakdowns across 8 domains with Spencer-Brown references.
- **Solution:** The primordial-mark project should differentiate by going deeper into the *primitive* — the Mark itself as generative engine — rather than re-surveying domain breakdowns. The unique contribution is the formal primitive definition and the Classification of Finite Simple Groups connection.
- **Prevention:** Always complete full due diligence (§0.8) before starting substantive work. Check Archive for prior projects with overlapping scope.
- **Cross-Project:** YES — Overlap risk applies to any new project. The archive contains 20+ ultrametric-related projects; always check before starting new work.

---

*Generated from LEARNINGS-TEMPLATE.md v1.1. Add new lessons at the top.*
