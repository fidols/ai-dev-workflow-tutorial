import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
st.title("ShopSmart Sales Dashboard")

# T005: Load CSV with error handling — no stack trace shown to the user
try:
    raw_df = pd.read_csv("data/sales-data.csv", parse_dates=["date"])
except FileNotFoundError:
    st.error("Data file not found at data/sales-data.csv. Please check the repository.")
    st.stop()
except Exception as e:
    st.error(f"Could not load sales data: {e}")
    st.stop()

# T006: Exclude rows with missing or non-numeric total_amount
raw_df["total_amount"] = pd.to_numeric(raw_df["total_amount"], errors="coerce")
invalid_rows = raw_df["total_amount"].isna().sum()
df = raw_df.dropna(subset=["total_amount"])

if invalid_rows > 0:
    st.info(f"{invalid_rows} row(s) skipped due to missing or invalid total_amount.")

# T007: Compute KPI scalars
total_sales = df["total_amount"].sum()
total_orders = df["order_id"].count()

# T008: Render KPI metric cards in two-column layout
col1, col2 = st.columns(2)
col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Orders", f"{total_orders:,}")

# T009: Compute time series aggregation
time_series = df.groupby("date")["total_amount"].sum().reset_index()
time_series.columns = ["date", "sales"]

# T010: Render sales trend line chart with interactive tooltips
fig_trend = px.line(
    time_series,
    x="date",
    y="sales",
    title="Sales Trend Over Time",
    labels={"sales": "Sales ($)", "date": "Date"},
)
st.plotly_chart(fig_trend, use_container_width=True)
# T011: Plotly shows tooltips by default — no custom hovertemplate suppressing them
