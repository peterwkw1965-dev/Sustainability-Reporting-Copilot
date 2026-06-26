"""Rule-based ISSB IFRS S1 disclosure support."""

from __future__ import annotations

from modules.reporting_agent import assumptions_block


def generate_issb_s1_section(inputs: dict) -> str:
    """Create a general sustainability-related financial disclosure section."""

    return f"""ISSB IFRS S1: General Sustainability-Related Financial Disclosures
TPC Group should disclose material sustainability-related risks and opportunities that could reasonably affect enterprise value, cash flows, access to finance, cost of capital, compliance exposure, operating resilience, or strategic delivery.

Governance
{inputs.get("governance", "")}

Strategy
Management should explain how sustainability risks and opportunities influence business model, value chain, strategy, resource allocation, time horizons, and financial planning.

Risk Management
Sustainability-related risks should be integrated into the enterprise risk process, assigned to accountable owners, and reviewed using consistent risk criteria.

Metrics and Targets
Metrics should be connected to material topics, source evidence, targets, controls, and management approvals.

S1 Gap Notes
- Confirm the sustainability topics that are financially material.
- Add time horizons and current or anticipated financial effects.
- Connect materiality assessment results to Board oversight and risk management.
- Document data controls and approval routes.

Assurance Notes
{assumptions_block(["ISSB S1 sections should be reconciled to financial and risk management records."])}
"""

