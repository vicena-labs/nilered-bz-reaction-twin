# Reproducibility protocol: gated computational synthesis path

Please check this protocol before using it. It may contain mistakes, missing constraints, unsafe assumptions, or source interpretation errors.

## Scope and safety boundary

This is a **computational and evidence-review protocol**, not a wet-lab recipe. It intentionally omits reagent identities, amounts, preparation order, heating, mixing, quenching, and waste instructions. Do not use it to perform a physical experiment. Any laboratory work requires a responsible laboratory officer, primary-source protocol verification, current SDS/compatibility review, institutional approval, containment, waste, and emergency controls.

Here, “synthesis” means synthesizing an evidence-backed computational mechanism package from an observed phenomenon. The BZ oscillation is a macroscopic nonlinear network; one molecular calculation cannot reconstruct or certify the full reaction.

## Evidence inputs

- **S1 — creator reference video:** `https://www.youtube.com/watch?v=LL3kVtc-4vY`
- **S2 — reproducibility/SOP guidance used for the review checklist:** `https://diverdi.colostate.edu/C442/references/SOPs/nature_2021_v597_p293.pdf`

S1 is an observation and communication source, not a substitute for a primary experimental protocol. S2 is checklist guidance, not a chemical safety approval for this project.

## Step-by-step gated workflow

### 0. Freeze the evidence package

1. Record the source URLs above, retrieval date, repository commit, environment, and file hashes.
2. Preserve only authorized, non-sensitive observations. If a video trace is used, keep the raw trace immutable and document every transformation.
3. Maintain a claim ledger separating: source-backed claims, local model results, Rowan results, measurements, and unknowns.

**Gate:** provenance and permissions are recorded; no private laboratory details are copied into the repository.

### 1. Define the observable

1. State the question in measurable terms: for example, whether a normalized oscillator reproduces periodic state transitions and how a spatial extension changes them.
2. Define the observable, units, sampling interval, time window, and acceptance metrics before fitting or comparing data.
3. Treat video color/intensity as qualitative until exposure, white balance, gamma, camera response, lighting, and occlusion artifacts have been assessed.

**Gate:** observable and units are explicit, and the data-processing plan is frozen before comparison.

### 2. Reproduce the local kinetics baseline

From the repository root, use an isolated environment and run:

```text
python -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[test]'
pytest -q
nilered-twin --output-dir outputs
```

The baseline uses normalized, dimensionless Oregonator variables. It is a qualitative dynamical model, not a calibrated concentration/temperature model and not a physical validation of the experiment.

Record:

- Python version and package metadata;
- solver names, tolerances, parameters, units, and initial conditions;
- peak count, period summary, spatial spread, and solver success;
- output filenames and SHA-256 hashes.

**Gate:** tests pass; the CLI regenerates the expected manifest and figures; printed metrics are retained.

### 3. Build the observation bridge

1. Obtain authorization before using a creator video or any laboratory recording as data.
2. Calibrate the measurement chain or state that the comparison is qualitative.
3. Lock or record acquisition settings where possible; document nonlinear camera processing and lighting changes.
4. Pre-register filtering, normalization, alignment, missing-data handling, and uncertainty summaries.
5. Report raw and processed traces together. Do not turn a visually similar trace into a mechanistic claim.

**Gate:** camera/data artifacts are either corrected, bounded, or explicitly reported as unresolved.

### 4. Pass the molecular structure gate

1. Do not infer a molecular elementary step or reagent identity from the video alone.
2. Obtain a provenance-backed primary source and have a qualified chemist select the single elementary transformation under review.
3. Supply atom-order-matched, creator/chemist-approved 3-D reactant and product structures.
4. Record geometry provenance, charge, spin, connectivity, conformer policy, solvent model, and intended method.

**Gate:** the step is chemically scoped, structures are valid and atom-mapped, and the responsible reviewer approves the input contract.

### 5. Run the Rowan route only after authorization

The planned sequence is endpoint optimization, a bounded double-ended transition-state search, transition-state optimization/frequencies, and an IRC/connectivity check when justified. A transition-state search is a candidate generator, not proof.

Before any remote submission, record the workflow type, exact inputs, method/basis/solvent choices, estimated credits, maximum credit cap, and explicit authorization. Save the UUID, status, logs, result files, and hashes. No Rowan job is part of the current release because approved structures and an authorized budget are not present.

**Gate:** the selected structure, method, budget, and acceptance checks are reviewed before submission; frequencies and connectivity evidence support any transition-state claim.

### 6. Release and audit the package

Release only when the evidence register contains:

- source URLs and permissions;
- reproducible commands and environment metadata;
- test and notebook transcripts;
- generated figures and tabular outputs with hashes;
- model limitations and uncertainty;
- Rowan provenance, if a job was authorized and completed;
- a claim ledger showing what is computed, measured, source-backed, or unknown;
- responsible-reviewer sign-off for any physical-use decision.

**Gate:** this computational package may be shared for review only while `lab_use` remains `blocked`.

## Acceptance criteria

| Layer | Passing evidence | Current status |
|---|---|---|
| Local code | Tests pass and CLI outputs regenerate | Passed in the current release; rerun in CI/reviewer environment |
| Kinetics | Solver success, peak detection, period summary, and spatial metrics are printed | Passed for the normalized baseline; not an experimental fit |
| Visualization | Kinetics figure and six-stage pipeline figure render from the notebook | Passed; visual inspection still belongs to the reviewer |
| Video bridge | Acquisition artifacts assessed and preprocessing frozen | **Blocked** |
| Molecular mechanism | Approved mapped structures, justified method, frequencies/connectivity checks | **Blocked** |
| Rowan | Authorized job with saved UUID, results, and credit record | Preflight only; **not submitted** |
| Laboratory protocol | Primary experimental source, SDS/EHS/compatibility/waste review, responsible approval | **Blocked; intentionally not supplied** |

## Required revisions before any lab use

1. Resolve camera intensity artifacts, including auto-exposure, white balance, nonlinear gamma, lighting drift, and occlusion.
2. Identify and justify the Rowan level of theory only after the actual elementary step and structures are reviewed.
3. Obtain and verify the primary experimental protocol and all institutional safety approvals; the current repository does not contain enough evidence to authorize a laboratory procedure.

## Audit status

This is an **internal pre-audit package**, not a formal audit certificate. It records reproducibility checks and blocking conditions; it does not certify laboratory safety, experimental correctness, or mechanism completeness. The machine-readable status is in `protocol/validation_manifest.json`.
