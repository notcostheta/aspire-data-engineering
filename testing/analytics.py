import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path

# Define paths
data_dir = Path("data")
plots_dir = Path("plots")
results_dir = Path("results")

# Ensure directories exist
plots_dir.mkdir(exist_ok=True)
results_dir.mkdir(exist_ok=True)

# Load the data
stock_prices = pd.read_csv(data_dir / "stock_price.csv", parse_dates=["Date"])
shares_outstanding = pd.read_csv(data_dir / "no_shares.csv")


# Calculate Market Cap for every day
def calculate_market_cap(row, shares):
    year = row["Date"].year
    shares_a = shares.loc[shares["Year"] == year, "Stock A"].values[0]
    shares_b = shares.loc[shares["Year"] == year, "Stock B"].values[0]
    return {
        "Market Cap A": row["Stock A"] * shares_a,
        "Market Cap B": row["Stock B"] * shares_b,
    }


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

# Save the plot
plt.savefig(plots_dir / "daily_market_cap.png")
plt.close()  # Close the plot to free up memory

# Display results
print("Average Monthly Market Cap:")
print(monthly_avg_market_cap)

print("\nDaily Percentage Change in Stock Price (first 5 rows):")
print(stock_prices[["Date", "Stock A % Change", "Stock B % Change"]].head())

# Save results to CSV
stock_prices.to_csv(results_dir / "stock_analysis_results.csv", index=False)
monthly_avg_market_cap.to_csv(results_dir / "monthly_avg_market_cap.csv")
