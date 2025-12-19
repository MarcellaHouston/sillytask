"""CLI tool for managing tasks."""

from random import randint
import importlib.metadata
from datetime import datetime
import click
import arrow as arw
from prettytable import TableStyle, PrettyTable
from .config import Config
from .utils import Db, code_of, color_hash, RESET_CODE

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
@click.option("--category", "-c", help="Category of tasks.")
def add(
    task: str | None,
    note: str | None = None,
    due: str | None = None,
    category: str | None = None,
):
    """Add task to db."""
    tasks = check_for_stdin(task)

    # TODO: Add an input parsing util
    due_datetime = (
        datetime(randint(2025, 2025), randint(12, 12), randint(18, 31))
        if due
        else None
    )
    for t in tasks:
        Db.add_task(t, note, due_datetime, category)


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
    type=click.Choice(["text", "json", "html", "latex", "csv", "mediawiki"]),
    default="text",
    help="Format of output.",
)
@click.option(
    "--col",
    "yes_cols",
    multiple=True,
    type=click.Choice(Db.COL_NAMES),
    help="Columns to include (can be repeated).",
)
@click.option(
    "--no-col",
    "no_cols",
    multiple=True,
    type=click.Choice(Db.COL_NAMES),
    help="Columns to exclude (can be repeated).",
)
@click.option("--all", "show_all", is_flag=True, help="Include all columns.")
@click.option(
    "--category",
    "-c",
    "categories",
    multiple=True,
    help="Categories to include (can be repeated).",
)
@click.option(
    "--no-format",
    "no_format",
    is_flag=True,
    default=False,
    help="Print without text formatting.",
)
def list_tasks(
    print_format: str,
    yes_cols: tuple[str],
    no_cols: tuple[str],
    categories: tuple[str],
    show_all: bool,
    no_format: bool,
):
    """List tasks."""
    cols_set = set(yes_cols + Config.DEFAULT_LIST_COLS) - set(no_cols)
    cols = tuple(
        x
        for x in Config.LIST_ORDER
        if show_all or x in cols_set or x == "category"
    )
    tasks = Db.get_tasks(cols, categories)
    category_col = cols.index("category")
    colors = [
        color_hash(tasks[i][category_col]) for i in range(len(tasks))
    ]  # TODO: Calculate color based on category

    rows = []
    for j, t in enumerate(tasks):
        row = []
        for i, attr in enumerate(t):
            ansi = code_of(
                colors[j],
                dim=cols[i] == "created",
            )
            if attr is None:
                attr = ""
            elif cols[i] in ["due", "created"]:
                attr = arw.get(attr).humanize()
            row.append(
                (str(attr) if attr is not None else "")
                if no_format
                else (
                    ansi + (str(attr) if attr is not None else "") + RESET_CODE
                )
            )
        rows.append(row)

    table = PrettyTable()
    table.set_style(TableStyle.SINGLE_BORDER)
    table.field_names = [col.capitalize() for col in cols]
    table.add_rows(rows)
    table.align["Desc"] = "l"
    table.align["Name"] = "l"
    table.align["Taskid"] = "r"
    if not ("category" in cols_set or show_all):
        table.del_column("Category")
    print(table.get_formatted_string(out_format=print_format))


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
