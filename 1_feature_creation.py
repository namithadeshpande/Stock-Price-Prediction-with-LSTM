import pandas as pd
import numpy as np
from ta.volatility import AverageTrueRange, BollingerBands
from datetime import datetime
from ta.trend import MACD
from ta.momentum import RSIIndicator

csv_file = "spy_yf_daily_data.csv"

START_DATE = '2001-01-01'
END_DATE = '2025-06-30'

# Load the CSV file
stock_pd = pd.read_csv(csv_file, parse_dates=['Date'], index_col='Date')
stock_pd = stock_pd[(stock_pd.index >= START_DATE) & (stock_pd.index <= END_DATE)]

stock_pd = stock_pd.sort_index()

#Additional features for LSTM
# --- Momentum Indicators ---
# Daily % change in closing price (momentum)
stock_pd['returns'] = stock_pd['Close'].pct_change()

# Logarithmic daily returns
stock_pd['log_returns'] = np.log(stock_pd['Close'] / stock_pd['Close'].shift(1))

# RSI (14-day) - 14-day Relative Strength Index (measures overbought/oversold conditions)
stock_pd['rsi_14'] = RSIIndicator(close=stock_pd['Close'], window=14).rsi()

# MACD 
macd = MACD(close=stock_pd['Close'])
stock_pd['macd'] = macd.macd() # MACD line = 12-EMA minus 26-EMA
stock_pd['macd_signal'] = macd.macd_signal() # Signal line = 9-EMA of MACD line
stock_pd['macd_diff'] = macd.macd_diff() # MACD histogram = MACD - Signal

# --- Trend Indicators ---
# 10-day Simple Moving Average (short-term trend) & 50-day Simple Moving Average (medium-term trend)
stock_pd['ma_10'] = stock_pd['Close'].rolling(window=10).mean()
stock_pd['ma_50'] = stock_pd['Close'].rolling(window=50).mean()
# 10-day Exponential Moving Average (faster trend) & 20-day EMA (used in MACD and trend analysis)
stock_pd['ema_10'] = stock_pd['Close'].ewm(span=10).mean()
stock_pd['ema_20'] = stock_pd['Close'].ewm(span=20).mean()

# Price-to-MA ratio
# Price relative to 20-day moving average (trend distance)
stock_pd['price_ma_ratio'] = stock_pd['Close'] / stock_pd['ma_20']

# --- Volatility Indicators ---
# 14-day rolling standard deviation of close (price volatility)
stock_pd['rolling_std_14'] = stock_pd['Close'].rolling(window=14).std()

atr = AverageTrueRange(high=stock_pd['High'], low=stock_pd['Low'], close=stock_pd['Close'], window=14)
stock_pd['atr_14'] = atr.average_true_range() # Average True Range (14 days) - price range volatility

bb = BollingerBands(close=stock_pd['Close'], window=20, window_dev=2)
stock_pd['bb_upper'] = bb.bollinger_hband() # Upper Bollinger Band (mean + 2*std)
stock_pd['bb_lower'] = bb.bollinger_lband() # Lower Bollinger Band (mean - 2*std)
stock_pd['bb_width'] = stock_pd['bb_upper'] - stock_pd['bb_lower'] # Band width (volatility indicator)

# --- Lag Features ---
# Close, return, volume lagged by {lag} days
lags = [1, 2, 3]
for lag in lags:
    stock_pd[f'close_lag_{lag}'] = stock_pd['Close'].shift(lag)
    stock_pd[f'return_lag_{lag}'] = stock_pd['returns'].shift(lag)
    stock_pd[f'volume_lag_{lag}'] = stock_pd['Volume'].shift(lag)

# --- Datetime Features ---
stock_pd['day_of_week'] = stock_pd.index.dayofweek  # 0 = Monday
stock_pd['week_of_year'] = stock_pd.index.isocalendar().week
stock_pd['month'] = stock_pd.index.month
stock_pd['quarter'] = stock_pd.index.quarter
stock_pd['is_month_end'] = stock_pd.index.is_month_end.astype(int)
stock_pd['is_quarter_end'] = stock_pd.index.is_quarter_end.astype(int)

stock_pd.dropna(inplace=True)
stock_pd.to_csv('yf_data_new_features.csv')  