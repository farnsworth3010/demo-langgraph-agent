"""SQLite helpers for storing tickets.

This module initializes the database, creates the tickets table, and
provides simple utilities for retrieving and listing tickets.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

DB_DIR_NAME = "data"
DB_FILE_NAME = "tickets.db"


def _get_default_db_path() -> Path:
    """Return the default database file path: `data/tickets.db` at the repo root."""
    repo_root = Path(__file__).resolve().parents[1]
    data_dir = repo_root / DB_DIR_NAME
    data_dir.mkdir(parents=True, exist_ok=True)

    return data_dir / DB_FILE_NAME


def init_db(db_path: Path | str | None = None) -> sqlite3.Connection:
    """Initialize a sqlite3 connection and ensure the `tickets` table exists.

    Args:
        db_path: Optional path to the sqlite file. If omitted, uses
            `data/tickets.db` at the repository root.

    Returns:
        A sqlite3.Connection object (row_factory set to sqlite3.Row).
    """
    path = Path(db_path) if db_path else _get_default_db_path()
    conn = sqlite3.connect(
        str(path),
        detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
        check_same_thread=False,
    )
    conn.row_factory = sqlite3.Row
    _ensure_tables(conn)

    return conn


def _ensure_tables(conn: sqlite3.Connection) -> None:
    """Create the `tickets` table if it does not already exist."""
    create_sql = """
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        priority TEXT,
        category TEXT,
        client_name TEXT,
        description TEXT,
        steps_taken TEXT,
        email TEXT,
        status TEXT DEFAULT 'open',
        created_at TEXT DEFAULT (datetime('now')),
        updated_at TEXT DEFAULT (datetime('now'))
    );
    """
    conn.execute(create_sql)
    conn.commit()


_conn: sqlite3.Connection | None = None


def get_connection() -> sqlite3.Connection:
    """Return the global sqlite3 connection, initialized on first access."""
    global _conn
    if _conn is None:
        _conn = init_db()
    return _conn
