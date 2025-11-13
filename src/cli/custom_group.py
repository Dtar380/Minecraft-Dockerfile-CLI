#################################################
# IMPORTS
#################################################
from __future__ import annotations

import inspect
from pathlib import Path

from click import Command, Group


#################################################
# CODE
#################################################
class CustomGroup(Group):

    cwd: Path = Path.cwd()

    def __init__(self) -> None:
        super().__init__()
        self.__register_commands()

    def __register_commands(self) -> None:
        for name, method in inspect.getmembers(
            self, predicate=inspect.ismethod
        ):
            if name.startswith("_"):
                continue

            try:
                result = method()
            except Exception:
                continue

            if isinstance(result, Command):
                self.add_command(result)
