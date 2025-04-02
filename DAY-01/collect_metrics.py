# collect_metrics.py
from prometheus_client import start_http_server, Gauge
import time, random

cpu_usage = Gauge('cpu_usage_percent', 'Simulated CPU Usage')

if __name__ == '__main__':
    start_http_server(8000)
    while True:
        cpu_usage.set(random.uniform(10, 30))  # Normal: 10-30%
        time.sleep(5)
