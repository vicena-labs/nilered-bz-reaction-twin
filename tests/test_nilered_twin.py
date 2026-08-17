import numpy as np
from nilered_twin import OregonatorParameters, SpatialOregonatorParameters, default_synthesis_plan, simulate_oregonator, simulate_oregonator_1d
def test_well_mixed_oscillation():
    result = simulate_oregonator(); assert result["solver_success"]; assert result["peak_count"] >= 10; assert np.isfinite(result["mean_period"]); assert result["period_std"] < 0.1
def test_q_changes_period():
    slow = simulate_oregonator(OregonatorParameters(q=0.001)); fast = simulate_oregonator(OregonatorParameters(q=0.003)); assert slow["mean_period"] > fast["mean_period"]
def test_spatial_solver_and_plan():
    result = simulate_oregonator_1d(SpatialOregonatorParameters(n_points=30, t_end=10, n_samples=101)); assert result["solver_success"]; assert result["state"].shape == (3, 30, 101); assert result["max_spatial_std"] > 0.1; plan = default_synthesis_plan(); assert len(plan) == 6; assert plan[3].route == "Rowan"

def test_virtual_twin_bundle(tmp_path):
    from nilered_twin.virtual_twin import build_virtual_twin_data, write_virtual_twin_bundle

    well_mixed = simulate_oregonator(t_end=80, transient=20, n_samples=2001)
    spatial = simulate_oregonator_1d(
        SpatialOregonatorParameters(n_points=15, t_end=20, n_samples=41)
    )
    data = build_virtual_twin_data(well_mixed, spatial, n_frames=7)
    assert len(data["times"]) == 7
    assert len(data["field"]) == 7
    assert len(data["field"][0]) == 15
    assert data["calibration_status"] == "not_calibrated_to_source_video"
    result = write_virtual_twin_bundle(
        tmp_path, well_mixed=well_mixed, spatial=spatial, n_frames=7
    )
    assert (tmp_path / result["html"]).exists()
    assert (tmp_path / result["data"]).exists()
    html = (tmp_path / result["html"]).read_text()
    assert "NileRed BZ Virtual Twin" in html
    assert "MODELLED LAYER" in html
