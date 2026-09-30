import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any

from .config import load_config, ensure_data_dir


def get_db_path() -> Path:
    data_dir = ensure_data_dir()
    return data_dir / "findings.db"


def init_db() -> None:
    conn = sqlite3.connect(get_db_path())
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS findings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            indicator TEXT NOT NULL,
            indicator_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            description TEXT,
            source TEXT,
            raw_data TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS scan_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            findings_count INTEGER,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()


def add_finding(indicator: str, indicator_type: str, severity: str,
                description: str = "", source: str = "local", raw_data: dict = None) -> None:
    init_db()
    conn = sqlite3.connect(get_db_path())
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO findings (timestamp, indicator, indicator_type, severity, description, source, raw_data) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            datetime.utcnow().isoformat() + "Z",
            indicator,
            indicator_type,
            severity,
            description,
            source,
            json.dumps(raw_data or {}),
        ),
    )
    conn.commit()
    conn.close()


def record_scan(findings_count: int, status: str = "completed") -> None:
    init_db()
    conn = sqlite3.connect(get_db_path())
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO scan_history (timestamp, findings_count, status) VALUES (?, ?, ?)",
        (datetime.utcnow().isoformat() + "Z", findings_count, status),
    )
    conn.commit()
    conn.close()


def get_recent_findings(hours: int = 24) -> List[Dict[str, Any]]:
    init_db()
    cutoff = (datetime.utcnow() - timedelta(hours=hours)).isoformat() + "Z"
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM findings WHERE timestamp >= ? ORDER BY timestamp DESC",
        (cutoff,),
    )
    rows = [dict(row) for row in cur.fetchall()]
    conn.close()
    return rows


def get_last_scan() -> Dict[str, Any] | None:
    init_db()
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM scan_history ORDER BY id DESC LIMIT 1")
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def cleanup_old_findings(days: int = 30) -> int:
    init_db()
    cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat() + "Z"
    conn = sqlite3.connect(get_db_path())
    cur = conn.cursor()
    cur.execute("DELETE FROM findings WHERE timestamp < ?", (cutoff,))
    deleted = cur.rowcount
    conn.commit()
    conn.close()
    return deleted
