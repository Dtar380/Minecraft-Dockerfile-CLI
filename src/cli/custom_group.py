from __future__ import annotations

import inspect

from click import Command, Group


class CustomGroup(Group):

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
