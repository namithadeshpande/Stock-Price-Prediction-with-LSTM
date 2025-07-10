#WIP
import pandas as pd
from datetime import datetime

csv_file = "spy_yahoo_daily_data.csv"

START_DATE = '2001-01-01'
END_DATE = datetime.today().strftime('%Y-%m-%d')  

# Load the CSV file
stock_pd = pd.read_csv(csv_file, parse_dates=['Date'], index_col='Date')
stock_pd = stock_pd[(stock_pd.index >= START_DATE) & (stock_pd.index <= END_DATE)]

# Display the filtered DataFrame
print(stock_pd.tail())
print(stock_pd.columns.to_list())


