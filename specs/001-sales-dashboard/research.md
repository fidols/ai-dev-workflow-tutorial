# Research: ShopSmart Sales Dashboard

**Feature**: 001-sales-dashboard
**Date**: 2026-03-07
**Status**: Complete — all NEEDS CLARIFICATION resolved

---

## Decision 1: Application Structure

**Decision**: Single `app.py` file at the repository root.

**Rationale**: The feature scope is a single-page dashboard with four charts and
two KPI cards. A single file is the simplest structure that satisfies all
requirements and aligns with Principle IV (Simplicity). Streamlit's own
documentation recommends this approach for apps that do not require multi-page
routing or shared component libraries.

**Alternatives considered**:
- `app.py` + `data.py` + `charts.py`: Rejected — introduces module boundaries
  and import complexity for a codebase that will likely remain under 200 lines.
  Premature abstraction per Principle IV.
- Full component structure: Rejected — designed for multi-page apps with shared
  chart types; overkill for four one-off visualizations.

---

## Decision 2: Charting Library

**Decision**: Plotly Express via `plotly` package, rendered through Streamlit's
native `st.plotly_chart()`.

**Rationale**: Plotly is the only library in the shortlist that satisfies FR-004
(interactive tooltips on line chart) and FR-007 (interactive tooltips on bar
charts) without additional configuration. Streamlit has first-class Plotly
support. The PRD's own technical recommendation lists Plotly.

**Alternatives considered**:
- Altair: Meets interactivity requirements; rejected in favor of Plotly because
  Plotly Express has a more intuitive API for stakeholder-style bar and line
  charts and wider familiarity in business analytics contexts.
- Matplotlib/Seaborn: Produces static images — no hover interactivity. Would
  violate FR-004 and FR-007. Rejected.

---

## Decision 3: Data Loading Strategy

**Decision**: Read `data/sales-data.csv` fresh on every Streamlit run using
`pandas.read_csv()`. No caching layer.

**Rationale**: The dataset is ~1,000 rows. A fresh pandas read of a 1,000-row
CSV takes under 50ms on any modern system — well within the 5-second load gate
(SC-001). Adding `st.cache_data` would introduce state management complexity
(cache invalidation, stale data risk) that violates Principle IV and Principle I
(Data Fidelity — cached data could mask updates to the CSV). The simplest
approach is also the safest here.

**Alternatives considered**:
- `st.cache_data`: Faster repeat interactions within a session; rejected because
  it risks serving stale data after CSV updates, conflicting with Principle I.
- Pre-process to Parquet: Significant added complexity (build step, two file
  formats, conversion logic); unnecessary for this data volume. Rejected.

---

## Decision 4: Dependency Management

**Decision**: `uv` for all dependency management, with `pyproject.toml` and
committed `uv.lock`. A `requirements.txt` generated from the lockfile is
included for Streamlit Cloud compatibility.

**Rationale**: Mandated by Principle III (Reproducible Environment). `uv sync`
from a clean checkout must produce an identical environment every time. Streamlit
Cloud currently reads `requirements.txt` for dependency installation, so a
generated `requirements.txt` is needed as a compatibility shim — but `uv.lock`
remains the source of truth.

**Alternatives considered**:
- `pip` + `requirements.txt` only: No lockfile guarantees; indirect dependencies
  can drift. Violates Principle III. Rejected.
- Poetry: Valid alternative; rejected because the constitution explicitly names
  `uv` as the mandated tool.

---

## Decision 5: Column Mapping and Aggregation Logic

**Decision**: Use the following canonical column mappings for all calculations:

| Metric | Source Column | Aggregation |
|--------|--------------|-------------|
| Total Sales | `total_amount` | `sum()` |
| Total Orders | `order_id` | `count()` |
| Sales by Date | `date` + `total_amount` | `groupby('date').sum()` |
| Sales by Category | `category` + `total_amount` | `groupby('category').sum()` |
| Sales by Region | `region` + `total_amount` | `groupby('region').sum()` |

**Rationale**: `total_amount` is explicitly designated as the authoritative sales
column in the spec's Assumptions section. Using `quantity * unit_price` would
introduce a derived calculation that could diverge from `total_amount` if data
has adjustments, discounts, or rounding. Using the stored value directly
satisfies Principle I (Data Fidelity).

**Alternatives considered**:
- `quantity * unit_price`: Derived; could differ from stored `total_amount`.
  Rejected per Principle I.
- `count()` on rows (instead of `order_id`): Equivalent for this dataset but
  less semantically clear. Using `order_id` count makes intent explicit.
