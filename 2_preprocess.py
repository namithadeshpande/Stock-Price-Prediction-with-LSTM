import pandas as pd
import numpy as np
from datetime import datetime
import shap
from sklearn.ensemble import RandomForestRegressor

csv_file = "yf_data_new_features.csv"

START_DATE = '2001-01-01'
END_DATE = '2025-06-30'

# Load the CSV file
feat_df = pd.read_csv(csv_file, parse_dates=['Date'], index_col='Date')
feat_df = feat_df[(feat_df.index >= START_DATE) & (feat_df.index <= END_DATE)]

feat_df = feat_df.sort_index()

# Define target and features
target = feat_df['Close']
features = feat_df.drop(columns=['Close'])

# Sample a smaller subset of data for SHAP computations
sample_size = 1000  
sampled_features = features.sample(n=sample_size, random_state=42)
sampled_target = target.loc[sampled_features.index]

# Train a Random Forest model
model = RandomForestRegressor()
model.fit(features, target)

# Initialize SHAP explainer
explainer = shap.TreeExplainer(model)

# Compute SHAP values
shap_values = explainer.shap_values(features)

# Visualize feature importance
shap.summary_plot(shap_values, features)

# Get mean absolute SHAP values for feature importance
shap_importance = np.abs(shap_values).mean(axis=0)
feature_importance = pd.Series(shap_importance, index=features.columns).sort_values(ascending=False)
print("Feature Importance:\n", feature_importance)

# Select top features (e.g., top 10)
selected_features = feature_importance.head(20).index.tolist()
print("Selected Features:\n", selected_features)

# Add the target column to the selected features
final_features = selected_features + ['Close']

# Filter the dataset to include only the selected features and target
final_data = feat_df[final_features]

# Save the final dataset to a new CSV file
final_data.to_csv("yf_data_feature_reduce.csv", index=True)

