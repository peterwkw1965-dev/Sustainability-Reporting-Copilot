"""Rule-based sustainability report generator for TPC Group."""

from __future__ import annotations

from modules.reporting_agent import assumptions_block, bullet_list, standard_header


def generate_sustainability_report(inputs: dict) -> str:
    """Generate a first-pass sustainability report narrative."""

    topics = inputs.get("material_topics", [])
    return f"""{standard_header("Sustainability Report Draft", inputs["reporting_year"])}
Executive Summary
TPC Group is advancing its sustainability reporting journey from GRI disclosure toward ISSB S1/S2 readiness, assurance preparation, and a net-zero roadmap. This draft summarizes the current reporting position for {inputs.get("business_unit", "Group-wide")} and should be reviewed by qualified sustainability personnel before use.

Sustainability Strategy Section
TPC Group's sustainability strategy should connect HSSE governance, climate transition planning, operational resilience, responsible supply chain practices, regulatory compliance, data quality, and stakeholder expectations.

Stakeholder Engagement Section
Stakeholder engagement should cover employees, seafarers, customers, regulators, investors, suppliers, local communities, banks, insurers, JV partners, and industry associations. The final report should describe engagement methods, priority concerns, and management response.

Material Topics
{bullet_list(topics)}

Key Achievements
{inputs.get("key_achievements", "To be confirmed by management.")}

Key Challenges
{inputs.get("key_challenges", "To be confirmed by management.")}

Performance Highlights
- Scope 1, Scope 2, and Scope 3 emissions have been captured as default sample data.
- Net-zero commitment planning is targeted for 2025.
- Scope 1 and Scope 2 baseline work is planned for 2025.
- Scope 3 baseline expansion is planned for 2026.
- SBTi alignment remains under development.

Disclosure Gaps
- Confirm evidence for emissions, safety, energy, water, waste, and people metrics.
- Confirm reporting boundary, consolidation approach, and data owners.
- Add climate scenario analysis assumptions and financial effects where material.
- Prepare an assurance evidence index before publication.

Assurance Notes
- Retain calculation workbooks and source records.
- Record reviewer and approver sign-offs.
- Clearly distinguish factual data, assumptions, gaps, and recommendations.

Assumptions
{assumptions_block()}
"""

