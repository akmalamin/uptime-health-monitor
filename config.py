"""config.py — Monitoring settings and thresholds."""

import os


class Config:
    # Health Probe Thresholds
    TIMEOUT_SECONDS = 8           # Max time to wait before marking endpoint DOWN
    LATENCY_THRESHOLD_MS = 1000   # Latency above 1000ms is flagged as DEGRADED (Slow)
    MAX_RETRIES = 2               # Retries before finalizing failure

    # Directories & Paths
    INPUT_DIR = "input"
    OUTPUT_DIR = "output"
    TARGETS_FILE = os.path.join(INPUT_DIR, "targets.csv")


os.makedirs(Config.INPUT_DIR, exist_ok=True)
os.makedirs(Config.OUTPUT_DIR, exist_ok=True)