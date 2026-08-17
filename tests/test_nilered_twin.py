import numpy as np
from nilered_twin import OregonatorParameters, SpatialOregonatorParameters, default_synthesis_plan, simulate_oregonator, simulate_oregonator_1d
def test_well_mixed_oscillation():
    result = simulate_oregonator(); assert result["solver_success"]; assert result["peak_count"] >= 10; assert np.isfinite(result["mean_period"]); assert result["period_std"] < 0.1
def test_q_changes_period():
    slow = simulate_oregonator(OregonatorParameters(q=0.001)); fast = simulate_oregonator(OregonatorParameters(q=0.003)); assert slow["mean_period"] > fast["mean_period"]
def test_spatial_solver_and_plan():
    result = simulate_oregonator_1d(SpatialOregonatorParameters(n_points=30, t_end=10, n_samples=101)); assert result["solver_success"]; assert result["state"].shape == (3, 30, 101); assert result["max_spatial_std"] > 0.1; plan = default_synthesis_plan(); assert len(plan) == 6; assert plan[3].route == "Rowan"
