import requests
import pandas as pd

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
MY_KEY = '3POHM8YSXROCY7DF'
# API_KEY = "DEMO"

url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=SPY&outputsize=full&apikey={MY_KEY}'
r = requests.get(url)
data = r.json()

# Extract the time series data
time_series = data.get("Time Series (Daily)", {})

# Convert the time series data into a pandas DataFrame
df = pd.DataFrame.from_dict(time_series, orient="index")
df.index.name = "Date"  # Set the index name to "Date"
df.reset_index(inplace=True)  # Reset the index to make "Date" a column

# Display the DataFrame
print(df)
print(type(df))
df.count()
