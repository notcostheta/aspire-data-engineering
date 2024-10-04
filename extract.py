#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path
import json


def load_excel_data(file_path, sheet_name, skiprows=0):
    """
    Load data from an Excel file into a DataFrame.

    Parameters:
    - file_path (str): Path to the Excel file.
    - sheet_name (str): Name of the sheet to load.
    - skiprows (int): Number of rows to skip at the start of the sheet.

    Returns:
    - pd.DataFrame: DataFrame containing the loaded data.
    """
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=skiprows)
        return df
    except Exception as e:
        print(f"Error loading data from {file_path}: {e}")
        return None


def load_data(file_path, parse_dates=None):
    """
    Load data from a CSV file into a DataFrame.

    Parameters:
    - file_path (str): Path to the CSV file.
    - parse_dates (list): List of column names to parse as dates.

    Returns:
    - pd.DataFrame: DataFrame containing the loaded data.
    """
    try:
        df = pd.read_csv(file_path, parse_dates=parse_dates)
        return df
    except Exception as e:
        print(f"Error loading data from {file_path}: {e}")
        return None


def save_to_csv(df, file_path):
    """
    Save a DataFrame to a CSV file.

    Parameters:
    - df (pd.DataFrame): DataFrame to save.
    - file_path (str): Path to save the CSV file.
    """
    try:
        df.to_csv(file_path, index=False)
        print(f"Data successfully saved to {file_path}")
    except Exception as e:
        print(f"Error saving data to {file_path}: {e}")


def calculate_market_cap(row, shares):
    """
    Calculate market capitalization for a given row.

    Parameters:
    - row (pd.Series): A row from the stock prices DataFrame.
    - shares (pd.DataFrame): DataFrame containing shares outstanding.

    Returns:
    - dict: Market cap for Stock A and Stock B.
    """
    year = row["Date"].year
    shares_a = shares.loc[shares["Year"] == year, "Stock A"].values[0]
    shares_b = shares.loc[shares["Year"] == year, "Stock B"].values[0]
    return {
        "Market Cap A": row["Stock A"] * shares_a,
        "Market Cap B": row["Stock B"] * shares_b,
    }


def parse_json_payload(payload):
    """
    Parse JSON payload and extract transaction_type and amount.

    Parameters:
    - payload (str): JSON payload as a string.

    Returns:
    - tuple: (transaction_type, amount)
    """
    try:
        data = json.loads(payload)
        return data.get("transaction_type"), data.get("amount")
    except json.JSONDecodeError:
        return None, None


def main():
    print("Starting main function")
    # Define file paths and sheet names
    excel_file = "assessment.xlsx"
    python_instructions_sheet = "Python Instructions"
    account_tab_sheet = "account_tab"
    transaction_tab_sheet = "transaction_tab"

    # Define base paths
    base_path = Path(".")
    data_path = base_path / "data"
    plots_path = base_path / "plots"
    outputs_path = base_path / "outputs"

    print(f"Current working directory: {Path.cwd()}")
    print(f"Excel file path: {base_path / excel_file}")
    print(f"Data path: {data_path}")

    # Create directories if they don't exist
    data_path.mkdir(parents=True, exist_ok=True)
    plots_path.mkdir(parents=True, exist_ok=True)
    outputs_path.mkdir(parents=True, exist_ok=True)

    # Load the main data from the Excel file
    print("Loading Excel data...")
    base_excel = load_excel_data(excel_file, python_instructions_sheet, skiprows=2)
    if base_excel is None:
        print("Failed to load Excel data. Exiting.")
        return

    # Extract and process the first two dataframes
    df1 = base_excel.iloc[:, 0:3].dropna()
    df2 = base_excel.iloc[:, 6:9].dropna()
    # Rename the columns of the second dataframe
    df2.columns = ["Year", "Stock A", "Stock B"]

    # Print the shapes of the dataframes
    print(f"Shape of df1: {df1.shape}")
    print(f"Shape of df2: {df2.shape}")

    # Save the dataframes to CSV files
    print("Saving dataframes to CSV...")
    save_to_csv(df1, data_path / "stock_price.csv")
    save_to_csv(df2, data_path / "no_shares.csv")

    # Load and save the account_tab and transaction_tab sheets
    account_tab = load_excel_data(excel_file, account_tab_sheet)
    if account_tab is not None:
        save_to_csv(account_tab, data_path / "account_tab.csv")

    transaction_tab = load_excel_data(excel_file, transaction_tab_sheet)
    if transaction_tab is not None:
        # Parse JSON payload and add new columns
        transaction_tab[["transaction_type", "amount"]] = (
            transaction_tab["payload"].apply(parse_json_payload).tolist()
        )
        # Remove the original 'payload' column
        transaction_tab = transaction_tab.drop(columns=["payload"])
        save_to_csv(transaction_tab, data_path / "transaction_tab.csv")

    # Load the data for analysis
    print("Loading CSV data for analysis...")
    stock_prices = load_data(data_path / "stock_price.csv", parse_dates=["Date"])
    shares_outstanding = load_data(data_path / "no_shares.csv")

    if stock_prices is None or shares_outstanding is None:
        print("Failed to load CSV data. Exiting.")
        return

    print("CSV data loaded successfully. Continuing with analysis...")

    # Calculate Market Cap for every day
    market_caps = stock_prices.apply(
        lambda row: pd.Series(calculate_market_cap(row, shares_outstanding)), axis=1
    )
    stock_prices = pd.concat([stock_prices, market_caps], axis=1)

    # Compute Average Monthly Market Cap
    stock_prices["Month"] = stock_prices["Date"].dt.to_period("M")
    monthly_avg_market_cap = stock_prices.groupby("Month")[
        ["Market Cap A", "Market Cap B"]
    ].mean()

    # Calculate daily percentage change in stock price
    stock_prices["Stock A % Change"] = stock_prices["Stock A"].pct_change() * 100
    stock_prices["Stock B % Change"] = stock_prices["Stock B"].pct_change() * 100

    # Plot Daily Market Cap over time
    plt.figure(figsize=(12, 6))
    plt.plot(stock_prices["Date"], stock_prices["Market Cap A"], label="Stock A")
    plt.plot(stock_prices["Date"], stock_prices["Market Cap B"], label="Stock B")
    plt.title("Daily Market Cap Over Time")
    plt.xlabel("Date")
    plt.ylabel("Market Cap")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(plots_path / "daily_market_cap.png")
    plt.close()  # Close the plot to free up memory

    # Display results
    print("Average Monthly Market Cap:")
    print(monthly_avg_market_cap)

    print("\nDaily Percentage Change in Stock Price (first 5 rows):")
    print(stock_prices[["Date", "Stock A % Change", "Stock B % Change"]].head())

    # Save results to CSV
    save_to_csv(stock_prices, outputs_path / "stock_analysis_results.csv")
    save_to_csv(monthly_avg_market_cap, outputs_path / "monthly_avg_market_cap.csv")

    print("Analysis completed successfully.")


if __name__ == "__main__":
    main()
