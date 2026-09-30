from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

from .config import ensure_data_dir, load_config
from .db import get_recent_findings, get_last_scan


def generate_report(hours: int = 24, client_mode: bool = False) -> str:
    findings = get_recent_findings(hours=hours)
    last_scan = get_last_scan()
    cfg = load_config()
    org = cfg.get("organization_name") or "Client"
    auth_ref = cfg.get("authorization_ref") or "N/A"

    lines = []

    if client_mode:
        lines.append(f"# Security Visibility Summary — {org}")
        lines.append(f"**Prepared by:** TrinTech Digital Defense")
        lines.append(f"**Period:** Last {hours} hours")
        lines.append(f"**Generated:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC")
        lines.append(f"**Authorization Reference:** {auth_ref}")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## Executive Summary")
        if not findings:
            lines.append("No matching threat indicators were detected in the monitored period.")
            lines.append("This does not guarantee the absence of all threats — only that no indicators "
                         "currently in the CaribWatch intelligence set were observed.")
        else:
            high = sum(1 for f in findings if f.get("severity", "").lower() == "high")
            medium = sum(1 for f in findings if f.get("severity", "").lower() == "medium")
            low = sum(1 for f in findings if f.get("severity", "").lower() == "low")
            lines.append(f"CaribWatch observed **{len(findings)}** indicator match(es) in the last {hours} hours.")
            lines.append(f"- High: {high}")
            lines.append(f"- Medium: {medium}")
            lines.append(f"- Low: {low}")
            lines.append("")
            lines.append("Details are provided below. Recommended next steps are listed at the end of this report.")
    else:
        lines.append("# CaribWatch Operator Report")
        lines.append(f"Generated: {datetime.utcnow().isoformat()}Z")
        lines.append(f"Window: last {hours} hours")
        lines.append(f"Authorization Ref: {auth_ref}")
        lines.append("")

    if last_scan:
        lines.append(f"Last scan: {last_scan.get('timestamp')} "
                     f"({last_scan.get('findings_count', 0)} findings, "
                     f"{last_scan.get('observations_count', 0)} observations)")
    else:
        lines.append("Last scan: none yet")

    lines.append("")
    lines.append(f"Total findings in window: {len(findings)}")
    lines.append("")

    if findings:
        by_sev = {"high": [], "medium": [], "low": []}
        for f in findings:
            sev = f.get("severity", "low").lower()
            by_sev.setdefault(sev, []).append(f)

        for sev in ["high", "medium", "low"]:
            items = by_sev.get(sev, [])
            if items:
                lines.append(f"## {sev.upper()} ({len(items)})")
                for f in items:
                    desc = f.get("description", "") or ""
                    lines.append(f"- **[{f.get('indicator_type')}]** `{f.get('indicator')}` — {desc}")
                lines.append("")

    if client_mode and findings:
        lines.append("## Recommended Next Steps")
        lines.append("1. Review high-severity items first with your technical contact.")
        lines.append("2. Confirm whether any matched indicators are expected business traffic.")
        lines.append("3. If unexpected, isolate affected systems and contact TrinTech for deeper investigation.")
        lines.append("4. Schedule a follow-up scan after any remediation.")
        lines.append("")

    lines.append("---")
    lines.append("CaribWatch by TrinTech Digital Defense | Authorized use only")
    lines.append("This report is confidential and intended solely for the authorized recipient.")

    report_text = "\n".join(lines)

    # Persist
    reports_dir = ensure_data_dir() / "reports"
    reports_dir.mkdir(exist_ok=True)
    suffix = "client" if client_mode else "operator"
    filename = f"report_{suffix}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.md"
    (reports_dir / filename).write_text(report_text, encoding="utf-8")

    return report_text
