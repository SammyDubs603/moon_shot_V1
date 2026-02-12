from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

from app.models import AISummary, PortfolioSnapshot, TradeBriefPayload, TradeBriefRow, Holding


DB_PATH = Path(__file__).resolve().parents[1] / "app.db"


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def migrate() -> None:
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS portfolio_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts TEXT NOT NULL,
                total_usd REAL NOT NULL,
                breakdown_json TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS trade_briefs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts TEXT NOT NULL,
                venue TEXT NOT NULL,
                payload_json TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS ai_summaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts TEXT NOT NULL,
                brief_id INTEGER NOT NULL,
                summary_text TEXT NOT NULL,
                changes_text TEXT NOT NULL,
                FOREIGN KEY (brief_id) REFERENCES trade_briefs(id)
            )
            """
        )


def insert_snapshot(snapshot: PortfolioSnapshot) -> None:
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO portfolio_snapshots (ts, total_usd, breakdown_json) VALUES (?, ?, ?)",
            (snapshot.ts.isoformat(), snapshot.total_usd, json.dumps([h.model_dump() for h in snapshot.breakdown])),
        )


def latest_snapshot() -> PortfolioSnapshot | None:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM portfolio_snapshots ORDER BY ts DESC LIMIT 1").fetchone()
    if not row:
        return None
    breakdown = [Holding.model_validate(h) for h in json.loads(row["breakdown_json"])]
    return PortfolioSnapshot(ts=datetime.fromisoformat(row["ts"]), total_usd=row["total_usd"], breakdown=breakdown)


def list_snapshots(limit: int = 60) -> list[PortfolioSnapshot]:
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM portfolio_snapshots ORDER BY ts DESC LIMIT ?", (limit,)).fetchall()
    snapshots: list[PortfolioSnapshot] = []
    for row in rows:
        breakdown = [Holding.model_validate(h) for h in json.loads(row["breakdown_json"])]
        snapshots.append(PortfolioSnapshot(ts=datetime.fromisoformat(row["ts"]), total_usd=row["total_usd"], breakdown=breakdown))
    return snapshots


def insert_brief(brief: TradeBriefRow) -> int:
    with get_conn() as conn:
        cursor = conn.execute(
            "INSERT INTO trade_briefs (ts, venue, payload_json) VALUES (?, ?, ?)",
            (brief.ts.isoformat(), brief.venue, brief.payload.model_dump_json()),
        )
        return int(cursor.lastrowid)


def latest_brief() -> TradeBriefRow | None:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM trade_briefs ORDER BY ts DESC LIMIT 1").fetchone()
    if not row:
        return None
    return TradeBriefRow(
        id=row["id"],
        ts=datetime.fromisoformat(row["ts"]),
        venue=row["venue"],
        payload=TradeBriefPayload.model_validate_json(row["payload_json"]),
    )


def previous_brief(exclude_id: int | None = None) -> TradeBriefRow | None:
    query = "SELECT * FROM trade_briefs"
    params: tuple = ()
    if exclude_id:
        query += " WHERE id != ?"
        params = (exclude_id,)
    query += " ORDER BY ts DESC LIMIT 1"
    with get_conn() as conn:
        row = conn.execute(query, params).fetchone()
    if not row:
        return None
    return TradeBriefRow(
        id=row["id"],
        ts=datetime.fromisoformat(row["ts"]),
        venue=row["venue"],
        payload=TradeBriefPayload.model_validate_json(row["payload_json"]),
    )


def list_briefs(limit: int = 30) -> list[TradeBriefRow]:
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM trade_briefs ORDER BY ts DESC LIMIT ?", (limit,)).fetchall()
    return [
        TradeBriefRow(
            id=row["id"],
            ts=datetime.fromisoformat(row["ts"]),
            venue=row["venue"],
            payload=TradeBriefPayload.model_validate_json(row["payload_json"]),
        )
        for row in rows
    ]


def insert_ai_summary(summary: AISummary) -> int:
    with get_conn() as conn:
        cursor = conn.execute(
            "INSERT INTO ai_summaries (ts, brief_id, summary_text, changes_text) VALUES (?, ?, ?, ?)",
            (summary.ts.isoformat(), summary.brief_id, summary.summary_text, summary.changes_text),
        )
        return int(cursor.lastrowid)


def latest_ai_summary() -> AISummary | None:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM ai_summaries ORDER BY ts DESC LIMIT 1").fetchone()
    if not row:
        return None
    return AISummary(
        id=row["id"],
        ts=datetime.fromisoformat(row["ts"]),
        brief_id=row["brief_id"],
        summary_text=row["summary_text"],
        changes_text=row["changes_text"],
    )
