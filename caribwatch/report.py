from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

from .config import ensure_data_dir, load_config
from .db import get_recent_findings, get_last_scan


def generate_report(hours: int = 24) -> str:
    findings = get_recent_findings(hours=hours)
    last_scan = get_last_scan()
    cfg = load_config()

    lines = []
    lines.append("# CaribWatch Summary Report")
    lines.append(f"Generated: {datetime.utcnow().isoformat()}Z")
    lines.append(f"Window: last {hours} hours")
    lines.append("")

    if last_scan:
        lines.append(f"Last scan: {last_scan.get('timestamp')} ({last_scan.get('findings_count', 0)} findings)")
    else:
        lines.append("Last scan: none yet")

    lines.append("")
    lines.append(f"Total findings in window: {len(findings)}")
    lines.append("")

    if not findings:
        lines.append("No matching indicators detected in the selected window.")
    else:
        # Group by severity
        by_sev = {"high": [], "medium": [], "low": []}
        for f in findings:
            sev = f.get("severity", "low").lower()
            by_sev.setdefault(sev, []).append(f)

        for sev in ["high", "medium", "low"]:
            items = by_sev.get(sev, [])
            if items:
                lines.append(f"## {sev.upper()} ({len(items)})")
                for f in items:
                    lines.append(f"- [{f.get('indicator_type')}] `{f.get('indicator')}` — {f.get('description', '')}")
                lines.append("")

    lines.append("---")
    lines.append("CaribWatch by TrinTech Digital Defense | Authorized use only")

    report_text = "\n".join(lines)

    # Save copy
    reports_dir = ensure_data_dir() / "reports"
    reports_dir.mkdir(exist_ok=True)
    filename = f"report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.md"
    path = reports_dir / filename
    path.write_text(report_text, encoding="utf-8")

    return report_text
