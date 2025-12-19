"""Config variables."""

from pathlib import Path


class Config:
    """Config variables."""

    DOTFOLDER = Path.home() / ".sillytask"

    DATABASE_PATH = DOTFOLDER / "sillytask.sqlite3"

    DARK_TERMINAL = True

    DEFAULT_LIST_COLS = ("name", "due", "category")
    LIST_ORDER = ("taskid", "name", "note", "due", "category", "created")
