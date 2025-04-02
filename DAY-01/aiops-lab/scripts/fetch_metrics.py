# Copyright (c) 2025 Rajinikanth Vadla
# All rights reserved.

import requests
import pandas as pd
import time
import os
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
PROM_URL = config['monitoring']['prometheus_url']
QUERY = config['monitoring']['query']

def fetch_historical(hours=1):
    try:
        if not os.path.exists('config.ini'):
            raise FileNotFoundError("config.ini not found")
            
        end = int(time.time())
        start = end - hours * 3600
        
        response = requests.get(
            f"{PROM_URL}/api/v1/query_range",
            params={
                "query": QUERY,
                "start": start,
                "end": end,
                "step": "60s"
            },
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        if not data["data"]["result"]:
            raise ValueError("No data received - check node_exporter connection")
            
        points = data["data"]["result"][0]["values"]
        df = pd.DataFrame(points, columns=["timestamp", "cpu_usage"])
        df["cpu_usage"] = df["cpu_usage"].astype(float)
        df.to_csv("cpu_metrics.csv", index=False)
        print(f"✅ Saved {len(df)} metrics to cpu_metrics.csv")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Network Error: {str(e)}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    fetch_historical(hours=6)