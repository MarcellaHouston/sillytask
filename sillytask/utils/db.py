"""Database access."""

from typing import Iterable
from enum import StrEnum
import sqlite3
from datetime import datetime
from sillytask.config import Config


class Db:
    """Functions related to the database."""

    COL_NAMES = set(["taskid", "name", "note", "created", "due", "category"])

    @staticmethod
    def initialize() -> None:
        """Initialize db tables."""
        con = Db._get_db_()
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                taskid INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                note TEXT,
                category TEXT,
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
        name: str,
        note: str | None = None,
        due: datetime | None = None,
        category: str | None = None,
    ) -> None:
        """Add task to db."""
        con = Db._get_db_()
        con.execute(
            """
            INSERT INTO tasks (name, note, due, category)
            VALUES (?, ?, ?, ?)
            """,
            (name, note, due, category),
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
    def get_tasks(
        cols: Iterable[str], categories: Iterable[str]
    ) -> list[tuple]:
        """Return cols of all tasks with categories."""
        con = Db._get_db_()
        cols = [x for x in cols if x in Db.COL_NAMES]
        cats_tuple = tuple(categories)
        cur = con.execute(
            f"""
            SELECT {", ".join(cols)} FROM tasks
            {("WHERE " + " or ".join(["category LIKE ?"] *
            len(cats_tuple))) if len(cats_tuple) > 0 else ""}
            ORDER BY due ASC, created ASC, taskid
            """,
            cats_tuple,
        )
        return cur.fetchall()

    @staticmethod
    def _get_db_() -> sqlite3.Connection:
        """Return connection to db."""
        return sqlite3.connect(Config.DATABASE_PATH, autocommit=True)
