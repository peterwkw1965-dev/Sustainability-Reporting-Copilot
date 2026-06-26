"""Agent 2: Sustainability Reporting & Climate Disclosure Copilot.

This Streamlit app is deliberately rule-based and template-based. It does not
call an external AI API, so it can run on Streamlit Community Cloud with only
the packages listed in requirements.txt.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from modules.assurance_readiness import assurance_checklist, generate_assurance_review, readiness_score
from modules.board_paper_writer import action_tracker, generate_board_paper
from modules.climate_transition_plan import action_roadmap, generate_transition_plan
from modules.emissions_calculator import calculate_emissions_summary, metrics_table, scope_split_table
from modules.gri_writer import generate_gri_disclosure
from modules.issb_s2_writer import assurance_checklist as issb_assurance_checklist
from modules.issb_s2_writer import generate_issb_s1_s2_disclosure, issb_gap_table
from modules.materiality_assessment import generate_materiality_assessment, materiality_table
from modules.reporting_agent import MATERIAL_TOPICS, TPC_DEFAULTS, format_tonnes, percentage, total_emissions
from modules.sustainability_report_generator import generate_sustainability_report
from modules.utils import download_csv, ensure_project_structure, show_generated_text


st.set_page_config(
    page_title="Agent 2: Sustainability Reporting & Climate Disclosure Copilot",
    page_icon="TPC",
    layout="wide",
)


def sidebar_defaults() -> dict:
    """Show the default TPC dataset in the sidebar and return editable values."""

    with st.sidebar:
        st.header("Default TPC Dataset")
        reporting_year = st.number_input("Reporting year", min_value=2020, max_value=2035, value=TPC_DEFAULTS["reporting_year"])
        scope_1 = st.number_input("Scope 1 emissions 2024 (tCO2e)", min_value=0.0, value=TPC_DEFAULTS["scope_1"])
        scope_2 = st.number_input("Scope 2 emissions 2024 (tCO2e)", min_value=0.0, value=TPC_DEFAULTS["scope_2"])
        scope_3 = st.number_input("Scope 3 emissions 2024 (tCO2e)", min_value=0.0, value=TPC_DEFAULTS["scope_3"])
        revenue = st.number_input("Revenue for intensity calculation", min_value=0.0, value=TPC_DEFAULTS["revenue"])
        st.caption("Net-zero commitment planned: 2025")
        st.caption("Scope 1 and 2 baseline: 2025")
        st.caption("Scope 3 baseline expansion: 2026")
        st.caption("SBTi alignment: under development")

    return {
        "reporting_year": int(reporting_year),
        "scope_1": float(scope_1),
        "scope_2": float(scope_2),
        "scope_3": float(scope_3),
        "revenue": float(revenue),
    }


def page_dashboard(inputs: dict) -> None:
    """Dashboard for the TPC reporting journey."""

    total = total_emissions(inputs["scope_1"], inputs["scope_2"], inputs["scope_3"])
    st.title("Agent 2: Sustainability Reporting & Climate Disclosure Copilot")
    st.write(
        "This rule-based copilot supports TPC Group's sustainability reporting, ISSB S1/S2 disclosure "
        "preparation, GRI reporting, materiality assessment, assurance readiness, climate transition "
        "planning, and Board reporting."
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Scope 1", format_tonnes(inputs["scope_1"]))
    col2.metric("Scope 2", format_tonnes(inputs["scope_2"]))
    col3.metric("Scope 3", format_tonnes(inputs["scope_3"]))
    col4.metric("Total emissions", format_tonnes(total))

    st.subheader("Scope Percentage Split")
    st.dataframe(scope_split_table(inputs["scope_1"], inputs["scope_2"], inputs["scope_3"]), use_container_width=True)

    st.subheader("Reporting Workflow")
    st.write("GRI -> ISSB S1/S2 -> Assurance Readiness -> Net-Zero Roadmap")

    st.subheader("Shipping Decarbonization Levers")
    st.write(", ".join(TPC_DEFAULTS["shipping_levers"]))

    st.warning("All generated content must be reviewed by qualified sustainability personnel before use.")


def page_sustainability_report(inputs: dict) -> None:
    """Sustainability report generator page."""

    st.title("Sustainability Report Generator")
    with st.form("sustainability_report_form"):
        reporting_year = st.number_input("Reporting year", min_value=2020, max_value=2035, value=inputs["reporting_year"])
        business_unit = st.text_input("Business unit", "Group-wide")
        selected_topics = st.multiselect("Selected material topics", MATERIAL_TOPICS, default=MATERIAL_TOPICS[:5])
        key_achievements = st.text_area("Key achievements", "Advanced sustainability reporting roadmap; prepared ISSB S1/S2 readiness plan; strengthened HSSE governance.", height=100)
        key_challenges = st.text_area("Key challenges", "Scope 3 data maturity; climate scenario analysis; assurance evidence readiness; evolving maritime regulation.", height=100)
        submitted = st.form_submit_button("Generate sustainability report")
    if submitted:
        values = {
            **inputs,
            "reporting_year": int(reporting_year),
            "business_unit": business_unit,
            "material_topics": selected_topics,
            "key_achievements": key_achievements,
            "key_challenges": key_challenges,
        }
        show_generated_text(generate_sustainability_report(values), "tpc_sustainability_report_draft.txt")


def page_issb(inputs: dict) -> None:
    """ISSB S1/S2 generator page."""

    st.title("ISSB S1/S2 Disclosure Generator")
    with st.form("issb_form"):
        scope_1 = st.number_input("Scope 1 emissions", min_value=0.0, value=inputs["scope_1"])
        scope_2 = st.number_input("Scope 2 emissions", min_value=0.0, value=inputs["scope_2"])
        scope_3 = st.number_input("Scope 3 emissions", min_value=0.0, value=inputs["scope_3"])
        roadmap = st.text_area("Net-zero roadmap text", TPC_DEFAULTS["roadmap_text"], height=100)
        risks = st.text_area("Climate risks", TPC_DEFAULTS["climate_risks"], height=100)
        opportunities = st.text_area("Climate opportunities", TPC_DEFAULTS["climate_opportunities"], height=100)
        governance = st.text_area("Governance description", TPC_DEFAULTS["governance"], height=100)
        submitted = st.form_submit_button("Generate ISSB S1/S2 disclosure")
    if submitted:
        values = {
            **inputs,
            "scope_1": float(scope_1),
            "scope_2": float(scope_2),
            "scope_3": float(scope_3),
            "roadmap_text": roadmap,
            "climate_risks": risks,
            "climate_opportunities": opportunities,
            "governance": governance,
            "risk_management": TPC_DEFAULTS["risk_management"],
        }
        st.subheader("Gap Analysis")
        st.dataframe(issb_gap_table(), use_container_width=True)
        st.subheader("Assurance Notes")
        st.dataframe(issb_assurance_checklist(), use_container_width=True)
        show_generated_text(generate_issb_s1_s2_disclosure(values), "tpc_issb_s1_s2_disclosure.txt")


def page_gri(inputs: dict) -> None:
    """GRI disclosure page."""

    st.title("GRI Disclosure Generator")
    with st.form("gri_form"):
        topic = st.selectbox("Select GRI topic", ["GRI 302 Energy", "GRI 305 Emissions", "GRI 403 OHS"])
        quantitative_data = st.text_area("Quantitative data", "Scope 1: 701,540 tCO2e; Scope 2: 38,302 tCO2e; Scope 3: 6,891 tCO2e.", height=100)
        management_approach = st.text_area("Management approach", TPC_DEFAULTS["management_approach"], height=120)
        submitted = st.form_submit_button("Generate GRI disclosure")
    if submitted:
        values = {**inputs, "gri_topic": topic, "quantitative_data": quantitative_data, "management_approach": management_approach}
        st.subheader("Data Table Summary")
        st.dataframe(pd.DataFrame({"Input Area": ["GRI topic", "Quantitative data"], "Summary": [topic, quantitative_data]}), use_container_width=True)
        show_generated_text(generate_gri_disclosure(values), "tpc_gri_disclosure_draft.txt")


def page_materiality() -> None:
    """Materiality assessment generator page."""

    st.title("Materiality Assessment Generator")
    with st.form("materiality_form"):
        stakeholder_groups = st.text_area("Stakeholder groups", "Board and senior management; Employees and seafarers; Customers; Regulators; Investors; Suppliers", height=90)
        business_impacts = st.text_area("Business impacts", "Climate regulation, safety performance, resource use, supply chain resilience, data security, and employee well-being.", height=90)
        financial_risks = st.text_area("Financial risks/opportunities", "Carbon cost exposure, fuel price volatility, customer expectations, access to sustainability-linked finance, and efficiency savings.", height=90)
        selected_topics = st.multiselect("Selected material topics", MATERIAL_TOPICS, default=MATERIAL_TOPICS)
        submitted = st.form_submit_button("Generate materiality assessment")
    if submitted:
        table = materiality_table(selected_topics, stakeholder_groups, business_impacts, financial_risks)
        st.subheader("Impact, Risk and Opportunity Register")
        st.dataframe(table, use_container_width=True)
        download_csv("Download CSV", table, "tpc_materiality_assessment.csv")
        show_generated_text(generate_materiality_assessment(selected_topics, stakeholder_groups, business_impacts, financial_risks, business_impacts), "tpc_double_materiality_assessment.txt")


def page_assurance() -> None:
    """Assurance readiness checker page."""

    st.title("Assurance Readiness Checker")
    with st.form("assurance_form"):
        disclosure_text = st.text_area("Disclosure text", "TPC Group reports 2024 Scope 1, Scope 2, and Scope 3 emissions.", height=120)
        evidence_list = st.text_area("Evidence list", "Emissions workbook; finance records; operational data; management approvals", height=90)
        methodology = st.text_area("Methodology description", "Boundaries, emissions factors, and calculation methods to be confirmed.", height=90)
        approval_status = st.selectbox("Approval status", ["Not approved", "In progress", "Approved"])
        evidence_status = st.selectbox("Evidence status", ["Partial", "Available", "Missing"])
        controls_status = st.selectbox("Controls status", ["Partial", "Complete", "Missing"])
        data_quality_status = st.selectbox("Data quality status", ["Review required", "In progress", "Complete"])
        consistency_status = st.selectbox("Narrative-data consistency", ["Review required", "In progress", "Complete"])
        submitted = st.form_submit_button("Run assurance check")
    if submitted:
        methodology_status = "Complete" if methodology.strip() else "Draft"
        score = readiness_score(evidence_status, methodology_status, approval_status, controls_status, data_quality_status, consistency_status)
        st.metric("Assurance readiness score", f"{score}%")
        table = assurance_checklist(evidence_status, methodology_status, approval_status, controls_status, data_quality_status, consistency_status)
        st.dataframe(table, use_container_width=True)
        download_csv("Download CSV", table, "tpc_assurance_readiness_checklist.csv")
        show_generated_text(generate_assurance_review(disclosure_text, evidence_list, methodology, approval_status, evidence_status, controls_status, data_quality_status, consistency_status), "tpc_assurance_readiness_review.txt")


def page_transition(inputs: dict) -> None:
    """Climate transition plan generator page."""

    st.title("Climate Transition Plan Generator")
    with st.form("transition_form"):
        baseline_year = st.number_input("Baseline year", min_value=2020, max_value=2035, value=2025)
        target_year = st.number_input("Target year", min_value=2030, max_value=2100, value=2050)
        levers = st.multiselect("Decarbonization levers", TPC_DEFAULTS["shipping_levers"], default=TPC_DEFAULTS["shipping_levers"])
        investment_constraints = st.text_area("Investment constraints", "Project-level capex, fuel cost premiums, operational savings, and regulatory cost avoidance to be quantified.", height=90)
        regulatory_drivers = st.text_area("Regulatory drivers", "IMO decarbonization requirements; EU ETS; FuelEU Maritime; ISSB S2", height=90)
        submitted = st.form_submit_button("Generate transition plan")
    if submitted:
        lever_text = "; ".join(levers)
        values = {
            **inputs,
            "baseline_year": int(baseline_year),
            "target_year": int(target_year),
            "current_emissions": total_emissions(inputs["scope_1"], inputs["scope_2"], inputs["scope_3"]),
            "decarbonization_levers": lever_text,
            "capex_opex": investment_constraints,
            "regulatory_drivers": regulatory_drivers,
        }
        st.subheader("Short-, Medium-, and Long-Term Actions")
        st.dataframe(action_roadmap(lever_text, regulatory_drivers), use_container_width=True)
        show_generated_text(generate_transition_plan(values), "tpc_climate_transition_plan.txt")


def page_board(inputs: dict) -> None:
    """Board paper generator page."""

    st.title("Board Paper Generator")
    with st.form("board_form"):
        meeting_name = st.text_input("Meeting name", "Board Sustainability and Climate Disclosure Update")
        reporting_period = st.text_input("Reporting period", "2024 sustainability reporting cycle")
        key_updates = st.text_area("Key ESG updates", "GRI draft under development; ISSB S1/S2 gap analysis prepared; assurance readiness workstream proposed")
        key_risks = st.text_area("Key risks", TPC_DEFAULTS["climate_risks"])
        decisions = st.text_area("Decisions required", "Approve reporting roadmap; Confirm governance ownership; Endorse assurance readiness milestones")
        submitted = st.form_submit_button("Generate Board paper")
    if submitted:
        recommendations = "Establish disclosure working group; Prepare evidence index; Develop net-zero roadmap"
        values = {**inputs, "meeting_title": meeting_name, "reporting_period": reporting_period, "key_updates": key_updates, "risks": key_risks, "decisions_required": decisions, "recommendations": recommendations}
        tracker = action_tracker(decisions, recommendations)
        st.subheader("Action Tracker Table")
        st.dataframe(tracker, use_container_width=True)
        download_csv("Download CSV", tracker, "tpc_board_action_tracker.csv")
        show_generated_text(generate_board_paper(values), "tpc_board_paper.txt")


def page_emissions(inputs: dict) -> None:
    """Emissions summary calculator page."""

    st.title("Emissions Summary Calculator")
    with st.form("emissions_form"):
        scope_1 = st.number_input("Scope 1", min_value=0.0, value=inputs["scope_1"])
        scope_2 = st.number_input("Scope 2", min_value=0.0, value=inputs["scope_2"])
        scope_3 = st.number_input("Scope 3", min_value=0.0, value=inputs["scope_3"])
        revenue = st.number_input("Revenue", min_value=0.0, value=inputs["revenue"])
        submitted = st.form_submit_button("Calculate emissions summary")
    if submitted:
        summary = calculate_emissions_summary(scope_1, scope_2, scope_3, revenue)
        col1, col2, col3 = st.columns(3)
        col1.metric("Total emissions", format_tonnes(summary["total"]))
        col2.metric("Scope 1 split", f"{percentage(scope_1, summary['total']):.1f}%")
        col3.metric("Emissions intensity", f"{summary['intensity']:.6f}")
        table = metrics_table(scope_1, scope_2, scope_3, revenue, 0.0, 0.0, 0.0)
        st.subheader("Summary Table")
        st.dataframe(table, use_container_width=True)
        st.subheader("Scope Split")
        st.dataframe(scope_split_table(scope_1, scope_2, scope_3), use_container_width=True)
        download_csv("Download CSV", table, "tpc_emissions_summary.csv")


PAGES = {
    "Dashboard": page_dashboard,
    "Sustainability Report Generator": page_sustainability_report,
    "ISSB S1/S2 Disclosure Generator": page_issb,
    "GRI Disclosure Generator": page_gri,
    "Materiality Assessment Generator": page_materiality,
    "Assurance Readiness Checker": page_assurance,
    "Climate Transition Plan Generator": page_transition,
    "Board Paper Generator": page_board,
    "Emissions Summary Calculator": page_emissions,
}


def main() -> None:
    """Run the selected page."""

    ensure_project_structure()
    inputs = sidebar_defaults()
    page_name = st.sidebar.radio("App pages", list(PAGES.keys()))
    page_function = PAGES[page_name]
    if page_name in {"Materiality Assessment Generator", "Assurance Readiness Checker"}:
        page_function()
    else:
        page_function(inputs)


if __name__ == "__main__":
    main()
