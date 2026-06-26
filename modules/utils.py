"""Small shared helpers used by the Streamlit pages.

These helpers keep the app easy to read for non-programmers: pages call clear
functions for downloads and tables instead of repeating the same setup.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_FOLDERS = [
    "prompts",
    "data/emissions",
    "data/policies",
    "data/sustainability_reports",
    "data/climate_strategy",
    "data/reference_documents",
    "outputs/reports",
    "outputs/disclosures",
    "outputs/board_papers",
    "outputs/assurance_reviews",
]


def ensure_project_structure() -> None:
    """Create the expected local folders if they are missing.

    Streamlit Community Cloud starts from a clean checkout, so the app creates
    empty data and output folders at startup instead of assuming they exist.
    """

    base = Path(__file__).resolve().parent.parent
    for folder in PROJECT_FOLDERS:
        (base / folder).mkdir(parents=True, exist_ok=True)


def download_text(label: str, text: str, file_name: str) -> None:
    """Show a download button for a generated text draft."""

    import streamlit as st

    st.download_button(label, text, file_name=file_name, mime="text/plain")


def download_csv(label: str, table: pd.DataFrame, file_name: str) -> None:
    """Show a download button for a CSV table."""

    import streamlit as st

    st.download_button(label, table.to_csv(index=False), file_name=file_name, mime="text/csv")


def show_generated_text(text: str, file_name: str, height: int = 420) -> None:
    """Display generated text and provide a matching TXT download."""

    import streamlit as st

    st.text_area("Generated draft", value=text, height=height)
    download_text("Download TXT", text, file_name)
