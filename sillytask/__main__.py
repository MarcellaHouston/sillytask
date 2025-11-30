"""CLI tool for managing tasks."""

import importlib.metadata
import click
from .config import Config
from .task import Task
from .utils import write_task, delete_task, get_task_list, Db

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
    (Config.DOTFOLDER / "tasks/").mkdir(parents=True, exist_ok=True)
    Db.initialize()
    if task:
        Db.add_task(task)
    if done:
        print("cross")
        Db.cross_task(done)
    if list_tasks:
        Db.print_tasks()


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
