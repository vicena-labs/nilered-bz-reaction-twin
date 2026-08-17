"""Safe, normalized BZ-reaction companion models for NileRed's topic."""
from .oregonator import OregonatorParameters, SpatialOregonatorParameters, estimate_period, simulate_oregonator, simulate_oregonator_1d
from .synthesis_plan import SynthesisStage, default_synthesis_plan
from .virtual_twin import build_virtual_twin_data, write_virtual_twin_bundle
__all__ = ["OregonatorParameters", "SpatialOregonatorParameters", "estimate_period", "simulate_oregonator", "simulate_oregonator_1d", "SynthesisStage", "default_synthesis_plan", "build_virtual_twin_data", "write_virtual_twin_bundle"]
