"""Rule-based ISSB IFRS S2 climate disclosure generator for TPC Group."""

from __future__ import annotations

import pandas as pd

from modules.reporting_agent import assumptions_block, bullet_list, format_tonnes, split_lines, standard_header, total_emissions


def issb_gap_table() -> pd.DataFrame:
    """Return common ISSB S2 disclosure gaps to help management review."""

    return pd.DataFrame(
        [
            {
                "Disclosure Area": "Climate governance",
                "Potential Gap": "Board committee, cadence, escalation route, and management roles need evidence.",
                "Management Action": "Retain Board papers, committee terms, and climate decision records.",
            },
            {
                "Disclosure Area": "Strategy and resilience",
                "Potential Gap": "Financial effects and climate scenario analysis are not yet quantified.",
                "Management Action": "Define time horizons, scenario assumptions, and affected assets or revenue streams.",
            },
            {
                "Disclosure Area": "Risk management",
                "Potential Gap": "Risk owners, controls, and residual ratings may not be consistently documented.",
                "Management Action": "Link climate risks to the enterprise risk register and control owners.",
            },
            {
                "Disclosure Area": "Metrics and targets",
                "Potential Gap": "Scope 3 boundary and target linkage need further maturity.",
                "Management Action": "Document emissions factors, data quality scores, and target methodology.",
            },
            {
                "Disclosure Area": "Assurance readiness",
                "Potential Gap": "Source evidence and approvals may not be assurance-ready.",
                "Management Action": "Create an evidence index and approval log for each disclosed metric.",
            },
        ]
    )


def assurance_checklist() -> pd.DataFrame:
    """Return ISSB S2 assurance preparation checks."""

    return pd.DataFrame(
        [
            {"Check": "Emissions methodology documented", "Status": "Management review required"},
            {"Check": "Source data retained", "Status": "Evidence required"},
            {"Check": "Governance claims supported", "Status": "Board evidence required"},
            {"Check": "Climate risk descriptions tied to risk register", "Status": "Control owner required"},
            {"Check": "Scenario analysis assumptions documented", "Status": "Gap to close"},
            {"Check": "Narrative reconciled to metric table", "Status": "Reviewer sign-off required"},
        ]
    )


def generate_issb_s2_disclosure(inputs: dict) -> str:
    """Generate a report-ready IFRS S2-style climate disclosure draft."""

    total = total_emissions(inputs["scope_1"], inputs["scope_2"], inputs["scope_3"])
    risks = bullet_list(split_lines(inputs.get("climate_risks", "")))
    opportunities = bullet_list(split_lines(inputs.get("climate_opportunities", "")))
    return f"""{standard_header("ISSB IFRS S2 Climate Disclosure Draft", inputs["reporting_year"])}
1. Climate Governance
{inputs.get("governance", "")}

Management review should confirm the Board body responsible for climate oversight, reporting cadence, escalation thresholds, delegated authority, and how climate matters influence strategy, risk management, and capital allocation.

2. Climate Strategy
TPC Group's climate reporting journey is structured as GRI reporting, ISSB S1/S2 readiness, assurance preparation, net-zero roadmap development, Board reporting, and sustainability intelligence. The current roadmap is:
{inputs.get("roadmap_text", "")}

Climate-related risks identified for review:
{risks}

Climate-related opportunities identified for review:
{opportunities}

3. Risk Management
{inputs.get("risk_management", "")}

TPC Group should document risk owners, controls, residual ratings, financial implications, time horizons, and links to IMO decarbonization requirements, EU ETS, FuelEU Maritime, customer requirements, and investor expectations.

4. Metrics and Targets
Reported {inputs["reporting_year"]} emissions are:
- Scope 1: {format_tonnes(inputs["scope_1"])}
- Scope 2: {format_tonnes(inputs["scope_2"])}
- Scope 3: {format_tonnes(inputs["scope_3"])}
- Total reported emissions: {format_tonnes(total)}

Targets and roadmap status should be presented as management-approved commitments only after governance review. Current planning assumptions include Scope 1 and Scope 2 baseline development in 2025, Scope 3 baseline expansion in 2026, a planned net-zero commitment in 2025, and SBTi alignment under development.

5. Disclosure Gap Analysis
- Confirm governance evidence, including Board minutes and terms of reference.
- Quantify current and anticipated financial effects of material climate risks and opportunities.
- Define climate scenario analysis approach, time horizons, and assumptions.
- Expand Scope 3 methodology, boundary decisions, estimation methods, and data quality scoring.
- Link climate targets to transition plan actions, capex or opex implications, and operating plans.

6. Assurance Notes
- Retain source files for emissions calculations and regulatory assumptions.
- Record reviewer and approver sign-offs.
- Reconcile narrative claims to source data.
- Mark estimates, limitations, and uncertainties clearly.
- Do not publish as final disclosure until management and assurance readiness review are complete.

Assumptions and Management Review
{assumptions_block(["No independent assurance conclusion is implied by this draft."])}
"""


def generate_issb_s1_s2_disclosure(inputs: dict) -> str:
    """Generate an integrated ISSB S1/S2 disclosure draft."""

    from modules.issb_s1_writer import generate_issb_s1_section

    return (
        f"{standard_header('ISSB S1/S2 Disclosure Draft', inputs['reporting_year'])}"
        f"{generate_issb_s1_section(inputs)}\n\n"
        f"{generate_issb_s2_disclosure(inputs)}"
    )
