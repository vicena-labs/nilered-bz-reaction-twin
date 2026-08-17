# Pre-audit report: NileRed BZ reaction twin

Please check this protocol before using it. It may contain mistakes, missing constraints, unsafe assumptions, or source interpretation errors.

## Decision

**Status: REVISION REQUIRED / NOT CERTIFIED FOR LAB USE**

The computational baseline is reproducible at the repository level, but the experimental and molecular-mechanism gates are not complete. This report is an internal pre-audit record, not a formal audit certificate.

## Audit boundary

Audited here:

- repository structure and separation of kinetics from molecular modeling;
- deterministic local model execution and printed metrics;
- generated visualizations and machine-readable outputs;
- Rowan SDK preflight and duplicate-safe non-submission state;
- documentation of evidence, assumptions, limitations, and blockers.

Not audited or certified here:

- the physical BZ experiment;
- reagent identity, concentration, handling, compatibility, or waste;
- camera calibration or quantitative video inference;
- the full chemical mechanism;
- any Rowan molecular result, because no job was submitted;
- institutional EHS approval or a responsible laboratory sign-off.

## Evidence register

| ID | Evidence | What it supports | Limitation |
|---|---|---|---|
| S1 | `https://www.youtube.com/watch?v=LL3kVtc-4vY` | Creator-facing observation/context | Not a primary experimental protocol |
| S2 | `https://diverdi.colostate.edu/C442/references/SOPs/nature_2021_v597_p293.pdf` | Reproducibility/SOP checklist context | Not project-specific safety approval |
| C1 | `pytest -q` and the repository test suite | Local implementation checks | Does not validate chemistry |
| C2 | Review notebook outputs | Recomputed kinetics metrics and figures | Uses a normalized model, not measured data |
| C3 | `outputs/release_manifest.json` and `protocol/validation_manifest.json` | Artifact/provenance status | Must be regenerated after substantive changes |
| R1 | Rowan SDK preflight | Exposed workflow routes and configured gateway | No structures, budget authorization, or job result |

## Findings

### F-001 — local computational baseline: pass with scope limitation

The normalized 0-D and 1-D Oregonator layers run, report solver success and numerical summaries, and produce the kinetics/spatial visualization. This supports software reproducibility for the stated model, not a claim that the physical reaction has been reproduced.

### F-002 — pipeline visualization: pass

The six-stage diagram makes the evidence gates visible: scope, kinetics, structure, Rowan, observation bridge, and review. It is a communication artifact and not a laboratory workflow.

### F-003a — interactive virtual twin: pass with calibration limitation

The repository now generates a self-contained HTML demo with a virtual vessel cross-section, 121 model frames, a moving model-signal marker, controls, and an external source-video link. Static HTML/data checks pass and the notebook regenerates the bundle. The browser-side rendering is a visual communication layer; it is not calibrated to the source video and was not treated as a chemical validation.

### F-003 — video-to-signal bridge: blocked

The current evidence does not establish that video intensity is linear, calibrated, or free of automatic camera processing. Quantitative fitting must not be treated as validated until these artifacts are measured or bounded.

### F-004 — molecular mechanism: blocked

No approved elementary step, atom-order-matched 3-D endpoints, method/basis/solvent rationale, frequencies, or connectivity checks are recorded. A Rowan TS search cannot be used as a substitute for these controls.

### F-005 — laboratory protocol: blocked by design

The repository intentionally does not publish an operational wet-lab recipe. A responsible laboratory must obtain the primary source, current SDS/compatibility information, waste plan, containment requirements, and institutional approval before any physical work.

## Corrective-action register

| Finding | Required action | Exit evidence |
|---|---|---|
| F-003 | Resolve or bound camera/data artifacts | Calibration note, raw/processed trace pair, frozen preprocessing record |
| F-004 | Select and review one elementary step | Approved mapped structures plus method/solvent/charge/spin rationale |
| F-004 | If authorized, run Rowan and verify the candidate | UUID, result files, frequencies, connectivity/IRC evidence, credit record |
| F-005 | Verify the primary experimental protocol and institutional controls | Source-backed protocol and responsible-officer sign-off |

## Reproducibility conclusion

The current package is suitable for code review, educational discussion, and creator-facing review of the computational architecture. It is not sufficient evidence for physical execution or for claiming that a molecular mechanism has been validated.
