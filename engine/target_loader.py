"""engine/target_loader.py — Ingests and standardizes target endpoints."""

import os
import pandas as pd
from config import Config


class TargetLoader:
    """Loads and validates monitoring target URLs from CSV/Excel."""

    def __init__(self, filepath=Config.TARGETS_FILE):
        self.filepath = filepath

    def load_targets(self):
        print(f"\n📂 Loading targets from: {self.filepath}")

        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"Targets file not found: {self.filepath}")

        ext = os.path.splitext(self.filepath)[1].lower()
        if ext == ".csv":
            df = pd.read_csv(self.filepath)
        elif ext in (".xlsx", ".xls"):
            df = pd.read_excel(self.filepath, engine="openpyxl")
        else:
            raise ValueError(f"Unsupported format: {ext}")

        df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]

        targets = []
        for _, row in df.iterrows():
            url = str(row.get("url", "")).strip()
            if not url:
                continue

            if not url.startswith("http://") and not url.startswith("https://"):
                url = "https://" + url

            targets.append({
                "name": str(row.get("name", url)).strip(),
                "url": url,
                "category": str(row.get("category", "Web Service")).strip(),
                "expected_status": int(row.get("expected_status", 200)),
            })

        print(f"   ✅ Successfully loaded {len(targets)} endpoints to monitor")
        return targets