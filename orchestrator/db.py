"""Cơ sở dữ liệu sự kiện (SQLite). Xem PRD mục 7 cho ý nghĩa các trường."""

import sqlite3
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    run_id TEXT NOT NULL,
    task_id TEXT,
    agent TEXT,
    event_type TEXT NOT NULL,
    model TEXT,
    tokens_in INTEGER,
    tokens_out INTEGER,
    cost REAL,
    duration_ms INTEGER,
    status TEXT,
    ref TEXT
);
CREATE INDEX IF NOT EXISTS idx_events_run ON events (run_id);
"""


def init_db(path: str) -> sqlite3.Connection:
    """Tạo file DB (và thư mục cha) nếu chưa có, tạo bảng, trả về kết nối."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.executescript(SCHEMA)
    conn.commit()
    return conn
