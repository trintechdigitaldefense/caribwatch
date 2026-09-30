import ipaddress
import json
from pathlib import Path
from typing import List, Dict, Any, Optional

from .config import ensure_data_dir

# Placeholder structure — replace with real curated Caribbean indicators.
DEFAULT_INDICATORS = {
    "version": "0.2.0-placeholder",
    "last_updated": "2026-09-29",
    "domains": [
        {"value": "streaming-free-tt.example", "severity": "high",
         "desc": "Illegal streaming distribution pattern (REPLACE WITH REAL)", "tags": ["streaming", "malware"]},
        {"value": "crack-software-download.example", "severity": "high",
         "desc": "Cracked software malware vector (REPLACE WITH REAL)", "tags": ["cracked", "malware"]},
        {"value": "whatsapp-verify-tt.example", "severity": "high",
         "desc": "Local WhatsApp phishing lure pattern (REPLACE WITH REAL)", "tags": ["phishing", "whatsapp"]},
        {"value": "tt-lottery-win.example", "severity": "medium",
         "desc": "Regional lottery phishing pattern (REPLACE WITH REAL)", "tags": ["phishing", "lottery"]},
    ],
    "ips": [
        {"value": "185.220.101.0/24", "severity": "medium",
         "desc": "Sample Tor/proxy range — replace with live residential proxy intel", "tags": ["proxy", "tor"]},
        {"value": "45.95.147.0/24", "severity": "medium",
         "desc": "Sample residential proxy network range", "tags": ["residential-proxy"]},
    ],
    "user_agents": [
        {"value": "ResidentialProxyBot", "severity": "high",
         "desc": "Known residential proxy tool signature (example)", "tags": ["proxy-tool"]},
    ],
    "notes": "MVP placeholders only. Load real Caribbean-focused indicators before any client deployment."
}


def get_intel_path() -> Path:
    return ensure_data_dir() / "intel" / "indicators.json"


def load_indicators() -> Dict[str, Any]:
    path = get_intel_path()
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    save_indicators(DEFAULT_INDICATORS)
    return DEFAULT_INDICATORS


def save_indicators(data: Dict[str, Any]) -> None:
    path = get_intel_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def update_intel() -> str:
    indicators = load_indicators()
    count = (
        len(indicators.get("domains", []))
        + len(indicators.get("ips", []))
        + len(indicators.get("user_agents", []))
    )
    version = indicators.get("version", "unknown")
    return (f"Intel loaded: {count} indicators (version {version}). "
            f"Replace ~/.caribwatch/intel/indicators.json with live Caribbean feed before client use.")


def _ip_in_cidr(ip_str: str, cidr: str) -> bool:
    try:
        return ipaddress.ip_address(ip_str) in ipaddress.ip_network(cidr, strict=False)
    except ValueError:
        return False


def _is_private(ip_str: str) -> bool:
    try:
        return ipaddress.ip_address(ip_str).is_private
    except ValueError:
        return False


def match_indicators(observed: List[Dict[str, str]],
                     suppress_private: bool = True) -> List[Dict[str, Any]]:
    """
    observed: list of {"type": "domain"|"ip"|"user_agent", "value": "..."}
    Returns list of matches with severity, description, tags.
    """
    indicators = load_indicators()
    matches = []

    domain_map = {d["value"].lower(): d for d in indicators.get("domains", [])}
    ua_map = {u["value"].lower(): u for u in indicators.get("user_agents", [])}
    ip_rules = indicators.get("ips", [])

    for item in observed:
        t = item.get("type", "").lower()
        val = item.get("value", "").strip()
        if not val:
            continue

        if t == "domain":
            key = val.lower()
            if key in domain_map:
                ind = domain_map[key]
                matches.append({
                    "indicator": val,
                    "indicator_type": "domain",
                    "severity": ind.get("severity", "medium"),
                    "description": ind.get("desc", ""),
                    "tags": ind.get("tags", []),
                    "source": "caribwatch-intel",
                })

        elif t == "ip":
            if suppress_private and _is_private(val):
                continue
            for rule in ip_rules:
                cidr = rule.get("value", "")
                if _ip_in_cidr(val, cidr):
                    matches.append({
                        "indicator": val,
                        "indicator_type": "ip",
                        "matched_rule": cidr,
                        "severity": rule.get("severity", "medium"),
                        "description": rule.get("desc", ""),
                        "tags": rule.get("tags", []),
                        "source": "caribwatch-intel",
                    })
                    break  # first match wins

        elif t == "user_agent":
            key = val.lower()
            if key in ua_map:
                ind = ua_map[key]
                matches.append({
                    "indicator": val,
                    "indicator_type": "user_agent",
                    "severity": ind.get("severity", "medium"),
                    "description": ind.get("desc", ""),
                    "tags": ind.get("tags", []),
                    "source": "caribwatch-intel",
                })

    return matches
