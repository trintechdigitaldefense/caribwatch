import json
import os
from pathlib import Path

DEFAULT_CONFIG = {
    "data_dir": str(Path.home() / ".caribwatch"),
    "scan_interval_seconds": 300,
    "alert_threshold": "medium",  # low, medium, high
    "webhook_url": None,
    "enable_console_alerts": True,
    "interface": None,  # None = all interfaces
    "max_findings_retention_days": 30,
}

CONFIG_PATH = Path.home() / ".caribwatch" / "config.json"


def ensure_data_dir() -> Path:
    data_dir = Path(DEFAULT_CONFIG["data_dir"])
    data_dir.mkdir(parents=True, exist_ok=True)
    (data_dir / "intel").mkdir(exist_ok=True)
    (data_dir / "reports").mkdir(exist_ok=True)
    return data_dir


def load_config() -> dict:
    ensure_data_dir()
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            user_cfg = json.load(f)
        cfg = DEFAULT_CONFIG.copy()
        cfg.update(user_cfg)
        return cfg
    return DEFAULT_CONFIG.copy()


def save_config(cfg: dict) -> None:
    ensure_data_dir()
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
