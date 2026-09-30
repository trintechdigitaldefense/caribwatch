import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional

from .config import ensure_data_dir


def get_db_path() -> Path:
    return ensure_data_dir() / "findings.db"


def _conn():
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with _conn() as conn:
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
                raw_data TEXT,
                UNIQUE(indicator, indicator_type, severity)
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS scan_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                findings_count INTEGER,
                observations_count INTEGER,
                status TEXT,
                authorization_ref TEXT
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS alert_cooldown (
                indicator TEXT PRIMARY KEY,
                last_alerted TEXT NOT NULL
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS auth_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                action TEXT NOT NULL,
                authorization_ref TEXT,
                details TEXT
            )
        """)
        conn.commit()


def add_finding(indicator: str, indicator_type: str, severity: str,
                description: str = "", source: str = "local",
                raw_data: Optional[dict] = None) -> bool:
    """Returns True if this is a new finding (not a duplicate)."""
    init_db()
    with _conn() as conn:
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO findings (timestamp, indicator, indicator_type, severity, description, source, raw_data) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
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
            return True
        except sqlite3.IntegrityError:
            # Already exists — update timestamp only
            cur.execute(
                "UPDATE findings SET timestamp = ? WHERE indicator = ? AND indicator_type = ? AND severity = ?",
                (datetime.utcnow().isoformat() + "Z", indicator, indicator_type, severity),
            )
            conn.commit()
            return False


def record_scan(findings_count: int, observations_count: int = 0,
                status: str = "completed", authorization_ref: str = "") -> None:
    init_db()
    with _conn() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO scan_history (timestamp, findings_count, observations_count, status, authorization_ref) "
            "VALUES (?, ?, ?, ?, ?)",
            (datetime.utcnow().isoformat() + "Z", findings_count, observations_count, status, authorization_ref),
        )
        conn.commit()


def log_authorization(action: str, authorization_ref: str = "", details: str = "") -> None:
    init_db()
    with _conn() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO auth_log (timestamp, action, authorization_ref, details) VALUES (?, ?, ?, ?)",
            (datetime.utcnow().isoformat() + "Z", action, authorization_ref, details),
        )
        conn.commit()


def is_in_cooldown(indicator: str, cooldown_seconds: int) -> bool:
    init_db()
    with _conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT last_alerted FROM alert_cooldown WHERE indicator = ?", (indicator,))
        row = cur.fetchone()
        if not row:
            return False
        last = datetime.fromisoformat(row["last_alerted"].replace("Z", ""))
        return (datetime.utcnow() - last).total_seconds() < cooldown_seconds


def set_cooldown(indicator: str) -> None:
    init_db()
    with _conn() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT OR REPLACE INTO alert_cooldown (indicator, last_alerted) VALUES (?, ?)",
            (indicator, datetime.utcnow().isoformat() + "Z"),
        )
        conn.commit()


def get_recent_findings(hours: int = 24) -> List[Dict[str, Any]]:
    init_db()
    cutoff = (datetime.utcnow() - timedelta(hours=hours)).isoformat() + "Z"
    with _conn() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM findings WHERE timestamp >= ? ORDER BY timestamp DESC",
            (cutoff,),
        )
        return [dict(row) for row in cur.fetchall()]


def get_last_scan() -> Optional[Dict[str, Any]]:
    init_db()
    with _conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM scan_history ORDER BY id DESC LIMIT 1")
        row = cur.fetchone()
        return dict(row) if row else None


def cleanup_old_findings(days: int = 30) -> int:
    init_db()
    cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat() + "Z"
    with _conn() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM findings WHERE timestamp < ?", (cutoff,))
        deleted = cur.rowcount
        conn.commit()
        return deleted
