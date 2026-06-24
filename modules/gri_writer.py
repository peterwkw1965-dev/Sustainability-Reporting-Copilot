"""Rule-based GRI disclosure generator for TPC Group."""

from __future__ import annotations

import pandas as pd

from modules.reporting_agent import assumptions_block, format_tonnes, standard_header


def gri_checklist() -> pd.DataFrame:
    """Return a practical GRI disclosure checklist."""

    return pd.DataFrame(
        [
            {"GRI Area": "GRI 305 Emissions", "Required Input": "Scopes, boundaries, factors, base year, restatements", "Status": "Draft"},
            {"GRI Area": "GRI 302 Energy", "Required Input": "Fuel, electricity, energy intensity, reductions", "Status": "Data gap"},
            {"GRI Area": "GRI 403 OHS", "Required Input": "OHS system, hazards, incidents, hours worked, contractor coverage", "Status": "Draft"},
            {"GRI Area": "Management Approach", "Required Input": "Policies, responsibilities, controls, evaluation", "Status": "Management review"},
            {"GRI Area": "Assurance", "Required Input": "Evidence index and approvals", "Status": "Preparation needed"},
        ]
    )


def generate_gri_disclosure(inputs: dict) -> str:
    """Generate GRI 305, GRI 302, GRI 403, and management approach text."""

    return f"""{standard_header("GRI Disclosure Draft", inputs["reporting_year"])}
Management Approach
{inputs.get("management_approach", "")}

TPC Group should describe responsibilities, policies, objectives, controls, stakeholder engagement, grievance or escalation routes, and how effectiveness is evaluated. The disclosure should separate confirmed facts from planned improvements and management recommendations.

GRI 305: Emissions
For {inputs["reporting_year"]}, TPC Group reports:
- Scope 1 emissions: {format_tonnes(inputs["scope_1"])}
- Scope 2 emissions: {format_tonnes(inputs["scope_2"])}
- Scope 3 emissions: {format_tonnes(inputs["scope_3"])}

Disclosure gaps to close include organizational boundary, operational boundary, emissions factors, calculation methodology, base year, restatement approach, market-based or location-based Scope 2 treatment, and Scope 3 category coverage.

GRI 302: Energy
{inputs.get("energy_use", "")}

TPC Group should disclose energy consumption within the organization, energy consumed outside the organization where relevant, energy intensity, reductions achieved, and conversion factors used. Fuel and electricity data should reconcile to emissions calculations.

GRI 403: Occupational Health and Safety
{inputs.get("ohs_performance", "")}

TPC Group should describe the OHS management system, hazard identification, incident investigation, worker consultation, training, contractor safety management, emergency preparedness, and performance metrics such as fatalities, high-consequence injuries, recordable incidents, and hours worked.

Disclosure Gap Notes
- Add energy consumption by source, site, vessel, or operational boundary where available.
- Confirm emissions factors, consolidation approach, exclusions, and uncertainty.
- Add OHS metrics and explain any limitations in contractor or value-chain coverage.
- Retain evidence and approvals for each published disclosure.

Assumptions and Management Review
{assumptions_block()}
"""
