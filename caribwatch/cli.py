#!/usr/bin/env python3
"""
CaribWatch CLI v0.2 — Caribbean-Specific Threat Visibility Tool
TrinTech Digital Defense
"""

import argparse
import sys
import time
from datetime import datetime

from . import __version__
from .config import load_config, save_config, ensure_data_dir
from .collector import collect_network_observations, privilege_check
from .intel import match_indicators, update_intel
from .alerter import alert_findings
from .report import generate_report
from .db import (
    init_db, record_scan, get_last_scan, get_recent_findings,
    cleanup_old_findings, log_authorization
)


def cmd_init(args):
    ensure_data_dir()
    init_db()
    cfg = load_config()
    if args.org:
        cfg["organization_name"] = args.org
    if args.auth_ref:
        cfg["authorization_ref"] = args.auth_ref
    save_config(cfg)
    log_authorization("init", cfg.get("authorization_ref", ""), "CaribWatch initialized")
    print("[+] CaribWatch v0.2 initialized.")
    print(f"    Data directory : {cfg['data_dir']}")
    if cfg.get("organization_name"):
        print(f"    Organization   : {cfg['organization_name']}")
    if cfg.get("authorization_ref"):
        print(f"    Auth reference : {cfg['authorization_ref']}")
    print("    Next: caribwatch update-intel")


def cmd_update_intel(_args):
    msg = update_intel()
    print(f"[+] {msg}")


def cmd_scan(args):
    cfg = load_config()
    auth_ref = cfg.get("authorization_ref", "")
    if not auth_ref and not args.force:
        print("[!] No authorization_ref set in config. Use --force to override or set it via init/config.")
        print("    Example: caribwatch init --auth-ref ROE-2026-001")
        return

    print("[*] Privilege check...")
    priv = privilege_check()
    print(f"    {priv['note']}")

    print("[*] Collecting network observations...")
    max_obs = int(cfg.get("max_observations_per_scan", 5000))
    observations = collect_network_observations(max_observations=max_obs)
    print(f"    Observed {len(observations)} unique network indicators")

    print("[*] Matching against threat intel...")
    suppress_private = cfg.get("suppress_private_ips", True)
    matches = match_indicators(observations, suppress_private=suppress_private)

    if matches:
        print(f"[!] {len(matches)} potential match(es) found")
        alert_findings(matches)
    else:
        print("[+] No matching indicators found")

    record_scan(len(matches), observations_count=len(observations),
                authorization_ref=auth_ref)
    log_authorization("scan", auth_ref, f"findings={len(matches)} observations={len(observations)}")
    print("[+] Scan complete")


def cmd_monitor(args):
    cfg = load_config()
    auth_ref = cfg.get("authorization_ref", "")
    if not auth_ref and not args.force:
        print("[!] No authorization_ref set. Use --force or set via init.")
        return

    interval = args.interval or cfg.get("scan_interval_seconds", 300)
    print(f"[*] Continuous monitor started (interval: {interval}s). Ctrl+C to stop.")
    print(f"    Authorization : {auth_ref or 'NONE (forced)'}")
    print("    Authorized defensive monitoring only.\n")

    log_authorization("monitor_start", auth_ref, f"interval={interval}")

    try:
        while True:
            ts = datetime.utcnow().strftime("%H:%M:%S")
            print(f"[{ts}] Scanning...")
            observations = collect_network_observations(
                max_observations=int(cfg.get("max_observations_per_scan", 5000))
            )
            matches = match_indicators(
                observations,
                suppress_private=cfg.get("suppress_private_ips", True)
            )
            if matches:
                alert_findings(matches)
            record_scan(len(matches), observations_count=len(observations),
                        authorization_ref=auth_ref)
            time.sleep(interval)
    except KeyboardInterrupt:
        log_authorization("monitor_stop", auth_ref, "user interrupt")
        print("\n[*] Monitor stopped.")


def cmd_report(args):
    hours = 24 if args.daily else (args.hours or 24)
    client_mode = args.client or load_config().get("client_report_mode", False)
    report = generate_report(hours=hours, client_mode=client_mode)
    print(report)


def cmd_status(_args):
    last = get_last_scan()
    recent = get_recent_findings(hours=24)
    cfg = load_config()
    priv = privilege_check()

    print("CaribWatch Status")
    print("=" * 50)
    print(f"Version           : {__version__}")
    print(f"Data directory    : {cfg['data_dir']}")
    print(f"Organization      : {cfg.get('organization_name') or '(not set)'}")
    print(f"Authorization Ref : {cfg.get('authorization_ref') or '(not set)'}")
    if last:
        print(f"Last scan         : {last.get('timestamp')} "
              f"({last.get('findings_count')} findings / {last.get('observations_count', 0)} obs)")
    else:
        print("Last scan         : never")
    print(f"Findings (24h)    : {len(recent)}")
    print(f"Alert threshold   : {cfg.get('alert_threshold')}")
    print(f"Cooldown (sec)    : {cfg.get('alert_cooldown_seconds')}")
    print(f"Webhook           : {'configured' if cfg.get('webhook_url') else 'none'}")
    print(f"Visibility        : {priv['note']}")


def cmd_cleanup(args):
    cfg = load_config()
    days = args.days or cfg.get("max_findings_retention_days", 30)
    deleted = cleanup_old_findings(days=days)
    print(f"[+] Removed {deleted} findings older than {days} days")


def main():
    parser = argparse.ArgumentParser(
        description="CaribWatch v0.2 — Caribbean-Specific Threat Visibility Tool by TrinTech Digital Defense",
        epilog="Authorized use only. Obtain written permission before monitoring any network you do not own.",
    )
    parser.add_argument("--version", action="version", version=f"CaribWatch {__version__}")

    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Initialize data directory and config")
    p_init.add_argument("--org", help="Organization / client name")
    p_init.add_argument("--auth-ref", help="Authorization / ROE reference")
    p_init.set_defaults(func=cmd_init)

    p_intel = sub.add_parser("update-intel", help="Refresh local threat indicators")
    p_intel.set_defaults(func=cmd_update_intel)

    p_scan = sub.add_parser("scan", help="Run a one-shot network visibility scan")
    p_scan.add_argument("--force", action="store_true", help="Run even without authorization_ref")
    p_scan.set_defaults(func=cmd_scan)

    p_mon = sub.add_parser("monitor", help="Run continuous monitoring")
    p_mon.add_argument("--interval", type=int, help="Seconds between scans")
    p_mon.add_argument("--force", action="store_true", help="Run even without authorization_ref")
    p_mon.set_defaults(func=cmd_monitor)

    p_rep = sub.add_parser("report", help="Generate summary report")
    p_rep.add_argument("--daily", action="store_true", help="Last 24 hours")
    p_rep.add_argument("--hours", type=int, help="Custom lookback window")
    p_rep.add_argument("--client", action="store_true", help="Client-facing report format")
    p_rep.set_defaults(func=cmd_report)

    p_stat = sub.add_parser("status", help="Show current status")
    p_stat.set_defaults(func=cmd_status)

    p_clean = sub.add_parser("cleanup", help="Remove old findings")
    p_clean.add_argument("--days", type=int, help="Retention days")
    p_clean.set_defaults(func=cmd_cleanup)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
