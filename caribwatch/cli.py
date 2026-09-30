#!/usr/bin/env python3
"""
CaribWatch CLI - Caribbean-Specific Threat Visibility Tool
TrinTech Digital Defense
"""

import argparse
import sys
import time
from datetime import datetime

from . import __version__
from .config import load_config, save_config, ensure_data_dir, DEFAULT_CONFIG
from .collector import collect_network_observations
from .intel import match_indicators, update_intel, load_indicators
from .alerter import alert_findings
from .report import generate_report
from .db import init_db, record_scan, get_last_scan, get_recent_findings, cleanup_old_findings


def cmd_init(_args):
    ensure_data_dir()
    init_db()
    cfg = load_config()
    save_config(cfg)
    print("[+] CaribWatch initialized.")
    print(f"    Data directory: {cfg['data_dir']}")
    print("    Run 'caribwatch update-intel' next.")


def cmd_update_intel(_args):
    msg = update_intel()
    print(f"[+] {msg}")


def cmd_scan(_args):
    print("[*] Collecting network observations...")
    observations = collect_network_observations()
    print(f"    Observed {len(observations)} unique network indicators")

    print("[*] Matching against Caribbean threat intel...")
    matches = match_indicators(observations)

    if matches:
        print(f"[!] {len(matches)} potential match(es) found")
        alert_findings(matches)
    else:
        print("[+] No matching indicators found")

    record_scan(len(matches))
    print("[+] Scan complete")


def cmd_monitor(args):
    cfg = load_config()
    interval = args.interval or cfg.get("scan_interval_seconds", 300)
    print(f"[*] Starting continuous monitor (interval: {interval}s). Ctrl+C to stop.")
    print("    Authorized defensive monitoring only.\n")

    try:
        while True:
            print(f"[{datetime.utcnow().strftime('%H:%M:%S')}] Scanning...")
            observations = collect_network_observations()
            matches = match_indicators(observations)
            if matches:
                alert_findings(matches)
            record_scan(len(matches))
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n[*] Monitor stopped.")


def cmd_report(args):
    hours = 24 if args.daily else (args.hours or 24)
    report = generate_report(hours=hours)
    print(report)


def cmd_status(_args):
    last = get_last_scan()
    recent = get_recent_findings(hours=24)
    cfg = load_config()

    print("CaribWatch Status")
    print("=" * 40)
    print(f"Version        : {__version__}")
    print(f"Data directory : {cfg['data_dir']}")
    if last:
        print(f"Last scan      : {last.get('timestamp')} ({last.get('findings_count')} findings)")
    else:
        print("Last scan      : never")
    print(f"Findings (24h) : {len(recent)}")
    print(f"Alert threshold: {cfg.get('alert_threshold')}")
    print(f"Webhook        : {'configured' if cfg.get('webhook_url') else 'none'}")


def main():
    parser = argparse.ArgumentParser(
        description="CaribWatch — Caribbean-Specific Threat Visibility Tool by TrinTech Digital Defense",
        epilog="Authorized use only. See README for details.",
    )
    parser.add_argument("--version", action="version", version=f"CaribWatch {__version__}")

    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Initialize data directory and config")
    p_init.set_defaults(func=cmd_init)

    p_intel = sub.add_parser("update-intel", help="Refresh local threat indicators")
    p_intel.set_defaults(func=cmd_update_intel)

    p_scan = sub.add_parser("scan", help="Run a one-shot network visibility scan")
    p_scan.set_defaults(func=cmd_scan)

    p_mon = sub.add_parser("monitor", help="Run continuous monitoring")
    p_mon.add_argument("--interval", type=int, help="Seconds between scans (default from config)")
    p_mon.set_defaults(func=cmd_monitor)

    p_rep = sub.add_parser("report", help="Generate summary report")
    p_rep.add_argument("--daily", action="store_true", help="Last 24 hours")
    p_rep.add_argument("--hours", type=int, help="Custom lookback window in hours")
    p_rep.set_defaults(func=cmd_report)

    p_stat = sub.add_parser("status", help="Show current status")
    p_stat.set_defaults(func=cmd_status)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
