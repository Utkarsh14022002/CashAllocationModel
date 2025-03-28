# 💸 Cash Allocation Model 🚀
```
This project aims to develop a robust cash allocation model using financial data and various feature engineering techniques. The model leverages data from multiple sources like NSE, RBI, and SEBI to compute metrics such as market volatility, traded volume, institutional flow, market breadth, and interest rates. These metrics are then used to analyze market conditions and make informed decisions on cash allocation.
```

# 🗂️ Project Structure
The project consists of three main components:

# 📊 Data Collection (dataCollection.py)
Collects data from sources like NSE, RBI, and SEBI. 

# 🔧 Feature Engineering (featureEngineering.py)
Computes financial metrics from the collected data.

# 💡 Cash Allocation Model (cashAllocationModel.py)
Uses the engineered features to determine optimal cash allocation.

# ⚙️ Installation
📝 Prerequisites
Python 3.8+
pip (Python package installer)

🛠️ Installation Steps
Clone the repository:

```
git clone https://github.com/yourusername/cash-allocation-model.git
```



## Install the required packages:

```
pip install -r requirements.txt
```


# 🚀 Usage
## 🗃️ Data Collection:
To collect data, run the dataCollection.py script:

```
python dataCollection.py
```

This script fetches data from NSE, RBI, and SEBI and saves it in the data_collections/ directory.

## ✨ Feature Engineering
To generate features from the collected data, run the featureEngineering.py script:

```
python featureEngineering.py
```
This script computes metrics like volatility, traded volume, institutional flows, market breadth, and interest rates. The processed data is saved in the data_collections/ directory.

## 💰 Cash Allocation
To execute the cash allocation model, run:

```
python cashAllocationModel.py
```
This script analyzes the generated features to determine the optimal cash allocation strategy.

🌟 Features
📈 1. Market Volatility Metrics
Calculates 30-day rolling volatility and volatility ratios between Nifty 50 and Nifty Midcap 100.

📊 2. Traded Volume Metrics
Calculates the 30-day rolling average of traded volume for Nifty 50 and Nifty Midcap 100.

💸 3. Institutional Flow Metrics
Calculates net flows for FIIs and DIIs, along with the FII/DII ratio.

📅 4. Market Breadth Indicators
Calculates the Advance-Decline ratio for Nifty 50 to assess market sentiment.

💼 5. Interest Rate Metrics
Extracts policy and reverse repo rates from RBI data.

# 📝 Output
~~~
The scripts generate several output files, including:

Nifty and Midcap Volatility: nifty_volatility.csv, midcap_volatility.csv

Traded Volume: nifty_volume.csv, midcap_volume.csv

Institutional Flows: institutional_flows.csv

Market Breadth: market_breadth.csv

Interest Rates: interest_rates.csv

Additionally, plots for various metrics are stored in the screenshots/ directory.
~~~


# 📜 License
This project is licensed under the MIT License. See LICENSE for more details.

# 🙏 Acknowledgements
Special thanks to NSE, RBI, and SEBI for providing the financial data used in this project.