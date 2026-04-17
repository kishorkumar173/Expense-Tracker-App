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
# Load Cleaned Data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/expenses.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    
    # Feature Engineering
    df["Month"] = df["Date"].dt.month
    df["Month_Name"] = df["Date"].dt.strftime('%b')
    
    return df

df = load_data()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔍 Filters")

categories = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

filtered_df = df[df["Category"].isin(categories)]

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
plt.xticks(rotation=30)
ax1.set_ylabel("Amount")
ax1.set_xlabel("Category")
st.pyplot(fig1)

# -----------------------------
# Pie Chart
# -----------------------------
st.subheader("🥧 Expense Distribution")

fig2, ax2 = plt.subplots()
ax2.pie(category_spending, labels=category_spending.index, autopct='%1.1f%%')
ax2.set_title("Spending Share by Category")
st.pyplot(fig2)

# -----------------------------
# Monthly Trend Line Chart
# -----------------------------
st.subheader("📈 Monthly Spending Trend")

monthly_spending = filtered_df.groupby("Month_Name")["Amount"].sum()

# Ensure correct month order
month_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
monthly_spending = monthly_spending.reindex(month_order)

fig3, ax3 = plt.subplots()
sns.lineplot(x=monthly_spending.index, y=monthly_spending.values, marker="o", ax=ax3)
ax3.set_xlabel("Month")
ax3.set_ylabel("Amount")
st.pyplot(fig3)

# -----------------------------
# Raw Data Display
# -----------------------------
st.subheader("📄 Raw Data")
st.dataframe(filtered_df)

# -----------------------------
# Insights Section
# -----------------------------
st.subheader("🔍 Insights")

if not category_spending.empty:
    highest = category_spending.idxmax()
    lowest = category_spending.idxmin()

    st.write(f"👉 Highest spending category: **{highest}**")
    st.write(f"👉 Lowest spending category: **{lowest}**")
    st.write(f"👉 Total transactions: **{len(filtered_df)}**")