"""Reproducible output generator for the NileRed BZ-reaction repository."""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path
import matplotlib.pyplot as plt
from .oregonator import OregonatorParameters, SpatialOregonatorParameters, simulate_oregonator, simulate_oregonator_1d
from .synthesis_plan import plan_as_dicts
from .virtual_twin import write_virtual_twin_bundle
VERSION = "0.2.0"
def _write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
def generate(output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True); kinetics = OregonatorParameters(); well_mixed = simulate_oregonator(kinetics); spatial = simulate_oregonator_1d(SpatialOregonatorParameters(kinetics=kinetics)); state = spatial["state"]
    field_rows = [{"time": float(t), "position": float(pos), "x": float(state[0, pi, ti]), "y": float(state[1, pi, ti]), "z": float(state[2, pi, ti])} for ti, t in enumerate(spatial["time"]) for pi, pos in enumerate(spatial["position"])]
    _write_csv(output_dir / "oregonator_spatial.csv", field_rows); (output_dir / "synthesis_plan.json").write_text(json.dumps(plan_as_dicts(), indent=2) + "\n")
    virtual_twin = write_virtual_twin_bundle(output_dir, well_mixed=well_mixed, spatial=spatial)
    plt.rcParams.update({"figure.dpi": 120, "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.alpha": 0.25}); fig, axes = plt.subplots(2, 1, figsize=(11, 7.5), constrained_layout=True)
    axes[0].plot(well_mixed["time"], well_mixed["state"][0], color="#4c72b0"); axes[0].set_xlabel("Dimensionless time"); axes[0].set_ylabel("x"); axes[0].set_title(f"Well-mixed oscillator: period {well_mixed['mean_period']:.3f} ± {well_mixed['period_std']:.3f}")
    heat = axes[1].pcolormesh(spatial["time"], spatial["position"], state[0], shading="auto", cmap="magma"); axes[1].set_xlabel("Dimensionless time"); axes[1].set_ylabel("1-D position"); axes[1].set_title(f"Spatial transient: max field SD {spatial['max_spatial_std']:.3f}"); fig.colorbar(heat, ax=axes[1], label="dimensionless x proxy"); fig.suptitle("NileRed companion: kinetics first, Rowan-gated mechanism second", fontsize=13); fig.savefig(output_dir / "bz_research_twin.png", bbox_inches="tight"); plt.close(fig)
    manifest = {"version": VERSION, "well_mixed": {"peak_count": well_mixed["peak_count"], "mean_period": well_mixed["mean_period"], "period_std": well_mixed["period_std"]}, "spatial": {"solver_success": spatial["solver_success"], "max_spatial_std": spatial["max_spatial_std"], "final_spatial_std": spatial["final_spatial_std"]}, "rowan": {"status": "ready_but_not_submitted", "reason": "explicit structures and budget authorization are required"}, "virtual_twin": virtual_twin}; (output_dir / "release_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n"); print(json.dumps(manifest, indent=2)); return manifest
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--output-dir", type=Path, default=Path("outputs")); args = parser.parse_args(argv); generate(args.output_dir); return 0
if __name__ == "__main__": raise SystemExit(main())
