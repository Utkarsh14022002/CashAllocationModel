import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def preprocess_csv(input_file, output_file):
    """Preprocess the CSV file to set correct headers and start from the 4th row."""
    # Define the correct headers
    column_names = ["Date", "Close", "High", "Low", "Open", "Volume"]

    # Read the CSV file, skipping the first three rows
    data = pd.read_csv(input_file, skiprows=3, names=column_names)

    # Save the processed data to a new CSV file
    data.to_csv(output_file, index=False)

    print(f"✅ Preprocessed CSV saved to {output_file}")


# 1. Market Volatility Metrics
def calculate_volatility_metrics(nifty_file, midcap_file):
    """Calculate 30-day rolling volatility and volatility ratio."""
    # Read the CSV files, skipping the first two rows and setting proper headers
    column_names = ["Date", "Close", "High", "Low", "Open", "Volume"]
    nifty_data = pd.read_csv(nifty_file, skiprows=1, names=column_names, parse_dates=["Date"])
    midcap_data = pd.read_csv(midcap_file, skiprows=1, names=column_names, parse_dates=["Date"])

    # Calculate daily returns
    nifty_data["Daily Return"] = nifty_data["Close"].pct_change()
    midcap_data["Daily Return"] = midcap_data["Close"].pct_change()

    # Calculate 30-day rolling volatility
    nifty_data["30-Day Volatility"] = nifty_data["Daily Return"].rolling(window=30).std()
    midcap_data["30-Day Volatility"] = midcap_data["Daily Return"].rolling(window=30).std()

    # Calculate volatility ratio
    nifty_data["Volatility Ratio"] = nifty_data["30-Day Volatility"] / midcap_data["30-Day Volatility"]

    # Handle missing data
    nifty_data.fillna(0, inplace=True)
    midcap_data.fillna(0, inplace=True)

    # Visualization
    plt.figure(figsize=(10, 6))
    plt.plot(nifty_data["Date"], nifty_data["30-Day Volatility"], label="Nifty 30-Day Volatility")
    plt.plot(midcap_data["Date"], midcap_data["30-Day Volatility"], label="Midcap 30-Day Volatility")
    plt.title("30-Day Rolling Volatility")
    plt.xlabel("Date")
    plt.ylabel("Volatility")
    plt.legend()
    plt.grid()
    plt.savefig("../screenshots/volatility_metrics.png")
    plt.close()

    return nifty_data[["Date", "30-Day Volatility", "Volatility Ratio"]], midcap_data[["Date", "30-Day Volatility"]]

# 2. Traded Volume Metrics

def calculate_traded_volume(nifty_file, midcap_file):
    """Calculate 30-day rolling average traded volume."""
    # Read the CSV files, skipping the first two rows and setting proper headers
    column_names = ["Date", "Close", "High", "Low", "Open", "Volume"]

    # Read the CSV files, skipping the first three rows and setting proper headers
    # Read only the Date and Volume columns from the CSV files
    nifty_data = pd.read_csv(
        nifty_file,
        skiprows=1,
        usecols=[0, 5],  # Select only the Date (0th column) and Volume (6th column)
        names=["Date", "Volume"],
        parse_dates=["Date"]
    )
    midcap_data = pd.read_csv(
        midcap_file,
        skiprows=1,
        usecols=[0, 5],  # Select only the Date (0th column) and Volume (6th column)
        names=["Date", "Volume"],
        parse_dates=["Date"]
    )

    # Ensure the Volume column is numeric
    nifty_data["Volume"] = pd.to_numeric(nifty_data["Volume"], errors="coerce")
    midcap_data["Volume"] = pd.to_numeric(midcap_data["Volume"], errors="coerce")
    # print(nifty_data["Volume"].head())
    # Replace zeros or invalid values with NaN to exclude them from the rolling average
    nifty_data["Volume"] = nifty_data["Volume"].replace(0, np.nan)
    midcap_data["Volume"] = midcap_data["Volume"].replace(0, np.nan)

    # Handle missing values
    if nifty_data["Volume"].notna().sum() == 0:
        nifty_data["Volume"] = 0
    else:
        nifty_data["Volume"] = nifty_data["Volume"].fillna(nifty_data["Volume"].median())

    if midcap_data["Volume"].notna().sum() == 0:
        midcap_data["Volume"] = 0
    else:
        midcap_data["Volume"] = midcap_data["Volume"].fillna(midcap_data["Volume"].median())

    # Calculate 30-day rolling average traded volume
    nifty_data["Average Volume"] = nifty_data["Volume"].rolling(window=30, min_periods=1).mean()
    midcap_data["Average Volume"] = midcap_data["Volume"].rolling(window=30, min_periods=1).mean()

    # # Debugging: Print the Average Volume column
    # print("Nifty Average Volume:")
    # print(nifty_data[["Date", "Average Volume"]].head())
    # print("Midcap Average Volume:")
    # print(midcap_data[["Date", "Average Volume"]].head())

    return nifty_data[["Date", "Average Volume"]], midcap_data[["Date", "Average Volume"]]



# 3. Institutional Flow Metrics
def calculate_institutional_flow_metrics(fii_dii_file):
    """Calculate FII/DII net flows and FII/DII ratio."""
    # Define column names for the CSV file
    column_names = [
        "MONTH", "FII Buy Amount", "FII Sell Amount", "FII Net Amount",
        "DII Buy Amount", "DII Sell Amount", "DII Net Amount", "NIFTY"
    ]

    # Read the CSV file, skipping the first two rows and using the second row as the header
    fii_dii_data = pd.read_csv(fii_dii_file, skiprows=1, names=column_names)

    # Drop any rows that contain non-numeric values in the FII and DII columns
    fii_dii_data = fii_dii_data[pd.to_numeric(fii_dii_data["FII Net Amount"], errors='coerce').notna()]
    fii_dii_data = fii_dii_data[pd.to_numeric(fii_dii_data["DII Net Amount"], errors='coerce').notna()]

    # Convert relevant columns to numeric (removing commas)
    fii_dii_data["FII Net Amount"] = fii_dii_data["FII Net Amount"].astype(float)
    fii_dii_data["DII Net Amount"] = fii_dii_data["DII Net Amount"].astype(float)

    # Calculate FII/DII net flows
    fii_dii_data["FII Net Flow"] = fii_dii_data["FII Net Amount"]
    fii_dii_data["DII Net Flow"] = fii_dii_data["DII Net Amount"]

    # Calculate FII/DII ratio (avoiding division by zero)
    fii_dii_data["FII/DII Ratio"] = np.where(
        fii_dii_data["DII Net Flow"] != 0,
        fii_dii_data["FII Net Flow"] / fii_dii_data["DII Net Flow"],
        np.nan
    )

    # Replace infinite and NaN values with 0
    fii_dii_data.replace([np.inf, -np.inf], np.nan, inplace=True)
    fii_dii_data.fillna(0, inplace=True)

    # Visualization
    plt.figure(figsize=(10, 6))
    plt.plot(fii_dii_data["MONTH"], fii_dii_data["FII Net Flow"], label="FII Net Flow", marker="o")
    plt.plot(fii_dii_data["MONTH"], fii_dii_data["DII Net Flow"], label="DII Net Flow", marker="o")
    plt.title("Institutional Flows (FII vs DII)")
    plt.xlabel("Month")
    plt.ylabel("Net Flow (INR Crore)")
    plt.legend()
    plt.grid()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("../screenshots/institutional_flows.png")
    plt.close()

    return fii_dii_data[["MONTH", "FII Net Flow", "DII Net Flow", "FII/DII Ratio"]]


# 4. Market Breadth Indicators for Nifty 50 Data
def calculate_market_breadth(nifty_file):
    """Calculate advance-decline ratio."""
    column_names = ["Date", "Price", "Close", "High", "Low", "Open", "Volume"]
    nifty_data = pd.read_csv(nifty_file, skiprows=30, names=column_names, parse_dates=["Date"])

    # Calculate advance-decline ratio
    nifty_data["Advance-Decline Ratio"] = (nifty_data["Close"] > nifty_data["Open"]).rolling(window=30).sum() / \
                                          (nifty_data["Close"] < nifty_data["Open"]).rolling(window=30).sum()

    # Handle missing data
    nifty_data.fillna(0, inplace=True)

    # Visualization
    plt.figure(figsize=(10, 6))
    plt.plot(nifty_data["Date"], nifty_data["Advance-Decline Ratio"], label="Advance-Decline Ratio")
    plt.title("Advance-Decline Ratio")
    plt.xlabel("Date")
    plt.ylabel("Ratio")
    plt.legend()
    plt.grid()
    plt.savefig("../screenshots/market_breadth.png")
    plt.close()

    return nifty_data[["Date", "Advance-Decline Ratio"]]

# 5. Interest Rate Metrics
def calculate_interest_rate_metrics(rbi_file):
    """Extract interest rate metrics from RBI data."""
    # Read the CSV file
    rbi_data = pd.read_csv(rbi_file, header=None, names=["Policy", "Rate"])

    # Clean the "Rate" column to extract numeric values
    rbi_data["Rate"] = rbi_data["Rate"].str.extract(r"([\d\.]+)").astype(float)

    # Extract relevant rates
    repo_rate = rbi_data.loc[rbi_data["Policy"].str.contains("Policy Repo Rate", case=False), "Rate"].values[0]
    reverse_repo_rate = rbi_data.loc[rbi_data["Policy"].str.contains("Fixed Reverse Repo Rate", case=False), "Rate"].values[0]

    # Visualization
    rates = {"Repo Rate": repo_rate, "Reverse Repo Rate": reverse_repo_rate}
    plt.bar(rates.keys(), rates.values())
    plt.title("Interest Rate Metrics")
    plt.ylabel("Rate (%)")
    plt.grid()
    plt.savefig("../screenshots/interest_rates.png")
    plt.close()

    return {"Repo Rate": repo_rate, "Reverse Repo Rate": reverse_repo_rate}

# Main Function to Execute All Features
def main():
    # File paths
    nifty_file = "../data_collections/nifty_50_data.csv"
    midcap_file = "../data_collections/nifty_midcap_100_data.csv"
    fii_dii_file = "../data_collections/fii_dii_data.csv"
    rbi_file = "../data_collections/rbi_policy_rates.csv"

    nifty_output_file = "../data_collections/processed_nifty_50_data.csv"
    midcap_output_file = "../data_collections/processed_midcap_100_data.csv"
    preprocess_csv(nifty_file, nifty_output_file)
    preprocess_csv(midcap_file, midcap_output_file)


    # Calculate features
    nifty_volatility, midcap_volatility = calculate_volatility_metrics(nifty_output_file, midcap_output_file)
    nifty_volume, midcap_volume = calculate_traded_volume(nifty_output_file, midcap_output_file)
    institutional_flows = calculate_institutional_flow_metrics(fii_dii_file)
    market_breadth = calculate_market_breadth(nifty_file)
    interest_rates = calculate_interest_rate_metrics(rbi_file)

    # Save results
    nifty_volatility.to_csv("../data_collections/nifty_volatility.csv", index=False)
    midcap_volatility.to_csv("../data_collections/midcap_volatility.csv", index=False)
    nifty_volume.to_csv("../data_collections/nifty_volume.csv", index=False)
    midcap_volume.to_csv("../data_collections/midcap_volume.csv", index=False)
    institutional_flows.to_csv("../data_collections/institutional_flows.csv", index=False)
    market_breadth.to_csv("../data_collections/market_breadth.csv", index=False)
    pd.DataFrame([interest_rates]).to_csv("../data_collections/interest_rates.csv", index=False)

    print("✅ Feature engineering completed and results saved!")

if __name__ == "__main__":
    main()