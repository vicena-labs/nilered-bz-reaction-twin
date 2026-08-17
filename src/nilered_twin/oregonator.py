"""Normalized Oregonator kinetics for a safe BZ-reaction virtual twin.

The model is intentionally abstract and dimensionless. The 0-D solver is a
well-mixed oscillator. The optional 1-D solver adds diffusion with no-flux
boundary conditions to make wave-like spatial structure inspectable without
turning the project into a laboratory recipe.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np
from scipy.integrate import solve_ivp
from scipy.signal import find_peaks
from scipy.sparse import lil_matrix


@dataclass(frozen=True)
class OregonatorParameters:
    """Dimensionless reduced-kinetics parameters."""

    epsilon: float = 0.01
    q: float = 0.002
    f: float = 1.4

    def __post_init__(self) -> None:
        if min(self.epsilon, self.q, self.f) <= 0:
            raise ValueError("epsilon, q, and f must be positive")


@dataclass(frozen=True)
class SpatialOregonatorParameters:
    """Numerical and diffusion settings for the 1-D extension."""

    kinetics: OregonatorParameters = field(default_factory=OregonatorParameters)
    diffusion_x: float = 1.0
    diffusion_y: float = 0.0
    diffusion_z: float = 0.0
    domain_length: float = 60.0
    n_points: int = 60
    t_end: float = 80.0
    n_samples: int = 401

    def __post_init__(self) -> None:
        if min(self.diffusion_x, self.diffusion_y, self.diffusion_z) < 0:
            raise ValueError("diffusion coefficients must be non-negative")
        if self.domain_length <= 0 or self.n_points < 5:
            raise ValueError("domain_length must be positive and n_points >= 5")
        if self.t_end <= 0 or self.n_samples < 20:
            raise ValueError("t_end must be positive and n_samples >= 20")


def oregonator_rhs(_time: float, state: np.ndarray, params: OregonatorParameters) -> list[float]:
    """Return the dimensionless well-mixed Oregonator derivatives."""
    x, y, z = state
    dx = (params.q * y - x * y + x * (1.0 - x)) / params.epsilon
    dy = (-params.q * y - x * y + params.f * z) / params.epsilon
    dz = x - z
    return [dx, dy, dz]


def estimate_period(
    time: np.ndarray,
    signal: np.ndarray,
    prominence: float = 0.05,
    min_distance: int = 50,
) -> dict[str, Any]:
    """Detect peaks and summarize a sampled oscillatory signal."""
    time = np.asarray(time, dtype=float)
    signal = np.asarray(signal, dtype=float)
    if time.ndim != 1 or signal.ndim != 1 or time.size != signal.size:
        raise ValueError("time and signal must be equally sized one-dimensional arrays")
    if time.size < 3 or min_distance < 1:
        raise ValueError("signal must contain at least three samples")
    peaks, properties = find_peaks(signal, prominence=prominence, distance=min_distance)
    peak_times = time[peaks]
    periods = np.diff(peak_times)
    return {
        "peak_indices": peaks,
        "peak_times": peak_times,
        "peak_prominences": properties.get("prominences", np.array([])),
        "periods": periods,
        "mean_period": float(periods.mean()) if periods.size else float("nan"),
        "period_std": float(periods.std()) if periods.size else float("nan"),
        "peak_count": int(peak_times.size),
    }


def simulate_oregonator(
    params: OregonatorParameters = OregonatorParameters(),
    initial_state: tuple[float, float, float] = (1.0, 1.0, 1.0),
    t_end: float = 200.0,
    transient: float = 50.0,
    n_samples: int = 20_001,
) -> dict[str, Any]:
    """Integrate the reduced model and estimate the x-oscillation period."""
    if t_end <= transient or n_samples < 100:
        raise ValueError("require t_end > transient and n_samples >= 100")
    sol = solve_ivp(
        lambda t, u: oregonator_rhs(t, u, params),
        (0.0, t_end),
        np.asarray(initial_state, dtype=float),
        method="LSODA",
        rtol=1e-8,
        atol=1e-10,
        max_step=0.1,
        dense_output=True,
    )
    if not sol.success:
        raise RuntimeError(sol.message)
    time = np.linspace(0.0, t_end, n_samples)
    state = sol.sol(time)
    transient_mask = time > transient
    period_result = estimate_period(
        time[transient_mask], state[0, transient_mask], prominence=0.05, min_distance=50
    )
    return {
        "time": time,
        "state": state,
        **period_result,
        "solver_success": bool(sol.success),
    }


def _neumann_laplacian(values: np.ndarray, spacing: float) -> np.ndarray:
    """Second derivative with zero normal derivative at both endpoints."""
    laplacian = np.empty_like(values)
    laplacian[1:-1] = values[:-2] - 2.0 * values[1:-1] + values[2:]
    laplacian[0] = 2.0 * (values[1] - values[0])
    laplacian[-1] = 2.0 * (values[-2] - values[-1])
    return laplacian / spacing**2


def spatial_oregonator_rhs(
    _time: float, flat_state: np.ndarray, params: SpatialOregonatorParameters
) -> np.ndarray:
    """Return the 1-D reaction-diffusion Oregonator derivatives."""
    n = params.n_points
    x, y, z = flat_state.reshape(3, n)
    kinetics = params.kinetics
    spacing = params.domain_length / (n - 1)
    reaction = np.asarray(
        [oregonator_rhs(_time, np.asarray([x[i], y[i], z[i]]), kinetics) for i in range(n)]
    )
    derivatives = reaction.T
    derivatives[0] += params.diffusion_x * _neumann_laplacian(x, spacing)
    derivatives[1] += params.diffusion_y * _neumann_laplacian(y, spacing)
    derivatives[2] += params.diffusion_z * _neumann_laplacian(z, spacing)
    return derivatives.ravel()


def _spatial_jacobian_pattern(params: SpatialOregonatorParameters):
    """Sparse pattern for the local reaction and nearest-neighbor diffusion."""
    n = params.n_points
    pattern = lil_matrix((3 * n, 3 * n), dtype=int)
    for i in range(n):
        rows = [i, n + i, 2 * n + i]
        cols = [i, n + i, 2 * n + i]
        for row in rows:
            for col in cols:
                pattern[row, col] = 1
        for offset, coefficient in ((0, params.diffusion_x), (n, params.diffusion_y), (2 * n, params.diffusion_z)):
            if coefficient:
                row = offset + i
                if i > 0:
                    pattern[row, row - 1] = 1
                if i < n - 1:
                    pattern[row, row + 1] = 1
    return pattern.tocsr()


def simulate_oregonator_1d(
    params: SpatialOregonatorParameters = SpatialOregonatorParameters(),
    baseline_state: tuple[float, float, float] = (0.02, 0.80, 0.02),
    pulse_state: tuple[float, float, float] = (0.80, 0.20, 0.02),
    pulse_width: int | None = None,
) -> dict[str, Any]:
    """Integrate a safe 1-D Oregonator reaction-diffusion field.

    The initial localized pulse is a mathematical perturbation, not a
    laboratory instruction. The returned state has shape
    ``(3, n_points, n_samples)`` and uses no-flux boundary conditions.
    """
    n = params.n_points
    if len(baseline_state) != 3 or len(pulse_state) != 3:
        raise ValueError("baseline_state and pulse_state must each contain three values")
    width = pulse_width if pulse_width is not None else max(2, n // 15)
    if width < 1 or width >= n:
        raise ValueError("pulse_width must be between 1 and n_points - 1")
    initial = np.empty((3, n), dtype=float)
    initial[:] = np.asarray(baseline_state, dtype=float)[:, None]
    center = n // 2
    left = max(0, center - width // 2)
    right = min(n, left + width)
    initial[:, left:right] = np.asarray(pulse_state, dtype=float)[:, None]
    time = np.linspace(0.0, params.t_end, params.n_samples)
    sol = solve_ivp(
        lambda t, u: spatial_oregonator_rhs(t, u, params),
        (0.0, params.t_end),
        initial.ravel(),
        method="BDF",
        t_eval=time,
        rtol=1e-6,
        atol=1e-8,
        max_step=0.5,
        jac_sparsity=_spatial_jacobian_pattern(params),
    )
    if not sol.success:
        raise RuntimeError(sol.message)
    state = sol.y.reshape(3, n, params.n_samples)
    spatial_std = state[0].std(axis=0)
    return {
        "time": time,
        "position": np.linspace(0.0, params.domain_length, n),
        "state": state,
        "initial_state": initial,
        "solver_success": bool(sol.success),
        "max_spatial_std": float(spatial_std.max()),
        "final_spatial_std": float(spatial_std[-1]),
    }
