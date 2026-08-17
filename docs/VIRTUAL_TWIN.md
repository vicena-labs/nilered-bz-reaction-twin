# Virtual Twin v0.2

## What this is

The virtual twin is a self-contained browser demo generated from the normalized
Oregonator reaction–diffusion model. It presents:

- the NileRed source video as an external context panel;
- an animated vessel cross-section whose color encodes the model's normalized
  abstract `x` state across one spatial dimension;
- a model signal plot with a moving timeline marker;
- play, pause, reset, speed, and timeline controls;
- model metrics and an explicit calibration-status banner.

The rendered colors are **not** measured concentrations, calibrated pixels, or
identified chemical species. This is a visualized computational layer.

## Run it

From the repository root:

```text
nilered-twin --output-dir outputs
python -m http.server 8000 --directory outputs
```

Open `http://localhost:8000/virtual_twin.html` in a browser. The generated
`virtual_twin_data.json` is the inspectable data source for the animation.

The notebook in `notebooks/` regenerates the same bundle and embeds the demo
for review. The HTML is intentionally dependency-light: the animation uses
browser Canvas and the data are embedded in the generated page.

## Read the display

- **Source video:** external reference only; it is not copied into this repo.
- **Virtual vessel:** model field rendered as a color gradient across 1-D
  position. It is not a photograph or a 3-D CFD reconstruction.
- **Signal plot:** normalized model `x` signal. The marker follows virtual time,
  not video time.
- **Metrics:** numerical outputs from the local solver; they are not laboratory
  measurements.

## What would make it a calibrated twin

1. An authorized video trace with timestamps and a documented color/intensity
   extraction method.
2. Verified experimental source conditions and vessel geometry.
3. A mapping from physical time, space, and optical signal to model variables.
4. Holdout comparison showing timing and waveform error.
5. A separately approved molecular elementary step before any Rowan work.

Until those gates pass, the correct claim is: **interactive visual surrogate of
the computational model, not an exact reconstruction of the laboratory event**.
