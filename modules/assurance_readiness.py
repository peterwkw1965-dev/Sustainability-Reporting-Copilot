"""Assurance readiness checks for sustainability reporting."""

from __future__ import annotations

import pandas as pd

from modules.reporting_agent import assumptions_block, standard_header


AREAS = [
    "Missing evidence",
    "Missing methodology",
    "Missing approvals",
    "Missing internal controls",
    "Data quality issues",
    "Narrative-data consistency",
    "Assurance preparation checklist",
]


def _status_score(status: str) -> int:
    """Convert a simple status into points for a transparent readiness score."""

    status = (status or "").lower()
    if "complete" in status or "available" in status or "approved" in status:
        return 2
    if "partial" in status or "draft" in status or "in progress" in status:
        return 1
    return 0


def assurance_checklist(
    evidence_status: str = "Partial",
    methodology_status: str = "Draft",
    approval_status: str = "Not approved",
    controls_status: str = "Partial",
    data_quality_status: str = "Review required",
    consistency_status: str = "Review required",
) -> pd.DataFrame:
    """Return assurance readiness checks as a table."""

    rows = [
        ("Missing evidence", evidence_status, "Collect source files, invoices, meter readings, calculation workbooks, and approvals."),
        ("Missing methodology", methodology_status, "Document boundaries, factors, consolidation approach, and estimation methods."),
        ("Missing approvals", approval_status, "Confirm management sign-off by data owners and disclosure owners."),
        ("Missing internal controls", controls_status, "Define reviewer checks, version control, segregation of duties, and change logs."),
        ("Data quality issues", data_quality_status, "Score completeness, accuracy, timeliness, and traceability by metric."),
        ("Narrative-data consistency", consistency_status, "Cross-check claims against metric tables, targets, and supporting evidence."),
        ("Assurance preparation checklist", "Open", "Prepare an evidence index, control matrix, and open-items log."),
    ]
    return pd.DataFrame(
        [{"Review Area": area, "Status": status, "Recommended Action": action} for area, status, action in rows]
    )


def readiness_score(
    evidence_status: str,
    methodology_status: str,
    approval_status: str,
    controls_status: str,
    data_quality_status: str,
    consistency_status: str,
) -> int:
    """Calculate a simple percentage readiness score."""

    statuses = [
        evidence_status,
        methodology_status,
        approval_status,
        controls_status,
        data_quality_status,
        consistency_status,
    ]
    points = sum(_status_score(status) for status in statuses)
    return round(points / (len(statuses) * 2) * 100)


def generate_assurance_review(
    disclosure_text: str = "",
    data_sources: str = "",
    methodology_notes: str = "",
    approval_status: str = "Not approved",
    evidence_status: str = "Partial",
    controls_status: str = "Partial",
    data_quality_status: str = "Review required",
    consistency_status: str = "Review required",
) -> str:
    """Generate an assurance readiness review with gaps and actions."""

    score = readiness_score(
        evidence_status,
        "Complete" if methodology_notes.strip() else "Draft",
        approval_status,
        controls_status,
        data_quality_status,
        consistency_status,
    )
    return f"""{standard_header("Assurance Readiness Review")}
Overall Readiness Score
{score}% based on evidence, methodology, approvals, internal controls, data quality, and narrative-data consistency.

Disclosure Text Reviewed
{disclosure_text or "No disclosure text supplied. Use this section to paste the draft disclosure for review."}

Data Sources
{data_sources or "Data sources not provided. Add source files, systems, owners, and dates."}

Methodology Notes
{methodology_notes or "Methodology notes not provided. Document boundaries, calculation methods, factors, estimates, and limitations."}

Gap List
- Evidence status: {evidence_status}
- Methodology status: {"Complete" if methodology_notes.strip() else "Draft or missing"}
- Approval status: {approval_status}
- Internal controls status: {controls_status}
- Data quality status: {data_quality_status}
- Narrative-data consistency status: {consistency_status}

Required Evidence Checklist
- Source data files and calculation workbooks.
- Emissions factors and methodology references.
- Data owner review and management approval records.
- Control matrix, version history, and change log.
- Reconciliation between disclosure narrative and metrics.

Management Action List
- Assign accountable owners for all open gaps.
- Close high-risk data gaps before external assurance or publication.
- Retain source evidence in a controlled evidence index.
- Mark assumptions, estimates, and uncertainties clearly.

Assumptions and Management Review
{assumptions_block(["This tool does not provide an assurance opinion."])}
"""
