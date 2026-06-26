# Sustainability Reporting Copilot for TPC Group

Agent 2 is a Streamlit prototype for sustainability reporting and climate disclosure preparation. It supports TPC Group's reporting journey:

GRI -> ISSB S1/S2 -> assurance readiness -> net-zero roadmap.

## Purpose

The app supports sustainability reporting, ISSB S1/S2 disclosure preparation, GRI reporting, materiality assessment, assurance readiness, climate transition planning, Board reporting, and emissions summaries.

## Features

- Dashboard with default TPC emissions data and reporting workflow
- Sustainability Report Generator
- ISSB S1/S2 Disclosure Generator
- GRI Disclosure Generator
- Materiality Assessment Generator
- Assurance Readiness Checker
- Climate Transition Plan Generator
- Board Paper Generator
- Emissions Summary Calculator
- TXT and CSV downloads for generated drafts and tables

## Local Setup

```powershell
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

## Streamlit Cloud Deployment

1. Push the repository to GitHub.
2. Open Streamlit Community Cloud.
3. Select this repository.
4. Select `app.py` as the main file.
5. Deploy.

## Prototype Boundaries

- Rule-based and template-based only.
- No external AI API yet.
- No RAG, vector database, ChromaDB, LangChain, or paid service dependency.
- Generated content requires expert review by qualified sustainability personnel.
- The app is not assurance, legal, accounting, financial, investment, or regulatory advice.

## Default Sample Data

- Scope 1 emissions 2024: 701,540 tCO2e
- Scope 2 emissions 2024: 38,302 tCO2e
- Scope 3 emissions 2024: 6,891 tCO2e
- 2024 total emissions: calculated from Scope 1 + Scope 2 + Scope 3
- Net-zero commitment planned: 2025
- Scope 1 and 2 baseline: 2025
- Scope 3 baseline expansion: 2026
- SBTi alignment: under development
- Shipping decarbonization levers: biofuels, voyage optimization, energy efficiency technologies, alternative fuels, fleet modernization, and operational improvements
