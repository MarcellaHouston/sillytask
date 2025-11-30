"""Config variables."""

from pathlib import Path


class Config:
    """Config variables."""

    DOTFOLDER = Path.home() / ".sillytask"

    DATABASE_PATH = DOTFOLDER / "sillytask.sqlite3"
