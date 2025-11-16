"""Represent a task."""

import time
from datetime import datetime


class Task:
    """A task."""

    def __init__(self, title: str, desc: str = "", add_time=int(time.time())):
        self.title = title
        self.desc = desc
        self.add_time = add_time

    def __repr__(self):
        human_add_time = datetime.fromtimestamp(self.add_time)
        return f"{self.title} | Added: {human_add_time}"
