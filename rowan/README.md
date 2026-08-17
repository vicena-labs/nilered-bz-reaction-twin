# Rowan integration

This folder is the controlled handoff from the abstract kinetics model to
managed molecular modeling.

## Verified route

- SDK: `rowan-python==3.1.8`
- Gateway: Vicena Rowan gateway configured in the active environment
- Relevant callables verified: descriptors, basic calculation, double-ended TS
  search
- Policy cap observed during preflight: 500 Vicena credits
- Submission status: **not submitted**

## Required before submission

1. A specific elementary transformation, not the entire BZ network.
2. 3-D reactant and product structures with matching atom order.
3. Charge, multiplicity, geometry provenance, and solvent assumptions.
4. A user-authorized Vicena credit cap and runtime boundary.
5. A stable task key recorded before submission to prevent duplicates.

Use the Vicena Rowan runner template for any future paid submission. Do not put
submission calls in notebooks. This repository intentionally contains no API
keys, no paid submission call, and no guessed molecular structures.
