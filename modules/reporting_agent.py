"""Shared defaults and plain-language helpers for the TPC reporting copilot."""

from __future__ import annotations

from datetime import date


TPC_DEFAULTS = {
    "company": "TPC Group",
    "reporting_year": 2024,
    "scope_1": 701_540.0,
    "scope_2": 38_302.0,
    "scope_3": 6_891.0,
    "revenue": 1_000_000_000.0,
    "prior_scope_1": 720_000.0,
    "prior_scope_2": 40_000.0,
    "prior_scope_3": 7_500.0,
    "energy_use": "Fuel and purchased electricity data to be confirmed through the 2024 reporting workbook.",
    "ohs_performance": "OHS performance narrative to be validated with incident data, hours worked, and contractor safety records.",
    "management_approach": (
        "TPC Group manages sustainability through HSSE governance, operational risk management, "
        "regulatory compliance, data owner review, and progressive assurance readiness."
    ),
    "governance": (
        "Board and senior management oversight is expected to operate through the Group HSSE and "
        "Sustainability governance structure, with management review before publication."
    ),
    "risk_management": (
        "Climate risks and opportunities should be reviewed through enterprise risk management, "
        "regulatory monitoring, operational planning, and investment governance."
    ),
    "climate_risks": (
        "IMO decarbonization requirements; EU ETS exposure; FuelEU Maritime compliance; fuel price "
        "volatility; technology readiness; customer expectations; physical climate disruption."
    ),
    "climate_opportunities": (
        "Voyage optimization, energy efficiency technologies, biofuels, alternative fuels, supplier "
        "engagement, stronger climate disclosure, and improved access to sustainability-linked finance."
    ),
    "roadmap_text": (
        "Scope 1 and Scope 2 baseline planned for 2025; Scope 3 baseline expansion planned for 2026; "
        "net-zero commitment planned for 2025; SBTi alignment under development; shipping "
        "decarbonization strategy includes biofuels, energy efficiency technologies, alternative fuels, "
        "voyage optimization, and operational improvements."
    ),
}


MATERIAL_TOPICS = [
    "Occupational Health and Safety",
    "Climate Change and Decarbonization",
    "Resource Use and Environmental Footprint",
    "Responsible Supply Chain",
    "Data Privacy and Cybersecurity",
    "Transition Assistance",
    "Regulatory Compliance",
    "Employee Well-being",
    "Governance and Stewardship",
]


FRAMEWORKS = [
    "GRI Standards",
    "ISSB IFRS S1",
    "ISSB IFRS S2",
    "SASB",
    "TCFD",
    "UN Global Compact",
    "IMO decarbonization requirements",
    "EU ETS",
    "FuelEU Maritime",
]


def format_tonnes(value: float) -> str:
    """Format emissions values for report text."""

    return f"{value:,.0f} tCO2e"


def total_emissions(scope_1: float, scope_2: float, scope_3: float) -> float:
    """Add Scope 1, Scope 2, and Scope 3 emissions."""

    return scope_1 + scope_2 + scope_3


def percentage(value: float, total: float) -> float:
    """Return a safe percentage even when total is zero."""

    if total == 0:
        return 0.0
    return value / total * 100


def split_lines(text: str) -> list[str]:
    """Turn comma, semicolon, or line-separated text into clean list items."""

    if not text:
        return []
    normalized = text.replace(";", "\n").replace(",", "\n")
    return [item.strip() for item in normalized.splitlines() if item.strip()]


def bullet_list(items: list[str]) -> str:
    """Format a list as report bullets."""

    if not items:
        return "- To be confirmed by management."
    return "\n".join(f"- {item}" for item in items)


def standard_header(title: str, reporting_year: int | None = None) -> str:
    """Create a reusable text output header."""

    year = reporting_year or TPC_DEFAULTS["reporting_year"]
    return (
        f"{title}\n"
        f"TPC Group | Reporting year: {year} | Generated: {date.today().isoformat()}\n"
        f"{'-' * 72}\n"
    )


def assumptions_block(extra_assumptions: list[str] | None = None) -> str:
    """Create the assumptions section used across generated outputs."""

    assumptions = [
        "Generated content is for management review and should not be used as final disclosure without validation.",
        "Reported data is treated as management-provided until source evidence is reviewed.",
        "Recommendations and gap notes are not factual claims unless supported by evidence.",
    ]
    if extra_assumptions:
        assumptions.extend(extra_assumptions)
    return "\n".join(f"- {item}" for item in assumptions)
