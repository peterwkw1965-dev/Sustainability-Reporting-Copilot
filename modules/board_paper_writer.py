"""Board paper generator for sustainability and climate reporting."""

from __future__ import annotations

import pandas as pd

from modules.reporting_agent import bullet_list, format_tonnes, split_lines, standard_header, total_emissions


def action_tracker(decisions_required: str = "", recommendations: str = "") -> pd.DataFrame:
    """Create a simple Board action tracker."""

    decisions = split_lines(decisions_required) or [
        "Approve sustainability reporting roadmap",
        "Confirm ISSB S1/S2 governance ownership",
        "Endorse assurance readiness milestones",
    ]
    recommendations_list = split_lines(recommendations) or [
        "Establish cross-functional disclosure working group",
        "Prepare emissions evidence index",
        "Develop net-zero roadmap and SBTi alignment assessment",
    ]
    rows = []
    for index, item in enumerate(decisions + recommendations_list, start=1):
        rows.append(
            {
                "Action ID": f"A{index:02d}",
                "Board Action": item,
                "Owner": "Management to assign",
                "Timing": "Next reporting cycle",
                "Status": "Open",
            }
        )
    return pd.DataFrame(rows)


def generate_board_paper(inputs: dict) -> str:
    """Generate a Board-ready sustainability paper draft."""

    total = total_emissions(inputs["scope_1"], inputs["scope_2"], inputs["scope_3"])
    return f"""{standard_header(inputs.get("meeting_title", "Board Paper: Sustainability Reporting and Climate Readiness"), inputs["reporting_year"])}
Reporting Period
{inputs.get("reporting_period", "2024 sustainability reporting cycle")}

Executive Summary
TPC Group is progressing from GRI reporting toward ISSB S1/S2 climate disclosure readiness, assurance preparation, and a structured net-zero roadmap. Management attention is required on data quality, methodology documentation, governance evidence, transition planning, and Board-level oversight.

Key Sustainability Performance Highlights
- Reported Scope 1 emissions: {format_tonnes(inputs["scope_1"])}
- Reported Scope 2 emissions: {format_tonnes(inputs["scope_2"])}
- Reported Scope 3 emissions: {format_tonnes(inputs["scope_3"])}
- Total reported emissions: {format_tonnes(total)}

Key Updates
{bullet_list(split_lines(inputs.get("key_updates", "")))}

Climate and Regulatory Risks
{bullet_list(split_lines(inputs.get("risks", "")))}

Decisions Required
{bullet_list(split_lines(inputs.get("decisions_required", "")))}

Management Recommendations
{bullet_list(split_lines(inputs.get("recommendations", "")))}

Board-Level Action Tracker
Management should track owners, due dates, and closure evidence for all approved actions. Priority actions include governance confirmation, ISSB S2 gap closure, assurance evidence preparation, and transition plan development.

Management Review Note
Generated content is for Board paper drafting support and requires validation by management before circulation.
"""
