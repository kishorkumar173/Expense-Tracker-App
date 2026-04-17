# src/data_generator.py

import pandas as pd
import numpy as np
import os


def generate_expense_data(num_records=500):
    np.random.seed(42)

    # Date range
    dates = pd.date_range(start="2024-01-01", end="2024-12-31")

    # Categories
    categories = [
        "Food", "Travel", "Rent", "Shopping",
        "Entertainment", "Healthcare", "Bills", "Education"
    ]

    # Payment methods
    payment_methods = ["Cash", "UPI", "Debit Card", "Credit Card"]

    # Generate base data
    data = {
        "Date": np.random.choice(dates, num_records),
        "Category": np.random.choice(categories, num_records),
        "Payment_Method": np.random.choice(payment_methods, num_records)
    }

    df = pd.DataFrame(data)

    # ✅ Add realistic spending (IMPORTANT FIX)
    amounts = []
    for cat in df["Category"]:
        if cat == "Rent":
            amounts.append(np.random.randint(5000, 15000))
        elif cat == "Food":
            amounts.append(np.random.randint(100, 1000))
        elif cat == "Travel":
            amounts.append(np.random.randint(500, 5000))
        else:
            amounts.append(np.random.randint(200, 4000))

    df["Amount"] = amounts

    # Sort by date
    df = df.sort_values(by="Date")

    return df


def save_data(df, path="data/expenses.csv"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"✅ Dataset saved at: {path}")


# Run script
if __name__ == "__main__":
    df = generate_expense_data(500)
    save_data(df)
    print(df.head())