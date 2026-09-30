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
from .db import add_finding


def severity_rank(sev: str) -> int:
    return {"low": 1, "medium": 2, "high": 3}.get(sev.lower(), 0)


def should_alert(severity: str, threshold: str) -> bool:
    return severity_rank(severity) >= severity_rank(threshold)


def alert_findings(findings: List[Dict[str, Any]]) -> None:
    cfg = load_config()
    threshold = cfg.get("alert_threshold", "medium")

    actionable = [f for f in findings if should_alert(f.get("severity", "low"), threshold)]

    if not actionable:
        return

    # Persist
    for f in actionable:
        add_finding(
            indicator=f["indicator"],
            indicator_type=f["indicator_type"],
            severity=f["severity"],
            description=f.get("description", ""),
            source=f.get("source", "caribwatch"),
            raw_data=f,
        )

    # Console
    if cfg.get("enable_console_alerts", True):
        if RICH_AVAILABLE:
            table = Table(title="CaribWatch Alerts", show_header=True, header_style="bold red")
            table.add_column("Severity")
            table.add_column("Type")
            table.add_column("Indicator")
            table.add_column("Description")
            for f in actionable:
                sev = f.get("severity", "").upper()
                color = {"HIGH": "red", "MEDIUM": "yellow", "LOW": "green"}.get(sev, "white")
                table.add_row(
                    f"[{color}]{sev}[/{color}]",
                    f.get("indicator_type", ""),
                    f.get("indicator", ""),
                    f.get("description", "")[:60],
                )
            console.print(table)
        else:
            print("\n=== CaribWatch Alerts ===")
            for f in actionable:
                print(f"[{f.get('severity', '').upper()}] {f.get('indicator_type')}: {f.get('indicator')} - {f.get('description', '')}")

    # Webhook (optional)
    webhook = cfg.get("webhook_url")
    if webhook:
        try:
            payload = {
                "source": "CaribWatch",
                "findings_count": len(actionable),
                "findings": actionable,
            }
            requests.post(webhook, json=payload, timeout=10)
        except Exception as e:
            print(f"[!] Webhook failed: {e}")
