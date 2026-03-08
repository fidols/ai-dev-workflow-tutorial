import pandas as pd
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
