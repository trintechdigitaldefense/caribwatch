import json
from pathlib import Path
from typing import List, Dict, Any

from .config import ensure_data_dir

# Sample Caribbean / regional focused indicators for MVP.
# In production these would be refreshed from a maintained feed.
DEFAULT_INDICATORS = {
    "domains": [
        {"value": "streaming-free-tt.example", "severity": "high", "desc": "Known illegal streaming distribution domain (example)"},
        {"value": "crack-software-download.example", "severity": "high", "desc": "Cracked software malware vector (example)"},
        {"value": "whatsapp-verify-tt.example", "severity": "high", "desc": "Local WhatsApp phishing lure pattern (example)"},
        {"value": "tt-lottery-win.example", "severity": "medium", "desc": "Regional lottery phishing pattern (example)"},
    ],
    "ips": [
        {"value": "185.220.101.0/24", "severity": "medium", "desc": "Known Tor exit / proxy range (sample)"},
        {"value": "45.95.147.0/24", "severity": "medium", "desc": "Residential proxy network sample"},
    ],
    "user_agents": [
        {"value": "ResidentialProxyBot", "severity": "high", "desc": "Known residential proxy tool signature"},
    ],
    "notes": "These are illustrative indicators for the MVP. Replace with real curated Caribbean threat intel."
}


def get_intel_path() -> Path:
    data_dir = ensure_data_dir()
    return data_dir / "intel" / "indicators.json"


def load_indicators() -> Dict[str, Any]:
    path = get_intel_path()
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    # Seed with defaults on first run
    save_indicators(DEFAULT_INDICATORS)
    return DEFAULT_INDICATORS


def save_indicators(data: Dict[str, Any]) -> None:
    path = get_intel_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def update_intel() -> str:
    """
    Placeholder for future remote intel refresh.
    For MVP we just ensure the local file exists and report status.
    """
    indicators = load_indicators()
    count = (
        len(indicators.get("domains", []))
        + len(indicators.get("ips", []))
        + len(indicators.get("user_agents", []))
    )
    return f"Intel loaded: {count} indicators (local curated set). Replace data/intel/indicators.json with live feed when ready."


def match_indicators(observed: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """
    observed: list of dicts with keys like {"type": "domain"|"ip"|"user_agent", "value": "..."}
    Returns list of matches with severity and description.
    """
    indicators = load_indicators()
    matches = []

    domain_map = {d["value"].lower(): d for d in indicators.get("domains", [])}
    ip_map = {i["value"]: i for i in indicators.get("ips", [])}
    ua_map = {u["value"].lower(): u for u in indicators.get("user_agents", [])}

    for item in observed:
        t = item.get("type", "").lower()
        val = item.get("value", "")

        if t == "domain" and val.lower() in domain_map:
            ind = domain_map[val.lower()]
            matches.append({
                "indicator": val,
                "indicator_type": "domain",
                "severity": ind.get("severity", "medium"),
                "description": ind.get("desc", ""),
                "source": "caribwatch-intel",
            })
        elif t == "ip":
            # Simple exact match for MVP (CIDR matching can be added later)
            if val in ip_map:
                ind = ip_map[val]
                matches.append({
                    "indicator": val,
                    "indicator_type": "ip",
                    "severity": ind.get("severity", "medium"),
                    "description": ind.get("desc", ""),
                    "source": "caribwatch-intel",
                })
        elif t == "user_agent" and val.lower() in ua_map:
            ind = ua_map[val.lower()]
            matches.append({
                "indicator": val,
                "indicator_type": "user_agent",
                "severity": ind.get("severity", "medium"),
                "description": ind.get("desc", ""),
                "source": "caribwatch-intel",
            })

    return matches
