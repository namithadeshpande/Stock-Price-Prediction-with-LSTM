import requests
import pandas as pd
from datetime import datetime
import os

#AlphaVantage API to get Stock Data 
# Get API key from environment variable
MY_KEY = "your_key"
if not MY_KEY:
    print("Error: API key not found. Set the ALPHA_VANTAGE_API_KEY environment variable.")
    exit()

url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&outputsize=full&apikey={MY_KEY}'
r = requests.get(url)

# Check for request errors
if r.status_code != 200:
    print(f"Error: Unable to fetch data. Status code: {r.status_code}")
    exit()

data = r.json()
if "Time Series (Daily)" not in data:
    print("Error: 'Time Series (Daily)' not found in the API response.")
    exit()

# Extract the time series data
time_series = data.get("Time Series (Daily)", {})

# Convert the time series data into a pandas DataFrame
df = pd.DataFrame.from_dict(time_series, orient="index")
df.index.name = "Date"  # Set the index name to "Date"
df.reset_index(inplace=True)  # Reset the index to make "Date" a column

# Rename columns for better readability
df.rename(columns={
    "1. open": "Open",
    "2. high": "High",
    "3. low": "Low",
    "4. close": "Close",
    "5. volume": "Volume",
}, inplace=True)

# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Display the DataFrame
print(df)
print(f"Number of rows: {len(df)}")

# Sort the DataFrame by Date in ascending order
df.sort_values(by="Date", inplace=True)

# Define the CSV file path
csv_file = "daily_SPY_stock_data.csv"

# Check if the CSV file already exists
if os.path.exists(csv_file):
    # Load the existing data
    existing_data = pd.read_csv(csv_file)
    existing_data["Date"] = pd.to_datetime(existing_data["Date"])

    # Append new rows to the existing data
    combined_data = pd.concat([existing_data, df]).drop_duplicates(subset="Date").sort_values(by="Date")
else:
    # If the file doesn't exist, use the current DataFrame
    combined_data = df

# Save the combined data back to the CSV file
combined_data.to_csv(csv_file, index=False)
print(f"Data saved to {csv_file}")
