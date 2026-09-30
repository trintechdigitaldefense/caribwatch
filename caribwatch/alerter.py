import json
from typing import List, Dict, Any

try:
    from rich.console import Console
    from rich.table import Table
    console = Console()
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    console = None

import requests

from .config import load_config
from .db import add_finding, is_in_cooldown, set_cooldown


def severity_rank(sev: str) -> int:
    return {"low": 1, "medium": 2, "high": 3}.get(sev.lower(), 0)


def should_alert(severity: str, threshold: str) -> bool:
    return severity_rank(severity) >= severity_rank(threshold)


def alert_findings(findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Apply threshold, cooldown, persist, and alert.
    Returns the list of findings that actually triggered an alert.
    """
    cfg = load_config()
    threshold = cfg.get("alert_threshold", "medium")
    cooldown = int(cfg.get("alert_cooldown_seconds", 3600))

    actionable = []
    for f in findings:
        if not should_alert(f.get("severity", "low"), threshold):
            continue
        ind = f.get("indicator", "")
        if is_in_cooldown(ind, cooldown):
            continue
        actionable.append(f)

    if not actionable:
        return []

    for f in actionable:
        is_new = add_finding(
            indicator=f["indicator"],
            indicator_type=f["indicator_type"],
            severity=f["severity"],
            description=f.get("description", ""),
            source=f.get("source", "caribwatch"),
            raw_data=f,
        )
        set_cooldown(f["indicator"])

    # Console output
    if cfg.get("enable_console_alerts", True):
        if RICH_AVAILABLE:
            table = Table(title="CaribWatch Alerts", show_header=True, header_style="bold red")
            table.add_column("Severity", width=8)
            table.add_column("Type", width=12)
            table.add_column("Indicator", width=28)
            table.add_column("Description", width=40)
            for f in actionable:
                sev = f.get("severity", "").upper()
                color = {"HIGH": "red", "MEDIUM": "yellow", "LOW": "green"}.get(sev, "white")
                table.add_row(
                    f"[{color}]{sev}[/{color}]",
                    f.get("indicator_type", ""),
                    f.get("indicator", "")[:28],
                    (f.get("description", "") or "")[:40],
                )
            console.print(table)
        else:
            print("\n=== CaribWatch Alerts ===")
            for f in actionable:
                print(f"[{f.get('severity', '').upper()}] {f.get('indicator_type')}: "
                      f"{f.get('indicator')} - {f.get('description', '')}")

    # Optional webhook
    webhook = cfg.get("webhook_url")
    if webhook:
        try:
            payload = {
                "source": "CaribWatch",
                "version": "0.2.0",
                "findings_count": len(actionable),
                "findings": actionable,
            }
            requests.post(webhook, json=payload, timeout=8)
        except Exception as e:
            print(f"[!] Webhook failed: {e}")

    return actionable
