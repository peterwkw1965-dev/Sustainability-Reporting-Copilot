"""Climate transition plan narrative generator."""

from __future__ import annotations

import pandas as pd

from modules.reporting_agent import assumptions_block, bullet_list, format_tonnes, split_lines, standard_header


def action_roadmap(levers: str = "", regulatory_drivers: str = "") -> pd.DataFrame:
    """Create a short, medium, and long-term transition action roadmap."""

    driver_text = "; ".join(split_lines(regulatory_drivers)) or "IMO, EU ETS, FuelEU Maritime, ISSB S2"
    lever_text = "; ".join(split_lines(levers)) or "Efficiency, voyage optimization, biofuels, alternative fuels"
    return pd.DataFrame(
        [
            {
                "Time Horizon": "Short term",
                "Action": "Confirm emissions baseline, methodology, controls, and quick-win efficiency projects.",
                "Levers": lever_text,
                "Dependencies and Risks": "Data quality, ownership, evidence retention, operational feasibility.",
                "Regulatory Drivers": driver_text,
            },
            {
                "Time Horizon": "Medium term",
                "Action": "Expand Scope 3 baseline, set interim targets, and develop investment pipeline.",
                "Levers": lever_text,
                "Dependencies and Risks": "Supplier data, technology readiness, commercial costs, customer demand.",
                "Regulatory Drivers": driver_text,
            },
            {
                "Time Horizon": "Long term",
                "Action": "Scale alternative fuels, technology upgrades, and value-chain partnerships.",
                "Levers": lever_text,
                "Dependencies and Risks": "Fuel availability, infrastructure, capex approval, policy evolution.",
                "Regulatory Drivers": driver_text,
            },
        ]
    )


def generate_transition_plan(inputs: dict) -> str:
    """Generate a TPC-specific net-zero roadmap narrative."""

    current_emissions = inputs.get("current_emissions", 0.0)
    return f"""{standard_header("Climate Transition Plan Draft", inputs.get("reporting_year"))}
Net-Zero Roadmap Narrative
TPC Group's net-zero roadmap should move from emissions baselining to target-setting, implementation planning, capital allocation, and assurance-ready progress reporting. The current planning view uses baseline year {inputs.get("baseline_year")} and target year {inputs.get("target_year")}. Current emissions for transition planning are {format_tonnes(current_emissions)}.

Decarbonization Levers
{bullet_list(split_lines(inputs.get("decarbonization_levers", "")))}

Shipping Decarbonization Pathway
TPC Group's pathway should combine near-term energy efficiency and voyage optimization with progressive assessment of biofuels, alternative fuels, technology upgrades, and operational improvements. The pathway should be tested against IMO decarbonization requirements, EU ETS, FuelEU Maritime, customer expectations, and technical readiness.

MACC Analysis Narrative
A marginal abatement cost curve should compare emissions reduction potential, cost per tCO2e avoided, implementation difficulty, asset readiness, regulatory benefit, and dependencies. The first version can rank initiatives qualitatively until project-level capex, opex, fuel cost, and abatement data are available.

Internal Carbon Pricing Narrative
TPC Group can use internal carbon pricing to test capital decisions, compare abatement projects, and evaluate exposure to carbon-related regulation. The price should be documented, reviewed periodically, and applied consistently in transition plan reviews and Board papers.

Capex and Opex Considerations
{inputs.get("capex_opex", "Capex and opex considerations should be confirmed by finance and operations.")}

Regulatory Drivers
{bullet_list(split_lines(inputs.get("regulatory_drivers", "")))}

Short-, Medium-, and Long-Term Actions
- Short term: confirm baseline, methodology, controls, and quick-win efficiency projects.
- Medium term: expand Scope 3 baseline, set interim targets, and build investment pipeline.
- Long term: scale alternative fuels, technology upgrades, and value-chain partnerships.

Risk and Dependency Notes
- Technology readiness, fuel availability, and infrastructure may affect delivery timing.
- Carbon cost exposure and compliance requirements should be refreshed as regulation evolves.
- Management should approve targets before they are presented as commitments.

Assumptions and Management Review
{assumptions_block(["The transition plan should be updated as baselines, targets, and financial plans mature."])}
"""
