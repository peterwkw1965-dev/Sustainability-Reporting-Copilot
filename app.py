"""Sustainability Reporting Copilot for TPC Group.

This Streamlit app is rule-based and template-based. It does not call any AI
API, and the internet search page is designed to fail gracefully if network
access is unavailable.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from modules.assurance_readiness import assurance_checklist, generate_assurance_review, readiness_score
from modules.board_paper_writer import action_tracker, generate_board_paper
from modules.climate_transition_plan import action_roadmap, generate_transition_plan
from modules.emissions_calculator import calculate_emissions_summary, metrics_table, scope_split_table
from modules.gri_writer import generate_gri_disclosure, gri_checklist
from modules.internet_search import search_feeds
from modules.issb_s2_writer import assurance_checklist as issb_assurance_checklist
from modules.issb_s2_writer import generate_issb_s2_disclosure, issb_gap_table
from modules.materiality_assessment import generate_materiality_assessment, materiality_table
from modules.reporting_agent import MATERIAL_TOPICS, TPC_DEFAULTS, format_tonnes, total_emissions


st.set_page_config(
    page_title="Sustainability Reporting Copilot for TPC Group",
    page_icon="TPC",
    layout="wide",
)


def download_text(label: str, text: str, file_name: str) -> None:
    """Create a text download button."""

    st.download_button(label, text, file_name=file_name, mime="text/plain")


def download_csv(label: str, table: pd.DataFrame, file_name: str) -> None:
    """Create a CSV download button."""

    st.download_button(label, table.to_csv(index=False), file_name=file_name, mime="text/csv")


def show_generated_text(text: str, file_name: str, height: int = 420) -> None:
    """Show generated text and provide a download."""

    st.text_area("Generated draft", value=text, height=height)
    download_text("Download TXT", text, file_name)


def common_inputs() -> dict:
    """Read common sidebar inputs used across reporting modules."""

    with st.sidebar:
        st.header("TPC Inputs")
        reporting_year = st.number_input("Reporting year", min_value=2020, max_value=2035, value=TPC_DEFAULTS["reporting_year"])
        scope_1 = st.number_input("Scope 1 emissions (tCO2e)", min_value=0.0, value=TPC_DEFAULTS["scope_1"])
        scope_2 = st.number_input("Scope 2 emissions (tCO2e)", min_value=0.0, value=TPC_DEFAULTS["scope_2"])
        scope_3 = st.number_input("Scope 3 emissions (tCO2e)", min_value=0.0, value=TPC_DEFAULTS["scope_3"])
        revenue = st.number_input("Revenue for intensity calculation", min_value=0.0, value=TPC_DEFAULTS["revenue"])

    return {
        "reporting_year": int(reporting_year),
        "scope_1": float(scope_1),
        "scope_2": float(scope_2),
        "scope_3": float(scope_3),
        "revenue": float(revenue),
    }


def page_dashboard(inputs: dict) -> None:
    """Executive dashboard for the TPC reporting journey."""

    total = total_emissions(inputs["scope_1"], inputs["scope_2"], inputs["scope_3"])
    st.title("Sustainability Reporting Copilot for TPC Group")
    st.caption("GRI -> ISSB S1/S2 -> assurance readiness -> net-zero roadmap -> Board reporting -> sustainability intelligence")

    st.write(
        "This app supports the Group HSSE & Sustainability Director in preparing sustainability reports, "
        "ISSB S1/S2 climate disclosures, GRI disclosures, materiality assessments, net-zero roadmap narratives, "
        "Board papers, assurance readiness checks, emissions summaries, and sustainability intelligence."
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Scope 1", format_tonnes(inputs["scope_1"]))
    col2.metric("Scope 2", format_tonnes(inputs["scope_2"]))
    col3.metric("Scope 3", format_tonnes(inputs["scope_3"]))
    col4.metric("Total", format_tonnes(total))

    st.subheader("Available Modules")
    st.write(
        "ISSB S2 Climate Disclosure Generator, GRI Disclosure Generator, Materiality Assessment, "
        "Assurance Readiness Review, Climate Transition Plan, Board Paper Generator, Emissions Summary Calculator, "
        "and Internet Sustainability Search."
    )
    st.warning("Generated content is for management review and should not be used as final disclosure without validation.")


def page_issb(inputs: dict) -> None:
    """ISSB S2 generator page."""

    st.title("ISSB S2 Climate Disclosure Generator")
    with st.form("issb_form"):
        governance = st.text_area("Governance description", TPC_DEFAULTS["governance"], height=100)
        risk_management = st.text_area("Risk management description", TPC_DEFAULTS["risk_management"], height=100)
        risks = st.text_area("Climate risks", TPC_DEFAULTS["climate_risks"], height=100)
        opportunities = st.text_area("Climate opportunities", TPC_DEFAULTS["climate_opportunities"], height=100)
        roadmap = st.text_area("Net-zero roadmap text", TPC_DEFAULTS["roadmap_text"], height=100)
        submitted = st.form_submit_button("Generate disclosure")
    if submitted or True:
        values = {**inputs, "governance": governance, "risk_management": risk_management, "climate_risks": risks, "climate_opportunities": opportunities, "roadmap_text": roadmap}
        text = generate_issb_s2_disclosure(values)
        st.subheader("Gap Analysis")
        st.dataframe(issb_gap_table(), use_container_width=True)
        download_csv("Download Gap CSV", issb_gap_table(), "tpc_issb_s2_gap_analysis.csv")
        st.subheader("Assurance Checklist")
        st.dataframe(issb_assurance_checklist(), use_container_width=True)
        show_generated_text(text, "tpc_issb_s2_climate_disclosure.txt")


def page_gri(inputs: dict) -> None:
    """GRI disclosure page."""

    st.title("GRI Disclosure Generator")
    with st.form("gri_form"):
        energy_use = st.text_area("Energy use", TPC_DEFAULTS["energy_use"], height=90)
        ohs = st.text_area("OHS performance", TPC_DEFAULTS["ohs_performance"], height=90)
        management = st.text_area("Management approach", TPC_DEFAULTS["management_approach"], height=100)
        submitted = st.form_submit_button("Generate GRI disclosure")
    if submitted or True:
        values = {**inputs, "energy_use": energy_use, "ohs_performance": ohs, "management_approach": management}
        st.dataframe(gri_checklist(), use_container_width=True)
        download_csv("Download Checklist CSV", gri_checklist(), "tpc_gri_disclosure_checklist.csv")
        show_generated_text(generate_gri_disclosure(values), "tpc_gri_disclosure_draft.txt")


def page_materiality() -> None:
    """Materiality assessment page."""

    st.title("Materiality Assessment")
    with st.form("materiality_form"):
        selected_topics = st.multiselect("Material topics", MATERIAL_TOPICS, default=MATERIAL_TOPICS)
        stakeholder_groups = st.text_area("Stakeholder groups", "Board and senior management; Employees and seafarers; Customers; Regulators; Investors; Suppliers")
        business_units = st.text_area("Business units", "Group operations; Shipping activities; Corporate functions; Supply chain interfaces")
        regulatory_drivers = st.text_area("Regulatory drivers", "GRI; ISSB S1/S2; IMO; EU ETS; FuelEU Maritime; assurance expectations")
        user_notes = st.text_area("User notes", "Prioritize climate, OHS, regulatory compliance, and governance for the next reporting cycle.")
        submitted = st.form_submit_button("Generate assessment")
    if submitted or True:
        table = materiality_table(selected_topics, stakeholder_groups, business_units, regulatory_drivers)
        st.dataframe(table, use_container_width=True)
        download_csv("Download CSV", table, "tpc_materiality_assessment.csv")
        text = generate_materiality_assessment(selected_topics, stakeholder_groups, business_units, regulatory_drivers, user_notes)
        show_generated_text(text, "tpc_double_materiality_assessment.txt")


def page_assurance() -> None:
    """Assurance readiness page."""

    st.title("Assurance Readiness Review")
    with st.form("assurance_form"):
        disclosure_text = st.text_area("Disclosure text", "TPC Group reports 2024 Scope 1, Scope 2, and Scope 3 emissions and is developing ISSB S2 readiness.", height=100)
        data_sources = st.text_area("Data sources", "Emissions workbook; finance records; operational data; management approvals")
        methodology_notes = st.text_area("Methodology notes", "Boundaries, emissions factors, and calculation methods to be confirmed before assurance.")
        evidence_status = st.selectbox("Evidence status", ["Partial", "Available", "Missing"])
        approval_status = st.selectbox("Approval status", ["Not approved", "In progress", "Approved"])
        controls_status = st.selectbox("Internal controls status", ["Partial", "Complete", "Missing"])
        data_quality_status = st.selectbox("Data quality status", ["Review required", "In progress", "Complete"])
        consistency_status = st.selectbox("Narrative-data consistency", ["Review required", "In progress", "Complete"])
        submitted = st.form_submit_button("Run review")
    if submitted or True:
        score = readiness_score(evidence_status, "Complete" if methodology_notes else "Draft", approval_status, controls_status, data_quality_status, consistency_status)
        st.metric("Assurance readiness score", f"{score}%")
        table = assurance_checklist(evidence_status, "Complete" if methodology_notes else "Draft", approval_status, controls_status, data_quality_status, consistency_status)
        st.dataframe(table, use_container_width=True)
        download_csv("Download CSV", table, "tpc_assurance_readiness_checklist.csv")
        text = generate_assurance_review(disclosure_text, data_sources, methodology_notes, approval_status, evidence_status, controls_status, data_quality_status, consistency_status)
        show_generated_text(text, "tpc_assurance_readiness_review.txt")


def page_transition(inputs: dict) -> None:
    """Climate transition plan page."""

    st.title("Climate Transition Plan")
    with st.form("transition_form"):
        baseline_year = st.number_input("Baseline year", min_value=2020, max_value=2035, value=2025)
        target_year = st.number_input("Net-zero target year", min_value=2030, max_value=2100, value=2050)
        levers = st.text_area("Decarbonization levers", "Biofuels; energy efficiency technologies; alternative fuels; voyage optimization; operational improvements", height=90)
        capex_opex = st.text_area("Capex/Opex considerations", "Project-level capex, fuel cost premiums, operational savings, and regulatory cost avoidance to be quantified.")
        regulatory_drivers = st.text_area("Regulatory drivers", "IMO decarbonization requirements; EU ETS; FuelEU Maritime; ISSB S2")
        submitted = st.form_submit_button("Generate transition plan")
    if submitted or True:
        current = total_emissions(inputs["scope_1"], inputs["scope_2"], inputs["scope_3"])
        values = {**inputs, "baseline_year": int(baseline_year), "target_year": int(target_year), "current_emissions": current, "decarbonization_levers": levers, "capex_opex": capex_opex, "regulatory_drivers": regulatory_drivers}
        table = action_roadmap(levers, regulatory_drivers)
        st.dataframe(table, use_container_width=True)
        download_csv("Download Roadmap CSV", table, "tpc_transition_plan_roadmap.csv")
        show_generated_text(generate_transition_plan(values), "tpc_climate_transition_plan.txt")


def page_board(inputs: dict) -> None:
    """Board paper page."""

    st.title("Board Paper Generator")
    with st.form("board_form"):
        meeting_title = st.text_input("Meeting title", "Board Paper: Sustainability Reporting and Climate Readiness")
        reporting_period = st.text_input("Reporting period", "2024 sustainability reporting cycle")
        key_updates = st.text_area("Key updates", "GRI draft under development; ISSB S2 gap analysis prepared; assurance readiness workstream proposed")
        risks = st.text_area("Risks", TPC_DEFAULTS["climate_risks"])
        decisions = st.text_area("Decisions required", "Approve reporting roadmap; Confirm governance ownership; Endorse assurance readiness milestones")
        recommendations = st.text_area("Management recommendations", "Establish disclosure working group; Prepare evidence index; Develop net-zero roadmap")
        submitted = st.form_submit_button("Generate Board paper")
    if submitted or True:
        values = {**inputs, "meeting_title": meeting_title, "reporting_period": reporting_period, "key_updates": key_updates, "risks": risks, "decisions_required": decisions, "recommendations": recommendations}
        table = action_tracker(decisions, recommendations)
        st.dataframe(table, use_container_width=True)
        download_csv("Download Action Tracker CSV", table, "tpc_board_action_tracker.csv")
        show_generated_text(generate_board_paper(values), "tpc_board_paper_sustainability_reporting.txt")


def page_emissions(inputs: dict) -> None:
    """Emissions calculator page."""

    st.title("Emissions Summary Calculator")
    with st.form("emissions_form"):
        prior_scope_1 = st.number_input("Prior year Scope 1", min_value=0.0, value=TPC_DEFAULTS["prior_scope_1"])
        prior_scope_2 = st.number_input("Prior year Scope 2", min_value=0.0, value=TPC_DEFAULTS["prior_scope_2"])
        prior_scope_3 = st.number_input("Prior year Scope 3", min_value=0.0, value=TPC_DEFAULTS["prior_scope_3"])
        submitted = st.form_submit_button("Calculate emissions summary")
    if submitted or True:
        summary = calculate_emissions_summary(inputs["scope_1"], inputs["scope_2"], inputs["scope_3"], inputs["revenue"], prior_scope_1, prior_scope_2, prior_scope_3)
        col1, col2, col3 = st.columns(3)
        col1.metric("Total emissions", format_tonnes(summary["total"]))
        col2.metric("Emissions intensity", f"{summary['intensity']:.6f}")
        yoy = "N/A" if summary["yoy_percentage_change"] is None else f"{summary['yoy_percentage_change']:.1f}%"
        col3.metric("YoY change", yoy)
        metrics = metrics_table(inputs["scope_1"], inputs["scope_2"], inputs["scope_3"], inputs["revenue"], prior_scope_1, prior_scope_2, prior_scope_3)
        split = scope_split_table(inputs["scope_1"], inputs["scope_2"], inputs["scope_3"])
        st.subheader("Metrics Table")
        st.dataframe(metrics, use_container_width=True)
        download_csv("Download Metrics CSV", metrics, "tpc_emissions_metrics.csv")
        st.subheader("Scope Split")
        st.dataframe(split, use_container_width=True)
        download_csv("Download Scope Split CSV", split, "tpc_emissions_scope_split.csv")


def page_internet_search() -> None:
    """Internet sustainability intelligence page."""

    st.title("Internet Sustainability Search")
    st.info("This page uses public RSS feeds and simple web requests. It will keep the app running if internet access is blocked.")
    with st.form("internet_search_form"):
        query = st.text_input("Search topic", "ISSB S2 latest update")
        max_results = st.slider("Maximum results", min_value=5, max_value=30, value=20)
        submitted = st.form_submit_button("Search")
    if submitted:
        with st.spinner("Searching public sustainability sources..."):
            try:
                results = search_feeds(query, max_results=max_results)
            except Exception:
                results = []
        if not results:
            st.warning("Internet access is unavailable. Please check network permission, firewall, or Streamlit Cloud deployment settings.")
            return
        table = pd.DataFrame(results)
        visible_columns = ["Title", "Source", "Date", "Link", "Short Summary", "Topic Classification", "Relevance to TPC Group", "Suggested Action"]
        st.dataframe(table[visible_columns], use_container_width=True)
        download_csv("Download Search CSV", table[visible_columns], "tpc_sustainability_intelligence_brief.csv")
        for item in results:
            st.subheader(item["Title"])
            st.write(f"Source: {item['Source']}")
            if item.get("Date"):
                st.write(f"Date: {item['Date']}")
            if item.get("Link"):
                st.write(item["Link"])
            st.write(item["Short Summary"])
            st.write(f"Topic classification: {item['Topic Classification']}")
            st.write(f"Relevance to TPC Group: {item['Relevance to TPC Group']}")
            st.write(f"Suggested action: {item['Suggested Action']}")


PAGES = {
    "Dashboard": page_dashboard,
    "ISSB S2 Climate Disclosure Generator": page_issb,
    "GRI Disclosure Generator": page_gri,
    "Materiality Assessment": page_materiality,
    "Assurance Readiness Review": page_assurance,
    "Climate Transition Plan": page_transition,
    "Board Paper Generator": page_board,
    "Emissions Summary Calculator": page_emissions,
    "Internet Sustainability Search": page_internet_search,
}


def main() -> None:
    """Run the selected Streamlit page."""

    inputs = common_inputs()
    page_name = st.sidebar.radio("App pages", list(PAGES.keys()))
    page_function = PAGES[page_name]
    if page_name in {"Materiality Assessment", "Assurance Readiness Review", "Internet Sustainability Search"}:
        page_function()
    else:
        page_function(inputs)


if __name__ == "__main__":
    main()
