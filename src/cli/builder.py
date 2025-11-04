from __future__ import annotations

import inspect
from typing import Any

from InquirerPy import inquirer  # type: ignore
from InquirerPy.validator import EmptyInputValidator  # type: ignore
from click import Command, Option

from ..utils.cli import clear  # type: ignore
from .custom_group import CustomGroup


class Menus:

    def __init__(
        self, network: str | None = None, update: bool = False
    ) -> None:
        self.network = network
        self.update = update

    # Construct service contents for docker-compose
    def service(self, name: str) -> dict[str, Any]:
        return {}

    def __get_ports(self) -> str:
        return ""

    def __expose(self) -> bool:
        return True

    def __resources(self) -> dict[str, Any]:
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

    def create(self) -> Command:

        help = ""
        options = [Option()]

        def callback() -> dict[str, Any]:
            return {}

        return Command(
            name=inspect.currentframe().f_code.co_name,  # type: ignore
            help=help,
            callback=callback,
            params=options,  # type: ignore
        )

    def update(self) -> Command:

        help = ""
        options = [Option()]

        def callback() -> dict[str, Any]:
            return {}

        return Command(
            name=inspect.currentframe().f_code.co_name,  # type: ignore
            help=help,
            callback=callback,
            params=options,  # type: ignore
        )
