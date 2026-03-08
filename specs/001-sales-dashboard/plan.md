# Implementation Plan: ShopSmart Sales Dashboard

**Branch**: `001-sales-dashboard` | **Date**: 2026-03-07 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/001-sales-dashboard/spec.md`

## Summary

Build a single-file Streamlit dashboard (`app.py`) that loads `data/sales-data.csv`
fresh on each run, computes KPIs and chart data using pandas, and renders four
interactive visualizations via Plotly. The app deploys to Streamlit Community
Cloud directly from the repository root with no additional infrastructure.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: streamlit, pandas, plotly, (managed via `uv`)
**Storage**: CSV file — `data/sales-data.csv` (read-only, no database)
**Testing**: Manual verification against expected values from PRD; no automated
test suite in scope for Phase 1
**Target Platform**: Streamlit Community Cloud (Linux, modern web browsers)
**Project Type**: Single-page web application (data dashboard)
**Performance Goals**: Full page load (including all charts) within 5 seconds
on the ~1,000 row sample dataset — hard acceptance gate per SC-001
**Constraints**: Single file (`app.py`); no caching layer; no authentication;
no external data sources beyond the CSV; must run with `uv sync && streamlit run app.py`
**Scale/Scope**: ~1,000 transaction rows; 4 charts; 2 KPI cards; single user
session; no concurrent user requirements for Phase 1

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Check | Status |
|-----------|-------|--------|
| I. Data Fidelity | All KPIs and chart values computed directly from raw CSV via pandas — no sampling, rounding, or approximation. FR-010 enforces this explicitly. | PASS |
| II. Spec-First | `spec.md` was written and approved before this plan was authored. | PASS |
| III. Reproducible Environment | All dependencies declared in `pyproject.toml` and locked via `uv.lock`. Single install command: `uv sync`. | PASS |
| IV. Simplicity | Single `app.py` file. No helper modules, no abstraction layers, no caching. Minimum viable structure for the requirements. | PASS |
| V. Transparency for Technical Users | Plotly charts include interactive tooltips showing exact values on hover. All aggregation logic is visible in the single source file. | PASS |

*Post-Phase 1 re-check*: All principles hold. No new complexity introduced.
No Complexity Tracking entries required.

## Project Structure

### Documentation (this feature)

```text
specs/001-sales-dashboard/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
app.py                   # Single Streamlit application file (all logic here)
data/
└── sales-data.csv       # Source dataset (read-only)
pyproject.toml           # Project metadata and dependency declarations
uv.lock                  # Locked dependency versions (committed)
requirements.txt         # Streamlit Cloud compatibility shim (generated from uv)
```

**Structure Decision**: Single-file layout. `app.py` at the repository root
contains all data loading, aggregation, and rendering logic. This satisfies
Principle IV (Simplicity) and keeps the deployment path to Streamlit Cloud
trivially simple — no build step, no src layout, no package discovery needed.
