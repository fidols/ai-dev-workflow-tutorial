# Quickstart: ShopSmart Sales Dashboard

**Feature**: 001-sales-dashboard
**Date**: 2026-03-07

Use this guide to validate that the implementation is working correctly from
a clean environment.

---

## Prerequisites

- Python 3.11 or later
- `uv` installed (`pip install uv` or `brew install uv`)
- Git (to clone the repository)

---

## Step 1: Clone and enter the repository

```bash
git clone <your-fork-url>
cd <repo-directory>
git checkout 001-sales-dashboard
```

---

## Step 2: Install dependencies

```bash
uv sync
```

Expected output: uv resolves and installs all packages from `uv.lock`.
No manual pip installs. No virtual environment activation needed.

---

## Step 3: Verify the data file exists

```bash
ls data/sales-data.csv
```

Expected: file found. If missing, the dashboard will display an error banner
(this is expected behavior per the spec — not a bug).

---

## Step 4: Run the dashboard

```bash
uv run streamlit run app.py
```

Expected: Streamlit opens in your browser at `http://localhost:8501`.

---

## Step 5: Validate against acceptance criteria

Work through each check below. All must pass before the feature is complete.

### SC-001: Load time

- [ ] The dashboard fully loads (all KPIs and charts visible) within 5 seconds
  of opening `http://localhost:8501`. Time it with a stopwatch if needed.

### SC-002 + FR-010: Data accuracy

Open `data/sales-data.csv` in a spreadsheet or run:

```bash
uv run python -c "
import pandas as pd
df = pd.read_csv('data/sales-data.csv')
print('Total Sales:', df['total_amount'].sum())
print('Total Orders:', df['order_id'].count())
print('By Category:')
print(df.groupby('category')['total_amount'].sum().sort_values(ascending=False))
print('By Region:')
print(df.groupby('region')['total_amount'].sum().sort_values(ascending=False))
"
```

- [ ] **Total Sales** displayed on dashboard matches `total_amount` sum exactly
- [ ] **Total Orders** displayed on dashboard matches row count exactly
- [ ] **Each category bar** height matches the category sum above
- [ ] **Each region bar** height matches the region sum above
- [ ] **Trend chart** shows one point per date; values match daily sums

### SC-003: First-time user can find KPIs in 60 seconds

- [ ] Ask someone unfamiliar with the dashboard to open it and identify:
  Total Sales, Total Orders, top category, top region, and whether sales
  trend up or down. They should succeed within 60 seconds.

### FR-004 + FR-007: Interactive tooltips

- [ ] Hover over any point on the line chart → exact sales value appears
- [ ] Hover over any bar on the category chart → exact sales value appears
- [ ] Hover over any bar on the region chart → exact sales value appears

### FR-009: Error handling

- [ ] Temporarily rename `data/sales-data.csv` to something else, reload
  the dashboard → a clear error message appears, no stack trace is shown
  to the user
- [ ] Restore the file name before proceeding

### SC-004: Clean run, no errors

- [ ] Terminal running `streamlit run app.py` shows no Python warnings or
  errors after the page loads with the valid CSV

---

## Step 6: Streamlit Cloud deployment validation

1. Push branch to GitHub
2. Log in to Streamlit Community Cloud
3. Deploy from the `001-sales-dashboard` branch, entry point `app.py`
4. Confirm the public URL loads the dashboard and passes SC-001 through SC-004
   in the cloud environment

---

## Expected values (from PRD)

| Metric | Expected |
|--------|----------|
| Total Sales | ~$650,000 – $700,000 |
| Total Orders | 482 |
| Categories | Electronics, Accessories, Audio, Wearables, Smart Home |
| Regions | North, South, East, West |
