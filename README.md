# 🔍 Enterprise Website & API Uptime Monitor

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Engine: Requests](https://img.shields.io/badge/Engine-Requests-orange.svg)]()
[![Export: OpenPyXL](https://img.shields.io/badge/Export-OpenPyXL-green.svg)]()

A lightweight, production-ready website availability and API health monitor built with Python. Tracks millisecond latency, HTTP status codes, and server response metrics across dozens of targets, exporting color-coded executive Excel SLA audit sheets on demand.

---

## 🌟 Key Features

- **⚡ High-Precision Latency Tracking:** Uses high-resolution performance counters (`time.perf_counter`) to measure response times to 2 decimal places.
- **🛡️ Root-Cause Outage Detection:** Differentiates between 500 Server Errors, 404 Missing Routes, 403 Access Denied, SSL Handshake Failures, and DNS Resolution Timeouts.
- **📊 Color-Coded Excel Health Audits:** Generates automated executive spreadsheets with color-coded health indicators (🟢 Healthy, 🟡 Degraded, 🔴 Down).
- **🔄 Single Audit & Continuous Loop Modes:** Can run as a single-pass CLI health check or an automated continuous background daemon.

---

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/your-username/uptime-health-monitor.git
cd uptime-health-monitor

# 2. Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run single audit
python main.py

# 5. Or run continuous monitoring (every 30 seconds)
python main.py --loop --interval 30