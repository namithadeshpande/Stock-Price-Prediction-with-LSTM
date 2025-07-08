#!/usr/bin/env python3

import os
import pandas as pd
import yfinance as yf
import pandas_market_calendars as mcal
from datetime import datetime, timedelta

# --- Config ---
CSV_PATH = "spy_yahoo_daily_data.csv"
TICKER = "SPY"
START_DATE = "2000-01-01"
COLUMNS = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']

# --- Check if market is open today ---
today = datetime.today().date()
nyse = mcal.get_calendar("NYSE")
if nyse.schedule(start_date=str(today), end_date=str(today)).empty:
    print("Market is closed today. Skipping update.")
    exit()

# --- Load existing data ---
if os.path.exists(CSV_PATH) and os.path.getsize(CSV_PATH) > 0:
    try:
        df = pd.read_csv(CSV_PATH)
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df.dropna(subset=['Date'], inplace=True)
        last_date = df['Date'].max().date() if not df.empty else datetime.strptime(START_DATE, "%Y-%m-%d").date()
        print(f"Existing data found. Last date: {last_date}")
    except Exception as e:
        print(f"Error reading CSV: {e}")
        df = pd.DataFrame(columns=COLUMNS)
        last_date = datetime.strptime(START_DATE, "%Y-%m-%d").date()
else:
    df = pd.DataFrame(columns=COLUMNS)
    last_date = datetime.strptime(START_DATE, "%Y-%m-%d").date()
    print("No existing data. Starting from scratch.")

# --- Download new data ---
start_date = last_date + timedelta(days=1)
end_date = today + timedelta(days=1)

if start_date > today:
    print("Data already up to date.")
    exit()

df_new = yf.download(TICKER, start=start_date, end=end_date)

if df_new is None or df_new.empty:
    print("No new data fetched.")
    exit()

df_new.reset_index(inplace=True)

# --- Flatten multi-index columns if needed ---
if isinstance(df_new.columns, pd.MultiIndex):
    df_new.columns = [col[0] for col in df_new.columns]

# --- Keep only expected columns ---
df_new = df_new[COLUMNS]
df_new['Date'] = pd.to_datetime(df_new['Date'])

# --- Combine and save ---
df_all = pd.concat([df, df_new], ignore_index=True)
df_all.drop_duplicates(subset='Date', keep='last', inplace=True)
df_all.sort_values('Date', inplace=True)
df_all.to_csv(CSV_PATH, index=False)

last_updated = df_all['Date'].dropna().max()
print(f"CSV updated. Last date in file: {last_updated.date() if pd.notna(last_updated) else 'N/A'}")
