"""File management utility functions."""

import json
from sillytask.task import Task
from sillytask.config import Config


def write_task(task: Task) -> None:
    """
    Write task to disk.

    Overwrites old tasks named task.title.
    """
    with (Config.PROG_DIR / f"tasks/{task.title}.json").open(
        "w", encoding="UTF-8"
    ) as file:
        json.dump(task.__dict__, file)


def delete_task(task_title: str) -> None:
    """
    Delete task with task_title from disk.

    Raises FileNotFoundError if no task has task_title.
    """
    (Config.PROG_DIR / f"tasks/{task_title}.json").unlink()


def get_task_list() -> list[Task]:
    """Return list of tasks."""
    tasks: list[Task] = []
    for file_path in (Config.PROG_DIR / "tasks/").iterdir():
        if file_path.suffix != ".json":
            continue
        with file_path.open("r", encoding="UTF-8") as file:
            task_dict: dict = json.load(file)
            tasks.append(
                Task(
                    task_dict["title"],
                    task_dict["desc"],
                    task_dict["add_time"],
                )
            )
    return tasks
