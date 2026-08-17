# NileRed BZ Reaction Twin

A clean, standalone research companion for NileRed's
[Recreating one of the weirdest reactions](https://www.youtube.com/watch?v=LL3kVtc-4vY).

This repository has two explicit layers:

1. **Kinetics layer:** a safe, normalized Oregonator model for oscillation,
   period sensitivity, and a one-dimensional spatial transient.
2. **Synthesis/mechanism layer:** a reviewable path from an observed phenomenon
   to creator-approved molecular structures and a Rowan-managed elementary-step
   calculation.

The word **synthesis** here means an evidence-backed computational mechanism
package. It is not a wet-lab recipe. The full oscillatory BZ network is not a
single molecular reaction and Rowan is not used to pretend that it is.

## Two-minute start

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[test]'
pytest -q
nilered-twin --output-dir outputs
```

Start with `docs/CREATOR_REVIEW.md`, `docs/SYNTHESIS.md`, `protocol/README.md`,
`rowan/README.md`, and the review notebook in `notebooks/`.

## Rowan status

Rowan integration is implemented as a gated, auditable path. The repository
records the intended workflow family and input contract, but no paid Rowan job
is submitted by default. A future job needs creator/chemist-approved mapped 3-D
reactant and product structures plus an explicit Vicena credit cap.

## Safety boundary

No reagent identities, quantities, preparation, heating, mixing, or waste
instructions are included. The state variables are dimensionless. An optional
anonymized time/intensity trace can be used for calibration without exposing
private laboratory details.

## License and attribution

Code and documentation are 0BSD. The video, creator name, trademarks, and
scientific papers remain the property of their respective rights holders. This
is an independent, non-endorsed companion.
