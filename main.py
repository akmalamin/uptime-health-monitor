"""
main.py — Enterprise Uptime & API Health Monitor.

Usage:
    python main.py                      → Single audit run across all endpoints
    python main.py --loop --interval 30 → Continuous monitoring loop every 30s
"""

import argparse
import time
from config import Config
from engine.target_loader import TargetLoader
from engine.ping_engine import PingEngine
from engine.incident_logger import IncidentLogger


def run_single_audit(targets, engine, logger):
    print(f"\n⚡ Executing health check on {len(targets)} endpoints...\n")
    print(f"{'Target Name':<24} {'Status':<18} {'Latency':<12} {'HTTP Code'}")
    print("-" * 65)

    healthy_count = 0

    for target in targets:
        res = engine.probe(target)
        logger.record(res)

        status_tag = res["health_label"]
        if "HEALTHY" in status_tag:
            healthy_count += 1
            icon = "🟢"
        elif "DEGRADED" in status_tag:
            icon = "🟡"
        else:
            icon = "🔴"

        latency_str = f"{res['latency_ms']} ms" if res['is_up'] else "---"
        code_str = str(res['status_code']) if res['status_code'] != 0 else "FAIL"

        print(f"{target['name'][:22]:<24} {icon} {status_tag:<15} {latency_str:<12} {code_str}")

    print("-" * 65)
    print(f"📊 Summary: {healthy_count}/{len(targets)} endpoints healthy")


def main():
    parser = argparse.ArgumentParser(description="🔍 Enterprise Website Uptime & Health Monitor")
    parser.add_argument("--targets", default=Config.TARGETS_FILE, help="Path to targets CSV")
    parser.add_argument("--loop", action="store_true", help="Run continuous monitoring loop")
    parser.add_argument("--interval", type=int, default=30, help="Seconds between loop checks")
    args = parser.parse_args()

    print("""
╔══════════════════════════════════════════════════════════╗
║   🔍  WEBSITE & API UPTIME MONITOR — Day 109             ║
║   Latency Tracking, HTTP Audits & Incident Reporting     ║
╚══════════════════════════════════════════════════════════╝
    """)

    # 1. Load targets
    loader = TargetLoader(args.targets)
    targets = loader.load_targets()

    if not targets:
        print("❌ No targets found to monitor.")
        return

    engine = PingEngine()
    logger = IncidentLogger()

    if args.loop:
        print(f"\n🔄 Entering continuous monitor loop (Interval: {args.interval}s). Press Ctrl+C to stop.")
        try:
            cycle = 1
            while True:
                print(f"\n[Cycle #{cycle}]")
                run_single_audit(targets, engine, logger)
                cycle += 1
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\n🛑 Monitoring loop stopped by user.")
    else:
        run_single_audit(targets, engine, logger)

    # 2. Export Excel Health Audit Report
    logger.export_excel_report()


if __name__ == "__main__":
    main()