#!/usr/bin/env python3
import os
import pandas as pd
import yfinance as yf
import pandas_market_calendars as mcal
from datetime import datetime, timedelta

# --- Config ---
CSV_PATH = "spy_yahoo_daily_data.csv"
TICKER = "SPY"
START_DATE = "2000-01-01"  # fallback start date for first run

# --- Step 1: Check if market is open today (NYSE) ---
today = datetime.today().date()
nyse = mcal.get_calendar('NYSE')
schedule = nyse.schedule(start_date=str(today), end_date=str(today))

if schedule.empty:
    print("Market is closed today (weekend or holiday). Skipping update.")
    exit()

# --- Step 2: Load existing data or initialize ---
if os.path.exists(CSV_PATH):
    df_existing = pd.read_csv(CSV_PATH, parse_dates=['Date'], index_col='Date')
    last_date = df_existing.index.max().date()
    start_fetch_date = last_date + timedelta(days=1)
    print(f"Existing data found. Last date in file: {last_date}")
else:
    df_existing = pd.DataFrame()
    start_fetch_date = datetime.strptime(START_DATE, "%Y-%m-%d").date()
    print("No existing data found. Creating new CSV from scratch.")

# --- Step 3: Download data from Yahoo Finance ---
today_plus = today + timedelta(days=1)  # end date is exclusive
if start_fetch_date <= today:
    df_new = yf.download(TICKER, start=start_fetch_date, end=today_plus)
    if df_new is None or df_new.empty:
        print("No new data to fetch (possible half-day or data delay).")
        exit()
    else:
        df_new.index.name = 'Date'  
        print(f"Fetched new data from {start_fetch_date} to {today}")

        # --- Step 4: Combine, deduplicate, save ---
        if not df_existing.empty:
            df_combined = pd.concat([df_existing, df_new])
            df_combined = df_combined[~df_combined.index.duplicated(keep='last')]
        else:
            df_combined = df_new

        df_combined = df_combined.reset_index()  
        df_combined.to_csv(CSV_PATH, index=False)
        print(f"CSV updated. Last date in file: {df_combined['Date'].max().date()}")
else:
    print("Data already up to date.")
