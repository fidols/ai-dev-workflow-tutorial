---

description: "Task list for ShopSmart Sales Dashboard implementation"
---

# Tasks: ShopSmart Sales Dashboard

**Input**: Design documents from `specs/001-sales-dashboard/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, quickstart.md ✅

**Tests**: No automated test suite in scope for Phase 1. Validation is manual
per `quickstart.md` acceptance criteria.

**Organization**: Tasks are grouped by user story to enable independent
implementation and testing of each story.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Include exact file paths in all descriptions

## Path Conventions

- Single-file app: `app.py` at repository root
- Data: `data/sales-data.csv`
- Dependencies: `pyproject.toml`, `uv.lock`, `requirements.txt`

---

## Phase 1: Setup

**Purpose**: Project initialization and dependency configuration

- [x] T001 Create `pyproject.toml` at repo root declaring project name, Python
  `>=3.11` requirement, and dependencies: `streamlit`, `pandas`, `plotly`
- [x] T002 Run `uv sync` to resolve and lock all dependencies, committing
  `uv.lock` to the repository
- [x] T003 [P] Generate `requirements.txt` from the lockfile for Streamlit Cloud
  compatibility: `uv export --no-hashes > requirements.txt`, commit the file
- [x] T004 [P] Create `app.py` at repo root with Streamlit page configuration:
  `st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")`
  and a placeholder `st.title("ShopSmart Sales Dashboard")`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Data loading and error handling infrastructure that ALL user stories
depend on. No user story work can begin until this phase is complete.

**⚠️ CRITICAL**: Phases 3, 4, and 5 are blocked until T005 and T006 are complete.

- [x] T005 In `app.py`, implement CSV loading: read `data/sales-data.csv` using
  `pandas.read_csv()` with `parse_dates=['date']`; wrap in a `try/except` block
  that calls `st.error()` with a human-readable message and `st.stop()` if the
  file is missing or unparseable — no stack trace shown to the user
- [x] T006 In `app.py`, after loading, identify rows where `total_amount` is
  null or non-numeric; exclude them from a clean `df` variable; if any rows were
  excluded, display `st.info("N rows skipped due to missing or invalid
  total_amount.")` where N is the count of excluded rows

**Checkpoint**: Run `uv run streamlit run app.py` — the app loads with no
errors on the valid CSV, and shows a clear error banner if the CSV is renamed.

---

## Phase 3: User Story 1 — KPI Snapshot at a Glance (Priority: P1) 🎯 MVP

**Goal**: Display Total Sales and Total Orders prominently on page load.

**Independent Test**: Open the dashboard; verify Total Sales and Total Orders
are visible within 5 seconds, matching values computed by the quickstart
validation script. This is the full MVP — independently demoed or used in
an executive meeting.

### Implementation for User Story 1

- [x] T007 [US1] In `app.py`, compute KPI scalars from the clean `df`:
  `total_sales = df['total_amount'].sum()` and
  `total_orders = df['order_id'].count()`
- [x] T008 [US1] In `app.py`, render KPI cards using `st.metric()` in a
  two-column layout: left column shows "Total Sales" formatted as
  `f"${total_sales:,.2f}"`, right column shows "Total Orders" formatted as
  `f"{total_orders:,}"`

**Checkpoint**: Dashboard loads showing both KPI cards. Values match the
quickstart validation script output exactly (SC-001, SC-002).

---

## Phase 4: User Story 2 — Sales Trend Over Time (Priority: P2)

**Goal**: Render an interactive line chart of sales over time.

**Independent Test**: Verify the line chart displays one point per calendar
date in the dataset, that the x-axis spans the full date range, and that
hovering any point shows the exact daily sales total.

### Implementation for User Story 2

- [x] T009 [US2] In `app.py`, compute the time series aggregation:
  `time_series = df.groupby('date')['total_amount'].sum().reset_index()`,
  rename columns to `['date', 'sales']`
- [x] T010 [US2] In `app.py`, render the trend chart using
  `plotly.express.line(time_series, x='date', y='sales',
  title='Sales Trend Over Time', labels={'sales': 'Sales ($)', 'date': 'Date'})`;
  display via `st.plotly_chart(fig, use_container_width=True)`
- [x] T011 [US2] Verify hover tooltips on the line chart show exact `sales`
  values (Plotly shows tooltips by default; confirm no custom `hovertemplate`
  suppresses them)

**Checkpoint**: Line chart renders with full date range, correct trend shape,
and interactive tooltips matching daily sums from the quickstart script (FR-004).

---

## Phase 5: User Story 3 — Category and Regional Breakdown (Priority: P3)

**Goal**: Render two bar charts (by category, by region) sorted highest to
lowest, with interactive tooltips.

**Independent Test**: Verify two bar charts are present; each shows all
expected categories/regions sorted descending; hover tooltips match CSV
group sums from the quickstart script.

### Implementation for User Story 3

- [x] T012 [US3] In `app.py`, compute category aggregation:
  `by_category = df.groupby('category')['total_amount'].sum().reset_index()
  .sort_values('total_amount', ascending=False)`;
  rename columns to `['category', 'sales']`
- [x] T013 [US3] In `app.py`, render category bar chart using
  `plotly.express.bar(by_category, x='category', y='sales',
  title='Sales by Category', labels={'sales': 'Sales ($)', 'category': 'Category'})`;
  display via `st.plotly_chart(fig, use_container_width=True)`
- [x] T014 [US3] In `app.py`, compute region aggregation:
  `by_region = df.groupby('region')['total_amount'].sum().reset_index()
  .sort_values('total_amount', ascending=False)`;
  rename columns to `['region', 'sales']`
- [x] T015 [US3] In `app.py`, render region bar chart using
  `plotly.express.bar(by_region, x='region', y='sales',
  title='Sales by Region', labels={'sales': 'Sales ($)', 'region': 'Region'})`;
  display via `st.plotly_chart(fig, use_container_width=True)`

**Checkpoint**: Both bar charts render with correct sort order and all
groups represented. Hover tooltips match group sums from quickstart script
(FR-007). All three user stories now independently functional.

---

## Phase 6: Polish & Validation

**Purpose**: End-to-end validation and deployment

- [ ] T016 Run the full quickstart.md validation checklist against the
  running app: SC-001 (5-second load), SC-002 (data accuracy), SC-003
  (60-second user test), FR-004/FR-007 (tooltips), FR-009 (error state),
  SC-004 (no warnings)
- [ ] T017 [P] Push branch `001-sales-dashboard` to GitHub; deploy to
  Streamlit Community Cloud from `app.py` entry point; verify public URL
  loads the dashboard and passes SC-001 through SC-005

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately; T003 and T004 are parallel
- **Foundational (Phase 2)**: Depends on Phase 1 completion — BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Phase 2 — no dependencies on US2 or US3
- **User Story 2 (Phase 4)**: Depends on Phase 2 — no dependencies on US1 or US3
- **User Story 3 (Phase 5)**: Depends on Phase 2 — no dependencies on US1 or US2
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **US1 (P1)**: Can start after Foundational — independently testable
- **US2 (P2)**: Can start after Foundational — independently testable
- **US3 (P3)**: Can start after Foundational — independently testable
- US2 and US3 are sequenced after US1 by priority, not by technical dependency

### Within Each User Story

- Computation task → Rendering task (e.g., T007 before T008, T009 before T010)
- All tasks in US3 touch `app.py` — implement sequentially (T012 → T013 → T014 → T015)

### Parallel Opportunities

- T003 and T004 (Phase 1) can run in parallel
- With a team: US1, US2, US3 phases can run in parallel after Phase 2

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1 (T007–T008)
4. **STOP and VALIDATE**: KPI cards match expected values, load under 5 seconds
5. Demo to stakeholders — this is a fully usable executive dashboard

### Incremental Delivery

1. Setup + Foundational → data loads cleanly
2. Add US1 (KPIs) → validate independently → demoed as MVP
3. Add US2 (trend chart) → validate independently → deploy update
4. Add US3 (bar charts) → validate independently → deploy final Phase 1

---

## Notes

- [P] tasks = different files or truly independent; US3 tasks share `app.py`
  and must be done sequentially
- [Story] label maps each task to a user story for traceability
- Commit after each checkpoint (end of each phase) at minimum
- Run `uv run streamlit run app.py` to test after every task — fast feedback
- Avoid: touching aggregation logic after it has been validated (data fidelity risk)
