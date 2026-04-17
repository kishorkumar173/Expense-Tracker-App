# src/analysis.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# -----------------------------
# Load Dataset
# -----------------------------
def load_data(path="data/expenses.csv"):
    df = pd.read_csv(path)
    df["Date"] = pd.to_datetime(df["Date"])
    return df


# -----------------------------
# Feature Engineering
# -----------------------------
def add_features(df):
    df["Month"] = df["Date"].dt.month
    df["Day"] = df["Date"].dt.day_name()
    return df


# -----------------------------
# Category Analysis
# -----------------------------
def category_analysis(df):
    category_spending = df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
    print("\n📊 Category-wise Spending:\n", category_spending)
    return category_spending


# -----------------------------
# Monthly Trend Analysis
# -----------------------------
def monthly_analysis(df):
    monthly_spending = df.groupby("Month")["Amount"].sum()
    print("\n📈 Monthly Spending:\n", monthly_spending)
    return monthly_spending


# -----------------------------
# Visualization
# -----------------------------
def create_visualizations(category_spending, monthly_spending):
    os.makedirs("outputs", exist_ok=True)

    # Bar Chart
    plt.figure(figsize=(8,5))
    sns.barplot(x=category_spending.index, y=category_spending.values)
    plt.title("Category-wise Spending")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig("outputs/category_bar.png")
    plt.show()

    # Pie Chart
    plt.figure(figsize=(6,6))
    plt.pie(category_spending, labels=category_spending.index, autopct='%1.1f%%')
    plt.title("Spending Distribution")
    plt.savefig("outputs/pie_chart.png")
    plt.show()

    # Line Chart
    plt.figure(figsize=(8,5))
    sns.lineplot(x=monthly_spending.index, y=monthly_spending.values)
    plt.title("Monthly Spending Trend")
    plt.xlabel("Month")
    plt.ylabel("Amount")
    plt.savefig("outputs/monthly_trend.png")
    plt.show()


# -----------------------------
# Insights Generation
# -----------------------------
def generate_insights(df, category_spending):
    print("\n🔍 Insights:")

    highest = category_spending.idxmax()
    print(f"👉 Highest spending category: {highest}")

    avg = df["Amount"].mean()
    print(f"👉 Average transaction amount: {avg:.2f}")

    if category_spending.max() > 50000:
        print("⚠️ Warning: Overspending detected in a category!")

    low = category_spending.idxmin()
    print(f"👉 Lowest spending category: {low}")


# -----------------------------
# Main Execution
# -----------------------------
if __name__ == "__main__":
    df = load_data()
    df = add_features(df)

    category_spending = category_analysis(df)
    monthly_spending = monthly_analysis(df)

    create_visualizations(category_spending, monthly_spending)
    generate_insights(df, category_spending)