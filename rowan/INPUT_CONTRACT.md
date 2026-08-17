# Rowan input contract

The minimum valid molecular handoff is:

- `reactant.xyz`: real or optimized 3-D coordinates;
- `product.xyz`: real or optimized 3-D coordinates;
- identical atom ordering across both endpoints;
- a sidecar recording charge, spin/multiplicity, solvent model, provenance,
  intended workflow, and authorized Vicena credit cap.

SMILES-only sketches are not sufficient evidence for a transition-state search.
If only a SMILES is available, use it for local topology review or a bounded
conformer preparation step first, then retain geometry provenance.
