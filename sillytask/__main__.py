"""CLI tool for managing tasks."""

from pathlib import Path
import importlib.metadata
import json
import time
import click
from .config import Config
from .task import Task

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
    Config.PROG_DIR.mkdir(parents=True, exist_ok=True)

    if task:
        new_task = {"task": task, "add_time": int(time.time())}
        with (Config.PROG_DIR / f"{task}.json").open(
            "w", encoding="UTF-8"
        ) as file:
            json.dump(new_task, file)
    if done:
        (Config.PROG_DIR / f"{done}.json").unlink()
    if list_tasks:
        for file in Config.PROG_DIR.iterdir():
            if file.suffix == ".json":
                print(file.read_text())


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
