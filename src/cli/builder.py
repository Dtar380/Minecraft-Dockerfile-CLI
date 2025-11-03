from __future__ import annotations

import inspect
from typing import Any

from InquirerPy import inquirer  # type: ignore
from InquirerPy.validator import EmptyInputValidator  # type: ignore
from click import Command, Option

from ..utils.cli import clear  # type: ignore
from .custom_group import CustomGroup


class Menus:

    # Construct service contents for docker-compose
    def service(self) -> dict[str, Any]:
        return {}

    def __get_name(self) -> str:
        return ""

    def __get_ports(self) -> str:
        return ""

    def __expose(self) -> bool:
        return True

    def __resources(self) -> dict[str, int]:
        return {}

    # Construct env file contents
    def env(self) -> dict[str, Any]:
        return {}

    def __get_jar(self) -> str:
        return ""

    def __use_args(self) -> str:
        return ""

    def __get_heaps(self) -> dict[str, str]:
        return {}

    def __get_type(self) -> str:
        return ""


class Builder(CustomGroup):

    def __init__(self) -> None:
        super().__init__()
        self.menus = Menus()

    def create(self) -> Command:

        help = ""
        options = [Option()]

        def callback() -> None:
            pass

        return Command(
            name=inspect.currentframe().f_code.co_name,  # type: ignore
            help=help,
            callback=callback,
            params=options,  # type: ignore
        )

    def update(self) -> Command:

        help = ""
        options = [Option()]

        def callback() -> None:
            pass

        return Command(
            name=inspect.currentframe().f_code.co_name,  # type: ignore
            help=help,
            callback=callback,
            params=options,  # type: ignore
        )
