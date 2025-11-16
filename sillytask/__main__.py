"""CLI tool for managing tasks."""

from pathlib import Path
import importlib.metadata
import json
import time
import click
from .config import Config
from .task import Task
from .utils import write_task, delete_task, get_task_list

__version__ = importlib.metadata.version("sillytask")


@click.command()
@click.version_option(__version__)
@click.option("--add", "-a", "task", help="Text describing a task")
@click.option("--cross", "-x", "done", help="Task to cross off")
@click.option(
    "--list", "-l", "list_tasks", help="List all tasks", is_flag=True
)
def main(
    list_tasks: bool, task: str | None = None, done: str | None = None
) -> None:
    (Config.PROG_DIR / "tasks/").mkdir(parents=True, exist_ok=True)

    if task:
        write_task(Task(task))
    if done:
        delete_task(done)
    if list_tasks:
        for item in get_task_list():
            print(item)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
