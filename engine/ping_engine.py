"""engine/ping_engine.py — Executes high-precision HTTP health probes."""

import time
import requests
from datetime import datetime
from config import Config


class PingEngine:
    """Probes URLs, checks status codes, measures latency, and handles network errors."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "EnterpriseUptimeBot/1.0 (HealthCheckMonitor)",
            "Accept": "*/*",
        })

    def probe(self, target):
        """
        Executes a health check against a target URL.

        Returns:
            dict containing status, latency_ms, status_code, health_label, timestamp
        """
        url = target["url"]
        expected_status = target.get("expected_status", 200)

        result = {
            "name": target["name"],
            "url": url,
            "category": target["category"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status_code": 0,
            "latency_ms": 0.0,
            "is_up": False,
            "health_label": "DOWN",
            "error_reason": "",
        }

        start_time = time.perf_counter()

        try:
            response = self.session.get(
                url,
                timeout=Config.TIMEOUT_SECONDS,
                allow_redirects=True,
            )
            elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)

            result["status_code"] = response.status_code
            result["latency_ms"] = elapsed_ms

            if response.status_code == expected_status or (200 <= response.status_code < 300):
                result["is_up"] = True
                if elapsed_ms > Config.LATENCY_THRESHOLD_MS:
                    result["health_label"] = "DEGRADED (Slow)"
                else:
                    result["health_label"] = "HEALTHY"
            else:
                result["is_up"] = False
                result["health_label"] = f"ERROR ({response.status_code})"
                result["error_reason"] = f"Unexpected HTTP status: {response.status_code}"

        except requests.exceptions.Timeout:
            result["is_up"] = False
            result["health_label"] = "TIMEOUT"
            result["error_reason"] = f"Server exceeded {Config.TIMEOUT_SECONDS}s timeout limit"

        except requests.exceptions.SSLError:
            result["is_up"] = False
            result["health_label"] = "SSL_ERROR"
            result["error_reason"] = "Invalid or expired SSL/TLS certificate"

        except requests.exceptions.ConnectionError:
            result["is_up"] = False
            result["health_label"] = "UNREACHABLE"
            result["error_reason"] = "DNS resolution failed or host refused connection"

        except Exception as e:
            result["is_up"] = False
            result["health_label"] = "FAILED"
            result["error_reason"] = str(e)

        return result