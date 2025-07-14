import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor

csv_file = "yf_data_new_features.csv"

START_DATE = '2001-01-01'
END_DATE = '2025-06-30'

# Load the CSV file
feat_df = pd.read_csv(csv_file, parse_dates=['Date'], index_col='Date')
feat_df = feat_df[(feat_df.index >= START_DATE) & (feat_df.index <= END_DATE)]

feat_df = feat_df.sort_index()

