"""
    Parse data from the Alphavantage API

    Author: Josh Mackie (joshjb87@gmail.com)
    Last Revised: 02/15/2025
"""
import os
import requests
import json
import statistics
import matplotlib.pyplot as plt

url = "https://www.alphavantage.co/query"

ALPHA_APIKEY= os.getenv("ALPHA_APIKEY")

params = {
    "function": "TIME_SERIES_INTRADAY",
    "symbol": "DIS",
    "interval": "5min",
    "outputsize": "full",
    "apikey": f"{ALPHA_APIKEY}"
}

response = requests.get(url, params=params)

# Check to see if there is a HTTP 200 response
if response.status_code == 200:
    data = response.json()
    print(json.dumps(data, indent=4))
else:
    print(f"Error fetching data: {response.status_code}")

# Get today's latest date from the metadata
latest_full = data["Meta Data"]["3. Last Refreshed"]
latest_date = latest_full.split()[0]

high_prices = []
low_prices = []
close_prices = []

# Loop through the time series records for today's date (latest_date)
time_series = data["Time Series (5min)"]
for timestamp, record in time_series.items():
    record_date = timestamp.split()[0]
    if record_date == latest_date:
        high_prices.append(float(record["2. high"]))
        low_prices.append(float(record["3. low"]))
        close_prices.append(float(record["4. close"]))

# Since the data is in reverse-chronological order, reverse the lists so they display chronologically
high_prices.reverse()
low_prices.reverse()
close_prices.reverse()

# Calculate the summary statistics, and handle potential for missing data
max_high = max(high_prices) if high_prices else None
min_low = min(low_prices) if low_prices else None
stdev_close = statistics.stdev(close_prices) if len(close_prices) > 1 else None

# Output the results
print("Date:", latest_date)
print("Max High Price:", max_high)
print("Min Low Price:", min_low)
print("Standard Deviation of Close Prices:", stdev_close)

# Plotting the Close Prices with some experimentation with display settings
ticker = params['symbol']

plt.figure(figsize=(10, 5))
plt.plot(close_prices, linestyle='-', color='b', markersize=5)
plt.title(f"Close Prices on {latest_date} for {ticker}", fontsize=14)
plt.xlabel("Record Number (chronological)", fontsize=12)
plt.ylabel("Close Price", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()

plt.savefig(f'{ticker}.png')
print(f"Plot saved as {ticker}.png")