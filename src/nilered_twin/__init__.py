"""Safe, normalized BZ-reaction companion models for NileRed's topic."""
from .oregonator import OregonatorParameters, SpatialOregonatorParameters, estimate_period, simulate_oregonator, simulate_oregonator_1d
from .synthesis_plan import SynthesisStage, default_synthesis_plan
__all__ = ["OregonatorParameters", "SpatialOregonatorParameters", "estimate_period", "simulate_oregonator", "simulate_oregonator_1d", "SynthesisStage", "default_synthesis_plan"]
