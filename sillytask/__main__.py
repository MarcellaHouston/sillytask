"""CLI tool for managing tasks."""

from random import randint
import importlib.metadata
from datetime import datetime
import click
from prettytable import PrettyTable
from .config import Config
from .utils import Db

__version__ = importlib.metadata.version("sillytask")


def check_for_stdin(arg: str | None) -> list[str]:
    """
    Return list of args to run command on.

    First check if an arg was passed and return that as a list.
    If there's no arg, return stdin as a list of str lines.
    """
    # TODO: Allow string input to consist of multiple args
    # TODO: Print usage if no arg is given and nothing is piped in
    return (
        [arg] if arg else [x.strip() for x in click.get_text_stream("stdin")]
    )


@click.group()
@click.version_option(__version__)
def sillytask():
    """Manage todo list items on the command line."""
    (Config.DOTFOLDER / "tasks/").mkdir(parents=True, exist_ok=True)
    Db.initialize()


@sillytask.command()
@click.argument("task", required=False)
@click.option("--note", "-n", help="Note details of task.")
@click.option("--due", "-d", help="Due date of task.")  # TODO: Specify format
def add(task: str | None, note: str | None = None, due: str | None = None):
    """Add task to db."""
    tasks = check_for_stdin(task)

    # TODO: Add an input parsing util
    due_datetime = (
        datetime(randint(2025, 2030), randint(1, 12), randint(1, 27))
        if due
        else None
    )
    for t in tasks:
        Db.add_task(t, note, due_datetime)


@sillytask.command()
@click.argument("task")
def cross(task: str):
    """Cross off a done task."""
    Db.cross_task(task)


@sillytask.command(name="list")
@click.option(
    "--format",
    "-f",
    "print_format",
    type=click.Choice(["plain", "json"]),
    default="plain",
    help="Format of output.",
)
@click.option("--name-only", "-n", default=False, help="Only print names.")
def list_tasks(print_format: str, name_only: bool):
    """List tasks."""
    print(f"format={print_format} name_only={name_only}")
    tasks = (
        [{"name": x["name"]} for x in Db.get_tasks()]
        if name_only
        else Db.get_tasks()
    )
    if print_format == "json":
        print(tasks)
    elif print_format == "plain":
        table = PrettyTable()
        table.field_names = [attr for attr in tasks[0].keys()]
        table.add_rows([[attr for attr in t.values()] for t in tasks])
        print(table)


@sillytask.command()
@click.argument("confirm", required=False)
def reset(confirm: str = ""):
    """Delete the db and build it again."""
    if confirm == "confirm":
        Db.drop()
    else:
        print("Please run 'sillytask reset confirm' to actually reset the db.")


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    sillytask()
