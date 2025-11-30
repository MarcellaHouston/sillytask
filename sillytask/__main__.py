"""CLI tool for managing tasks."""

import importlib.metadata
from datetime import datetime
import click
from .config import Config
from .utils import Db

__version__ = importlib.metadata.version("sillytask")


@click.group()
@click.version_option(__version__)
def sillytask():
    """Manage todo list items on the command line."""
    (Config.DOTFOLDER / "tasks/").mkdir(parents=True, exist_ok=True)
    Db.initialize()


@sillytask.command()
@click.argument("task")
@click.option("--note", "-n", help="Note details of task.")
@click.option("--due", "-d", help="Due date of task.")  # TODO: Specify format
def add(task: str, note: str | None = None, due: str | None = None):
    """Add task to db."""
    # TODO: Add an input parsing util
    due_datetime = datetime(2026, 1, 12) if due else None
    Db.add_task(task, note, due_datetime)


@sillytask.command()
@click.argument("task")
def cross(task: str):
    """Cross off a done task."""
    Db.cross_task(task)


@sillytask.command(name="list")
def list_tasks():
    """List tasks."""
    Db.print_tasks()


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    sillytask()
