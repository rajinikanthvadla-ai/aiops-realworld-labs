# Copyright (c) 2025 Rajinikanth Vadla
# All rights reserved.

import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os

def train_model():
    try:
        if not os.path.exists("cpu_metrics.csv"):
            raise FileNotFoundError("cpu_metrics.csv not found - run fetch_metrics.py first")
            
        df = pd.read_csv("cpu_metrics.csv")
        if len(df) < 10:
            raise ValueError("Not enough data points (minimum 10 required)")
            
        if df["cpu_usage"].isnull().any():
            raise ValueError("Missing values in CPU usage data")
            
        model = IsolationForest(
            contamination=0.05,
            random_state=42,
            n_estimators=100,
            max_samples='auto'
        )
        model.fit(df["cpu_usage"].values.reshape(-1, 1))
        
        joblib.dump(model, "aiops_model.joblib")
        print("✅ Model trained and saved as aiops_model.joblib")
        
    except Exception as e:
        print(f"❌ Training failed: {str(e)}")

if __name__ == "__main__":
    train_model()