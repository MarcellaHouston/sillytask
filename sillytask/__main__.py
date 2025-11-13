"""CLI tool for managing tasks."""

import importlib.metadata
import click

__version__ = importlib.metadata.version("sillytask")


@click.command()
@click.version_option(__version__)
@click.option("--add", "-a", "task", help="Text describing a task")
@click.option("--cross", "-x", "done", help="Task to cross off")
def main(*, task: str, done: str) -> None:
    if task:
        print(f"Task: {task}")
    if done:
        print(f"Done: {done}")


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
