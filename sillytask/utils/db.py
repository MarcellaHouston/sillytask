"""Database access."""

from typing import Any
import sqlite3
from datetime import datetime
from sillytask.config import Config


class Db:
    """Functions related to the database."""

    @staticmethod
    def initialize() -> None:
        """Initialize db tables."""
        con = Db._get_db_()
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks(
                taskid INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                desc TEXT,
                created DATETIME DEFAULT CURRENT_TIMESTAMP,
                due DATETIME
            )
            """
        )

    @staticmethod
    def drop() -> None:
        """Delete the db file."""
        Config.DATABASE_PATH.unlink()

    @staticmethod
    def add_task(
        name: str, desc: str | None = None, due: datetime | None = None
    ) -> None:
        """Add task to db."""
        con = Db._get_db_()
        con.execute(
            """
            INSERT INTO tasks (name, desc, due)
            VALUES (?, ?, ?)
            """,
            (name, desc, due),
        )

    @staticmethod
    def cross_task(name: str):
        """Cross off a task."""
        con = Db._get_db_()
        con.execute(
            """
            DELETE FROM tasks
            WHERE name = ?
            """,
            (name,),
        )

    @staticmethod
    def get_tasks() -> list[dict[str, Any]]:
        """Return all tasks."""
        con = Db._get_db_()
        cur = con.execute(
            """
            SELECT taskid, name, desc, created, due FROM tasks
            ORDER BY due ASC, created ASC, taskid
            """
        )
        return [
            {
                "taskid": t[0],
                "name": t[1],
                "desc": t[2],
                "created": t[3],
                "due": t[4],
            }
            for t in cur.fetchall()
        ]

    @staticmethod
    def _get_db_() -> sqlite3.Connection:
        """Return connection to db."""
        return sqlite3.connect(Config.DATABASE_PATH, autocommit=True)
