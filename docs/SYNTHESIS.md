# Computational synthesis and mechanism path

## What this project does—and does not do

The visible BZ oscillation is a macroscopic nonlinear phenomenon. It is not
scientifically valid to call one Rowan molecular calculation a reconstruction of
the whole reaction. This repository therefore uses a staged synthesis path:
first build the observable kinetics model, then study only a creator-approved
elementary step at molecular resolution.

## Six-stage workflow

| Stage | Question | Output | Gate |
|---|---|---|---|
| 01 | What visible phenomenon is being explained? | `scope.yaml` | Observable and units are explicit |
| 02 | Does the normalized oscillator reproduce the qualitative behavior? | Kinetics figures and metrics | Solver, peaks, sensitivity pass |
| 03 | Which elementary step is actually under review? | Mapped 3-D endpoints | Human/chemist approval and provenance |
| 04 | Can Rowan characterize that step? | UUID, path energies, TS candidate | Explicit credit cap and valid structures |
| 05 | Does the molecular result inform the observed signal? | Comparison table/figure | Period, phase, and residuals reported |
| 06 | What remains unknown? | Creator review | Computed, measured, and unknown claims separated |

## Rowan route

The intended Rowan sequence is:

1. `submit_multistage_optimization_workflow` or a bounded basic optimization
   for each endpoint;
2. `submit_double_ended_ts_search_workflow` with atom-order-matched 3-D
   reactant/product structures;
3. `submit_basic_calculation_workflow` with `optimize_ts` and `frequencies`;
4. `submit_irc_workflow` when the selected step and TS result justify it.

A double-ended search produces a TS guess, not proof. Frequencies and, where
appropriate, an IRC are the acceptance checks. Rowan result provenance and the
workflow UUID must be saved in `rowan_workflows.json`.

## Current status

The Rowan SDK preflight is verified in the Vicena Science Computer:
`rowan-python==3.1.8`, gateway configured, and the relevant workflow callables
exposed. No paid job has been submitted because this repository does not yet
contain an approved molecular target, mapped structures, or a user-authorized
credit budget.
