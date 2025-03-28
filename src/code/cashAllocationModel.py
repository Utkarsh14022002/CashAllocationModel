import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculate_cash_allocation(volatility_file, volume_file, institutional_flows_file, market_breadth_file, risk_tolerance="medium"):
    """
    Calculate the optimal cash allocation percentage based on liquidity metrics.
    
    Parameters:
    - volatility_file: Path to the Nifty volatility CSV file.
    - volume_file: Path to the Nifty traded volume CSV file.
    - institutional_flows_file: Path to the institutional flows CSV file.
    - market_breadth_file: Path to the market breadth CSV file.
    - risk_tolerance: User's risk tolerance ("high", "medium", "low").
    
    Returns:
    - Recommended cash allocation percentage.
    """
    # Load the data
    volatility_data = pd.read_csv(volatility_file)
    volume_data = pd.read_csv(volume_file)
    institutional_flows_data = pd.read_csv(institutional_flows_file)
    market_breadth_data = pd.read_csv(market_breadth_file)

    # Normalize the metrics (scaling between 0 and 1)
    volatility_data["30-Day Volatility"] = (volatility_data["30-Day Volatility"] - volatility_data["30-Day Volatility"].min()) / \
                                           (volatility_data["30-Day Volatility"].max() - volatility_data["30-Day Volatility"].min())
    volume_data["Average Volume"] = (volume_data["Average Volume"] - volume_data["Average Volume"].min()) / \
                                     (volume_data["Average Volume"].max() - volume_data["Average Volume"].min())
    institutional_flows_data["FII/DII Ratio"] = (institutional_flows_data["FII/DII Ratio"] - institutional_flows_data["FII/DII Ratio"].min()) / \
                                                (institutional_flows_data["FII/DII Ratio"].max() - institutional_flows_data["FII/DII Ratio"].min())
    market_breadth_data["Advance-Decline Ratio"] = (market_breadth_data["Advance-Decline Ratio"] - market_breadth_data["Advance-Decline Ratio"].min()) / \
                                                   (market_breadth_data["Advance-Decline Ratio"].max() - market_breadth_data["Advance-Decline Ratio"].min())


    # print(volatility_data)
    # print(volume_data)
    # print(institutional_flows_data)
    # print(market_breadth_data)
    # Weighted scoring system
    weights = {
        "volatility": 0.4,
        "volume": 0.2,
        "institutional_flows": 0.2,
        "market_breadth": 0.2
    }

    # Calculate scores
    latest_volatility = volatility_data["30-Day Volatility"].iloc[-1]
    latest_volume = volume_data["Average Volume"].iloc[-1]
    latest_institutional_flows = institutional_flows_data["FII/DII Ratio"].iloc[-1]
    latest_market_breadth = market_breadth_data["Advance-Decline Ratio"].iloc[-1]

    score = (
        weights["volatility"] * (1 - latest_volatility) + 
        weights["volume"] * latest_volume * 0.8 +
        weights["institutional_flows"] * latest_institutional_flows * 0.7 +
        weights["market_breadth"] * latest_market_breadth * 0.6
    )

    # Adjust cash allocation based on risk tolerance
    if risk_tolerance == "high":
        cash_allocation = max(0, 20 - score * 20)  # Lower cash allocation for high risk tolerance
    elif risk_tolerance == "medium":
        cash_allocation = max(0, 30 - score * 30)  # Moderate cash allocation for medium risk tolerance
    elif risk_tolerance == "low":
        cash_allocation = max(0, 50 - score * 50)  # Higher cash allocation for low risk tolerance
    else:
        raise ValueError("Invalid risk tolerance. Choose from 'high', 'medium', or 'low'.")

    # Visualization
    metrics = ["Volatility", "Volume", "Institutional Flows", "Market Breadth"]
    values = [latest_volatility, latest_volume, latest_institutional_flows, latest_market_breadth]
    plt.figure(figsize=(10, 6))
    plt.bar(metrics, values, color=["blue", "green", "orange", "purple"])
    plt.title(f"Liquidity Metrics and Cash Allocation (Risk Tolerance: {risk_tolerance.capitalize()})")
    plt.ylabel("Normalized Score")
    plt.grid(axis="y")
    plt.tight_layout()
    plt.savefig("../screenshots/cash_allocation_metrics.png")
    plt.close()

    return cash_allocation

# Example Usage
def main():
    # File paths
    volatility_file = "../data_collections/nifty_volatility.csv"
    volume_file = "../data_collections/nifty_volume.csv"
    institutional_flows_file = "../data_collections/institutional_flows.csv"
    market_breadth_file = "../data_collections/market_breadth.csv"

    # Calculate cash allocation for different risk tolerances
    for risk_tolerance in ["high", "medium", "low"]:
        cash_allocation = calculate_cash_allocation(
            volatility_file, volume_file, institutional_flows_file, market_breadth_file, risk_tolerance
        )
        print(f"Recommended Cash Allocation ({risk_tolerance.capitalize()} Risk): {cash_allocation:.2f}%")

if __name__ == "__main__":
    main()