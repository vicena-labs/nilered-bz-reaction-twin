"""A safety-bounded computational synthesis/mechanism plan.

This is a research-plan object, not a wet-lab protocol. It describes the
artifacts and acceptance gates needed to connect an abstract BZ model to
creator-approved observations while withholding operational chemistry details.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
@dataclass(frozen=True)
class SynthesisStage:
    stage: str
    objective: str
    input_contract: str
    output_artifact: str
    acceptance_gate: str
    route: str
    safety_boundary: str
def default_synthesis_plan() -> list[SynthesisStage]:
    return [
        SynthesisStage("01_scope", "Define the visible oscillatory phenomenon and the question to test.", "Creator-approved video observation or abstract target; no recipe required.", "scope.yaml", "Question, observable, and units are explicit.", "local", "No operational chemistry details."),
        SynthesisStage("02_kinetics", "Fit or stress-test the dimensionless well-mixed and spatial Oregonator layers.", "Normalized parameters, initial state, and numerical tolerances.", "kinetics_summary.json and figures", "Solver success, peak detection, and parameter sensitivity are reported.", "local", "Abstract state variables only."),
        SynthesisStage("03_structure_gate", "Select a creator- and chemist-approved elementary step for molecular study.", "Mapped 3-D reactant and product structures with provenance.", "reactant.xyz and product.xyz", "Atom ordering matches; charge, spin, geometry source, and scope are recorded.", "human review", "Structures are not inferred from the video and no recipe is generated."),
        SynthesisStage("04_rowan_path", "Characterize the selected elementary step with bounded managed molecular modeling.", "Approved 3-D endpoints, method/settings, and explicit Vicena credit cap.", "Rowan UUID, path energies, TS candidate, and provider provenance.", "Submission is authorized; TS is checked with frequencies and, when appropriate, IRC.", "Rowan", "Rowan models selected elementary steps, not the full BZ oscillatory network."),
        SynthesisStage("05_observation_bridge", "Compare model phase, period, and waveform shape to an anonymized intensity trace.", "CSV with time and intensity proxy; calibration metadata.", "comparison.csv and review figure", "Timebase, preprocessing, and residuals are visible.", "local + Rowan results", "No private lab data or hazardous procedure is required."),
        SynthesisStage("06_creator_review", "Return a concise failure-aware summary for scientific critique.", "All prior artifacts plus limitations.", "creator_review.md", "Claims are separated into measured, computed, and unknown.", "local", "No endorsement is requested or implied."),
    ]
def plan_as_dicts() -> list[dict[str, str]]:
    return [asdict(stage) for stage in default_synthesis_plan()]
