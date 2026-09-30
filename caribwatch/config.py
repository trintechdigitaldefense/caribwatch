import json
from pathlib import Path
from typing import Any, Dict

DEFAULT_CONFIG: Dict[str, Any] = {
    "data_dir": str(Path.home() / ".caribwatch"),
    "scan_interval_seconds": 300,
    "alert_threshold": "medium",          # low | medium | high
    "webhook_url": None,
    "enable_console_alerts": True,
    "interface": None,
    "max_findings_retention_days": 30,
    "alert_cooldown_seconds": 3600,       # suppress duplicate alerts for same indicator
    "max_observations_per_scan": 5000,    # resource protection
    "client_report_mode": False,
    "organization_name": "",
    "authorization_ref": "",              # e.g. ROE-2026-001 or client ticket
    "suppress_private_ips": True,         # ignore RFC1918 by default for external focus
}

CONFIG_PATH = Path.home() / ".caribwatch" / "config.json"


def ensure_data_dir() -> Path:
    data_dir = Path(DEFAULT_CONFIG["data_dir"])
    data_dir.mkdir(parents=True, exist_ok=True)
    (data_dir / "intel").mkdir(exist_ok=True)
    (data_dir / "reports").mkdir(exist_ok=True)
    (data_dir / "logs").mkdir(exist_ok=True)
    return data_dir


def load_config() -> Dict[str, Any]:
    ensure_data_dir()
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            user_cfg = json.load(f)
        cfg = DEFAULT_CONFIG.copy()
        cfg.update(user_cfg)
        return cfg
    return DEFAULT_CONFIG.copy()


def save_config(cfg: Dict[str, Any]) -> None:
    ensure_data_dir()
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
