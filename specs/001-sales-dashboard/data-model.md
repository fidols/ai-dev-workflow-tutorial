# Data Model: ShopSmart Sales Dashboard

**Feature**: 001-sales-dashboard
**Date**: 2026-03-07

---

## Source Entity: Transaction

The atomic unit of all data in this dashboard. Loaded directly from
`data/sales-data.csv`. No transformation or normalization is applied to the
source data before aggregation.

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| `date` | date | Transaction date | MUST be parseable as a date; rows with unparseable dates are excluded and counted |
| `order_id` | string | Unique order identifier | Used for order count; duplicates counted individually (each row = one transaction) |
| `product` | string | Product name | Informational; not used in Phase 1 aggregations |
| `category` | string | Product category | MUST be non-null to appear in category chart; null rows excluded and counted |
| `region` | string | Geographic region | MUST be non-null to appear in region chart; null rows excluded and counted |
| `quantity` | integer | Units sold | Informational in Phase 1; not aggregated directly |
| `unit_price` | decimal | Price per unit | Informational in Phase 1; not aggregated directly |
| `total_amount` | decimal | Total transaction value | MUST be numeric and non-null to be included in any sales calculation; null/non-numeric rows excluded and counted |

**Row exclusion rule**: Any row excluded from calculations MUST be surfaced to
the user as a count (e.g., "3 rows skipped due to missing total_amount"). This
satisfies Principle I (Data Fidelity) — no silent data loss.

---

## Derived Entities (computed at runtime, not stored)

### KPI: Total Sales

```
total_sales = transactions['total_amount'].sum()
```

- Source: all valid Transaction rows
- Format: USD currency string — `$XXX,XXX` (commas, no cents unless non-zero)
- Displayed as: prominent metric card (P1, User Story 1)

### KPI: Total Orders

```
total_orders = transactions['order_id'].count()
```

- Source: all valid Transaction rows
- Format: whole number with comma separator — `482`
- Displayed as: prominent metric card (P1, User Story 1)

### Time Series: Sales by Date

```
time_series = transactions.groupby('date')['total_amount'].sum().reset_index()
time_series.columns = ['date', 'sales']
```

- Granularity: daily (one point per calendar date present in the data)
- X-axis: `date` (chronological)
- Y-axis: `sales` (sum of `total_amount` for that date)
- Displayed as: line chart with Plotly (P2, User Story 2)

### Category Summary: Sales by Category

```
by_category = (
    transactions.groupby('category')['total_amount']
    .sum()
    .reset_index()
    .sort_values('total_amount', ascending=False)
)
by_category.columns = ['category', 'sales']
```

- Sort: descending by `sales`
- All categories present in the data MUST appear (no top-N filtering)
- Displayed as: horizontal or vertical bar chart with Plotly (P3, User Story 3)

### Region Summary: Sales by Region

```
by_region = (
    transactions.groupby('region')['total_amount']
    .sum()
    .reset_index()
    .sort_values('total_amount', ascending=False)
)
by_region.columns = ['region', 'sales']
```

- Sort: descending by `sales`
- All regions present in the data MUST appear
- Displayed as: horizontal or vertical bar chart with Plotly (P3, User Story 3)

---

## State Model

This is a stateless application. All derived entities are recomputed on every
page load from the raw CSV. No state is persisted between sessions. No user
input mutates the data.

---

## Error States

| Condition | Behavior |
|-----------|----------|
| CSV file missing | Display error banner: "Data file not found at data/sales-data.csv. Please check the repository." App stops rendering charts. |
| CSV unparseable | Display error banner with exception message. App stops rendering charts. |
| Rows with null `total_amount` | Exclude from calculations. Display info banner: "N rows skipped due to missing or invalid total_amount." |
| Empty dataset after exclusions | Display warning: "No valid transaction data found." KPIs show $0 / 0 Orders. Charts render empty. |
