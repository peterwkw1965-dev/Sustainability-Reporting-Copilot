"""Emissions calculations for the Streamlit copilot."""

from __future__ import annotations

import pandas as pd

from modules.reporting_agent import percentage, total_emissions


def _change(current: float, prior: float) -> tuple[float, float | None]:
    """Return absolute and percentage change."""

    absolute = current - prior
    percent = None if prior == 0 else absolute / prior * 100
    return absolute, percent


def calculate_emissions_summary(
    scope_1: float,
    scope_2: float,
    scope_3: float,
    revenue: float,
    prior_scope_1: float = 0.0,
    prior_scope_2: float = 0.0,
    prior_scope_3: float = 0.0,
) -> dict:
    """Calculate totals, scope split, intensity, and year-on-year movement."""

    total = total_emissions(scope_1, scope_2, scope_3)
    prior_total = total_emissions(prior_scope_1, prior_scope_2, prior_scope_3)
    total_abs, total_pct = _change(total, prior_total)
    return {
        "total": total,
        "prior_total": prior_total,
        "scope_1_pct": percentage(scope_1, total),
        "scope_2_pct": percentage(scope_2, total),
        "scope_3_pct": percentage(scope_3, total),
        "intensity": total / revenue if revenue else 0.0,
        "yoy_absolute_change": total_abs,
        "yoy_percentage_change": total_pct,
    }


def scope_split_table(scope_1: float, scope_2: float, scope_3: float) -> pd.DataFrame:
    """Return scope split values as a table."""

    total = total_emissions(scope_1, scope_2, scope_3)
    return pd.DataFrame(
        [
            {"Scope": "Scope 1", "Emissions tCO2e": scope_1, "Share %": percentage(scope_1, total)},
            {"Scope": "Scope 2", "Emissions tCO2e": scope_2, "Share %": percentage(scope_2, total)},
            {"Scope": "Scope 3", "Emissions tCO2e": scope_3, "Share %": percentage(scope_3, total)},
            {"Scope": "Total", "Emissions tCO2e": total, "Share %": 100.0 if total else 0.0},
        ]
    )


def metrics_table(
    scope_1: float,
    scope_2: float,
    scope_3: float,
    revenue: float,
    prior_scope_1: float,
    prior_scope_2: float,
    prior_scope_3: float,
) -> pd.DataFrame:
    """Return the requested emissions metrics table."""

    current_values = {
        "Scope 1": scope_1,
        "Scope 2": scope_2,
        "Scope 3": scope_3,
        "Total": total_emissions(scope_1, scope_2, scope_3),
    }
    prior_values = {
        "Scope 1": prior_scope_1,
        "Scope 2": prior_scope_2,
        "Scope 3": prior_scope_3,
        "Total": total_emissions(prior_scope_1, prior_scope_2, prior_scope_3),
    }
    total = current_values["Total"]
    rows = []
    for scope, current in current_values.items():
        prior = prior_values[scope]
        absolute, percent = _change(current, prior)
        rows.append(
            {
                "Metric": scope,
                "Current tCO2e": current,
                "Prior Year tCO2e": prior,
                "Scope Split %": percentage(current, total) if scope != "Total" else 100.0 if total else 0.0,
                "YoY Absolute Change tCO2e": absolute,
                "YoY % Change": percent,
                "Emissions Intensity": total / revenue if scope == "Total" and revenue else "",
            }
        )
    return pd.DataFrame(rows)


def emissions_table(scope_1: float, scope_2: float, scope_3: float) -> pd.DataFrame:
    """Backward-compatible wrapper for the scope split table."""

    return scope_split_table(scope_1, scope_2, scope_3)
