# Feature Specification: ShopSmart Sales Dashboard

**Feature Branch**: `001-sales-dashboard`
**Created**: 2026-03-07
**Status**: Draft
**Input**: PRD — E-Commerce Analytics Platform (prd/ecommerce-analytics.md)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - KPI Snapshot at a Glance (Priority: P1)

A finance manager or executive opens the dashboard and immediately sees Total
Sales (formatted as currency) and Total Orders (formatted as a whole number)
prominently displayed. No navigation or interaction is needed — the numbers are
visible on page load. This is the MVP: a single screen that replaces the weekly
manual Excel summary.

**Why this priority**: This is the most-requested capability across all four
named personas (Sarah, David, James, Maria). A dashboard that loads with
accurate headline numbers delivers immediate value and can be demoed or used
in executive meetings independently of all other features.

**Independent Test**: Open the dashboard with `sales-data.csv` loaded. Verify
that Total Sales (~$650,000–$700,000) and Total Orders (482) are displayed
within 5 seconds of page load, without any user interaction.

**Acceptance Scenarios**:

1. **Given** the dashboard is opened with a valid CSV file, **When** the page
   finishes loading, **Then** Total Sales is displayed formatted as "$XXX,XXX"
   and Total Orders is displayed as a whole number, both matching the sum and
   count of the source data exactly.
2. **Given** the source CSV is replaced with a different valid dataset, **When**
   the dashboard reloads, **Then** Total Sales and Total Orders reflect the new
   data exactly — no cached or stale values.
3. **Given** the dashboard loads, **When** a stakeholder reads the Total Sales
   figure, **Then** the value matches the sum of the `total_amount` column in
   the CSV with no rounding or approximation.

---

### User Story 2 - Sales Trend Over Time (Priority: P2)

The CEO and marketing director want to understand whether sales are growing,
declining, or seasonal. They open the dashboard and see a line chart with time
on the x-axis and sales amount on the y-axis, covering all available historical
data. Hovering over any point reveals the exact value for that period.

**Why this priority**: Trend visibility is the second most-cited need (CEO,
Marketing Director) and supports strategic decisions. It is independently useful
even without the category/region breakdowns in P3.

**Independent Test**: Load the dashboard and inspect the line chart. Confirm it
plots one data point per month (or day, depending on granularity), that the
x-axis spans the full date range in the CSV, and that hover tooltips show exact
values matching the source data.

**Acceptance Scenarios**:

1. **Given** the dashboard loads with 12 months of data, **When** the user views
   the trend chart, **Then** the chart displays all months/periods with no gaps
   and no interpolated values.
2. **Given** the user hovers over any data point, **When** the tooltip appears,
   **Then** it shows the exact sales total for that period, matching what can be
   calculated from the raw CSV.
3. **Given** the source data has varying sales volumes across periods, **When**
   the chart renders, **Then** the y-axis scale reflects the actual min/max of
   the data — not a fixed range that distorts trends.

---

### User Story 3 - Category and Regional Breakdown (Priority: P3)

The marketing director needs to allocate budget by product category; the regional
manager needs to spot underperforming territories. Both see bar charts — one for
sales by product category, one for sales by region — sorted highest to lowest,
with exact values accessible via hover tooltips.

**Why this priority**: These are supporting analytics for specific roles. They
add significant value but are not blocking for the executive use case covered by
P1 and P2. Both charts are grouped as a single story because they share the same
chart type, data pattern, and acceptance criteria shape.

**Independent Test**: Verify that two bar charts are present on the dashboard.
Confirm each shows distinct bars for every category (Electronics, Accessories,
Audio, Wearables, Smart Home) and every region (North, South, East, West),
sorted descending by value, with hover tooltips matching CSV calculations.

**Acceptance Scenarios**:

1. **Given** the dashboard loads, **When** the user views the Category chart,
   **Then** all 5 product categories are represented, sorted highest to lowest
   by total sales, with no category omitted.
2. **Given** the dashboard loads, **When** the user views the Region chart,
   **Then** all 4 geographic regions are represented, sorted highest to lowest
   by total sales.
3. **Given** the user hovers over any bar, **When** the tooltip appears,
   **Then** it displays the exact sales total for that category or region,
   matching the sum of `total_amount` for that group in the CSV.
4. **Given** a bar chart is rendered, **When** a stakeholder compares bar
   heights, **Then** the relative proportions accurately reflect the underlying
   data (no truncated y-axis that distorts comparison).

---

### Edge Cases

- **Missing or empty CSV**: The dashboard MUST display a clear, human-readable
  error message (e.g., "Data file not found. Please check the data directory.")
  rather than a blank screen or stack trace.
- **CSV with missing values in `total_amount`**: Rows with null or non-numeric
  `total_amount` MUST be excluded from all calculations; the dashboard MUST note
  how many rows were skipped.
- **Single-month dataset**: The trend chart MUST render meaningfully (a single
  point or short segment) without breaking layout.
- **All sales in one category or region**: Bar charts MUST still render
  correctly with a single bar.
- **Large currency values**: Formatting MUST handle values above $1,000,000
  without truncation (e.g., "$1,234,567" not "$1.2M" unless explicitly chosen).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The dashboard MUST display Total Sales (sum of `total_amount`)
  formatted as USD currency with comma separators on every page load.
- **FR-002**: The dashboard MUST display Total Orders (count of rows) formatted
  as a whole number with comma separators on every page load.
- **FR-003**: The dashboard MUST render a line chart of sales over time using
  the date granularity present in the source data (daily or monthly).
- **FR-004**: The line chart MUST include interactive tooltips showing the exact
  sales value for the selected time period.
- **FR-005**: The dashboard MUST render a bar chart of total sales by product
  category, sorted descending by value, covering all categories in the dataset.
- **FR-006**: The dashboard MUST render a bar chart of total sales by geographic
  region, sorted descending by value, covering all regions in the dataset.
- **FR-007**: All bar charts MUST include interactive tooltips showing the exact
  sales value for the selected bar.
- **FR-008**: The dashboard MUST load its data from `data/sales-data.csv` at
  startup; no manual file selection is required.
- **FR-009**: The dashboard MUST display a clear error message if the CSV file
  is missing or cannot be parsed, rather than crashing or showing a blank screen.
- **FR-010**: All displayed metric values MUST match calculations verifiable
  directly from the raw CSV (no silent rounding, sampling, or approximation).

**Phase 2 seams** *(not in scope, but design should not block these)*:
- Date range filtering widget could be placed above the trend chart without
  restructuring the layout.
- Drill-down to transaction level could be added as a collapsible table below
  each bar chart without reworking the existing charts.
- Export (CSV/PDF) could attach to the KPI section without touching chart code.

### Key Entities

- **Transaction**: A single sales record with date, order ID, product, category,
  region, quantity, unit price, and total amount. The atomic unit of all
  aggregations.
- **KPI**: An aggregated scalar derived from all transactions (e.g., Total Sales,
  Total Orders). Displayed prominently above charts.
- **Time Series**: Transactions grouped by date period (day or month), producing
  the data points for the trend chart.
- **Category Summary**: Transactions grouped by `category`, summing
  `total_amount` per group.
- **Region Summary**: Transactions grouped by `region`, summing `total_amount`
  per group.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The dashboard MUST fully load and display all KPIs, charts, and
  labels within 5 seconds of opening, measured on the provided sample dataset
  (~1,000 rows). This is a hard acceptance gate.
- **SC-002**: All displayed figures (KPIs, chart values, tooltips) MUST exactly
  match values independently calculated from the raw CSV — zero tolerance for
  discrepancy on the sample dataset.
- **SC-003**: A first-time user with no training can identify Total Sales, Total
  Orders, the sales trend, the top-performing category, and the top-performing
  region within 60 seconds of the dashboard loading.
- **SC-004**: The dashboard runs without errors or warnings on the provided
  sample dataset in a clean environment set up with a single dependency install
  command.
- **SC-005**: The dashboard is accessible via a public URL on Streamlit Community
  Cloud using only the project's repository — no additional infrastructure or
  configuration required.

## Assumptions

- The CSV schema matches the specification in the PRD exactly (columns: date,
  order_id, product, category, region, quantity, unit_price, total_amount).
- "Sales" always means `total_amount`, not `quantity * unit_price` (these should
  be equivalent, but `total_amount` is the authoritative column).
- No authentication or access control is needed for Phase 1; the dashboard is
  publicly accessible.
- The sample dataset (~1,000 rows) is representative of the typical load; no
  pagination or lazy loading is required for Phase 1.
- Charts do not need to be mobile-responsive for Phase 1 (desktop browser is
  the primary target per NFR-2/NFR-4 in the PRD).
