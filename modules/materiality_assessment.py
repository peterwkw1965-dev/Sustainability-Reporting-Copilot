"""Double materiality assessment support for TPC Group."""

from __future__ import annotations

import pandas as pd

from modules.reporting_agent import MATERIAL_TOPICS, assumptions_block, bullet_list, split_lines, standard_header


def materiality_table(
    topics: list[str] | None = None,
    stakeholder_groups: str = "",
    business_units: str = "",
    regulatory_drivers: str = "",
) -> pd.DataFrame:
    """Create an impact, risk, and opportunity table for selected topics."""

    topics = topics or MATERIAL_TOPICS
    stakeholders = "; ".join(split_lines(stakeholder_groups)) or "Board, employees, customers, regulators, investors, suppliers"
    units = "; ".join(split_lines(business_units)) or "Group operations and shipping activities"
    drivers = "; ".join(split_lines(regulatory_drivers)) or "GRI, ISSB, IMO, EU ETS, FuelEU Maritime"
    rows = []
    for index, topic in enumerate(topics, start=1):
        priority = "High" if index <= 4 else "Medium" if index <= 7 else "Monitor"
        rows.append(
            {
                "Priority Rank": index,
                "Priority Band": priority,
                "Material Topic": topic,
                "Stakeholders": stakeholders,
                "Business Units": units,
                "Impact Lens": "People, environment, operations, or value-chain impact to validate",
                "Financial Lens": "Risk or opportunity for enterprise value, compliance, cost, revenue, or reputation",
                "Regulatory Drivers": drivers,
                "Recommended Disclosure": "Map to GRI, ISSB S1/S2, SASB, TCFD, and assurance evidence",
            }
        )
    return pd.DataFrame(rows)


def generate_materiality_assessment(
    topics: list[str] | None = None,
    stakeholder_groups: str = "",
    business_units: str = "",
    regulatory_drivers: str = "",
    user_notes: str = "",
) -> str:
    """Generate a double materiality narrative and recommended disclosures."""

    topics = topics or MATERIAL_TOPICS
    return f"""{standard_header("Double Materiality Assessment Draft")}
Assessment Approach
TPC Group's assessment should consider impact materiality and financial materiality. Impact materiality covers how TPC Group affects people, the environment, workers, customers, suppliers, communities, and other stakeholders. Financial materiality covers how sustainability matters may affect cash flows, access to capital, cost base, operations, compliance, insurance, and reputation.

Stakeholder Mapping
{bullet_list(split_lines(stakeholder_groups) or ["Board and senior management", "Employees and seafarers", "Customers and commercial partners", "Regulators and port authorities", "Investors, lenders, and insurers", "Suppliers and contractors", "Communities and civil society"])}

Business Units and Boundaries
{bullet_list(split_lines(business_units) or ["Group operations", "Shipping activities", "Corporate functions", "Supply chain interfaces"])}

Regulatory and Reporting Drivers
{bullet_list(split_lines(regulatory_drivers) or ["GRI Standards", "ISSB IFRS S1 and S2", "IMO decarbonization requirements", "EU ETS", "FuelEU Maritime", "Sustainability assurance expectations"])}

Priority Material Topics
{bullet_list(topics)}

Impact, Risk, and Opportunity View
The highest-priority topics should be linked to operational controls, climate and HSSE risk registers, policies, performance metrics, targets, Board oversight, and assurance evidence. Topics with a high financial or regulatory dimension should be connected to ISSB S1/S2 disclosure and transition planning.

Recommended Disclosures
- Map each topic to GRI topic standards and relevant ISSB S1/S2 requirements.
- Identify owners, source data, controls, and approval routes for each metric.
- Explain stakeholder input, scoring method, and management judgement.
- Update the assessment when regulatory drivers, business strategy, or stakeholder expectations change.

User Notes
{user_notes or "No additional management notes provided."}

Assumptions and Management Review
{assumptions_block(["Topic ranking is a starting view and should be validated through stakeholder engagement."])}
"""
