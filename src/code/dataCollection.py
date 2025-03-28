import os
import pandas as pd
import yfinance as yf
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from io import StringIO

# Ensure the output directory exists
OUTPUT_DIR = "../data_collections"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_nifty_data():
    """Fetch Nifty 50, Midcap 100, Next 50, and India VIX data using yfinance."""
    tickers = {
        "Nifty 50": "^NSEI",
        "Nifty Midcap 100": "^NSEMDCP50",
        "Nifty Next 50": "^NSMIDCP",
        "INDIA VIX": "^INDIAVIX"
    }

    for name, ticker in tickers.items():
        try:
            data = None
            if name == "INDIA VIX":
                data = yf.download("^INDIAVIX", period="3y", interval="1d")
            else:
                data = yf.download(ticker, start="2022-02-01", end="2025-02-01", interval="1d")
            if data.empty:
                continue
            file_path = os.path.join(OUTPUT_DIR, f"{name.replace(' ', '_').lower()}_data.csv")
            data.to_csv(file_path)
            print(f"{name} data downloaded successfully to {file_path}.")
        except Exception as e:
            print(f"Error fetching data for {name}: {e}")


def scrape_fii_dii_data():
    """Scrape FII/DII data from NiftyTrader using Selenium."""
    url = "https://www.niftytrader.in/fii-dii-data"

    # Set up Selenium WebDriver
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        time.sleep(5)  # Wait for JavaScript to load the table

        # Find the FII/DII data table
        table = driver.find_element(By.TAG_NAME, "table")
        html = table.get_attribute("outerHTML")

        # Convert HTML table to Pandas DataFrame
        df = pd.read_html(html)[0]
        file_path = os.path.join(OUTPUT_DIR, "fii_dii_data.csv")
        df.to_csv(file_path, index=False)

        print(f"FII/DII data scraped successfully to {file_path}.")

    except Exception as e:
        print(f"Error scraping FII/DII data: {e}")
    
    finally:
        driver.quit()


def scrape_rbi_policy_rates():
    """Scrape policy rates & monetary operations from RBI website."""
    url = "https://rbi.org.in/"

    # Set up Selenium WebDriver
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        time.sleep(5)  # Wait for JavaScript content to load

        # Find tables on the page
        tables = driver.find_elements(By.TAG_NAME, "table")
        if not tables:
            print("❌ Error: No tables found on the page.")
            return

        # Extract the first table's HTML content
        html = tables[0].get_attribute("outerHTML")
        df = pd.read_html(StringIO(html))[0]
        file_path = os.path.join(OUTPUT_DIR, "rbi_policy_rates.csv")
        df.to_csv(file_path, index=False)

        print(f"✅ RBI policy rates data scraped successfully to {file_path}.")

    except Exception as e:
        print(f"❌ Error scraping RBI data: {e}")

    finally:
        driver.quit()


def scrape_sebi_pms_data():
    """Scrape mutual fund & PMS cash holdings data from SEBI website."""
    url = "https://www.sebi.gov.in/sebiweb/other/OtherAction.do?doMfd=yes&type=1"

    # Set up Selenium WebDriver
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        time.sleep(5)  # Allow JavaScript to load content

        # Find the first table on the page (adjust as needed)
        tables = driver.find_elements(By.TAG_NAME, "table")
        if not tables:
            print("❌ Error: No tables found on the SEBI page.")
            return

        html = tables[0].get_attribute("outerHTML")
        df = pd.read_html(html)[0]  # Convert HTML table to DataFrame

        # Remove the last row
        df = df.iloc[:-1]

        # Remove the last column
        df = df.iloc[:, :-1]

        # Save the cleaned data to a CSV file
        file_path = os.path.join(OUTPUT_DIR, "sebi_pms_data.csv")
        df.to_csv(file_path, index=False)

        print(f"✅ SEBI PMS & mutual fund data scraped and cleaned successfully to {file_path}.")

    except Exception as e:
        print(f"❌ Error scraping SEBI data: {e}")

    finally:
        driver.quit()


def main():
    fetch_nifty_data()
    scrape_fii_dii_data()
    scrape_rbi_policy_rates()
    scrape_sebi_pms_data()


if __name__ == "__main__":
    main()