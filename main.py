# main.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(page_title="Expense Tracker Dashboard", layout="wide")

# -----------------------------
# Title
# -----------------------------
st.title("💰 Expense Tracker Dashboard")

# -----------------------------
# Load Default Data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/expenses.csv")
    df["Date"] = pd.to_datetime(df["Date"])

    # Feature Engineering
    df["Month"] = df["Date"].dt.month
    df["Month_Name"] = df["Date"].dt.strftime('%b')

    return df

# -----------------------------
# File Upload Handling (FIXED)
# -----------------------------
uploaded_file = st.file_uploader("📂 Upload your Expense CSV", type=["csv"])

required_columns = ["Date", "Category", "Amount"]

if uploaded_file is not None:
    try:
        uploaded_file.seek(0)  # 🔥 Important fix

        df = pd.read_csv(uploaded_file)

        if df.empty:
            st.error("❌ Uploaded file is empty!")
            st.stop()

        if not all(col in df.columns for col in required_columns):
            st.error("❌ Invalid CSV format. Required columns: Date, Category, Amount")
            st.stop()

        # Convert Date
        df["Date"] = pd.to_datetime(df["Date"])

        # Feature Engineering
        df["Month"] = df["Date"].dt.month
        df["Month_Name"] = df["Date"].dt.strftime('%b')

        st.success("✅ CSV Uploaded Successfully!")

    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
        st.stop()

else:
    df = load_data()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔍 Filters")

# Category Filter
categories = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

# Date Filter (ADVANCED FEATURE 🔥)
min_date = df["Date"].min()
max_date = df["Date"].max()

date_range = st.sidebar.date_input(
    "Select Date Range",
    [min_date, max_date]
)

# Apply Filters
filtered_df = df[df["Category"].isin(categories)]

if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        (filtered_df["Date"] >= pd.to_datetime(start_date)) &
        (filtered_df["Date"] <= pd.to_datetime(end_date))
    ]

# -----------------------------
# Key Metrics
# -----------------------------
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Spending", f"₹ {filtered_df['Amount'].sum():,.0f}")
col2.metric("Average Spending", f"₹ {filtered_df['Amount'].mean():,.0f}")
col3.metric("Transactions", len(filtered_df))

# -----------------------------
# Category-wise Bar Chart
# -----------------------------
st.subheader("📊 Category-wise Spending")

category_spending = filtered_df.groupby("Category")["Amount"].sum()

fig1, ax1 = plt.subplots()
sns.barplot(x=category_spending.index, y=category_spending.values, ax=ax1)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
ax1.set_ylabel("Amount")
ax1.set_xlabel("Category")
st.pyplot(fig1)

# -----------------------------
# Pie Chart
# -----------------------------
st.subheader("🥧 Expense Distribution")

fig2, ax2 = plt.subplots()
ax2.pie(
    category_spending,
    labels=category_spending.index,
    autopct='%1.1f%%',
    startangle=90
)
plt.tight_layout()
st.pyplot(fig2)

# -----------------------------
# Monthly Trend Line Chart
# -----------------------------
st.subheader("📈 Monthly Spending Trend")

monthly_spending = filtered_df.groupby("Month_Name")["Amount"].sum()

month_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
monthly_spending = monthly_spending.reindex(month_order)

fig3, ax3 = plt.subplots()
sns.lineplot(
    x=monthly_spending.index,
    y=monthly_spending.values,
    marker="o",
    ax=ax3
)
ax3.set_xlabel("Month")
ax3.set_ylabel("Amount")
st.pyplot(fig3)

# -----------------------------
# Insights Section
# -----------------------------
st.subheader("🔍 Insights")

if not category_spending.empty:
    highest = category_spending.idxmax()
    lowest = category_spending.idxmin()

    st.info(f"💡 Top Spending Category: {highest}")
    st.write(f"👉 Lowest spending category: **{lowest}**")
    st.write(f"👉 Total transactions: **{len(filtered_df)}**")

# -----------------------------
# Download Button (PRO FEATURE 🔥)
# -----------------------------
csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    "📥 Download Filtered Data",
    csv,
    "filtered_expenses.csv",
    "text/csv"
)

# -----------------------------
# Raw Data Display
# -----------------------------
st.subheader("📄 Raw Data")
st.dataframe(filtered_df)