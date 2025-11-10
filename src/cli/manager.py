from __future__ import annotations

import inspect

from InquirerPy import inquirer  # type: ignore
from InquirerPy.validator import EmptyInputValidator  # type: ignore
from click import Command, Option

from ..utils.cli import clear, confirm  # type: ignore
from .custom_group import CustomGroup


class Manager(CustomGroup):

    def __init__(self) -> None:
        super().__init__()

    def backup(self) -> Command:

        help = "Create a backup of the files inside the containers to their respective build directories."
        options = [Option()]

        def callback() -> None:
            pass

        return Command(
            name=inspect.currentframe().f_code.co_name,  # type: ignore
            help=help,
            callback=callback,
            params=options,  # type: ignore
        )

    def delete(self) -> Command:

        help = "Delete entirely the files related with the containerization of the server/network."
        options = [Option()]

        def callback() -> None:
            pass

        return Command(
            name=inspect.currentframe().f_code.co_name,  # type: ignore
            help=help,
            callback=callback,
            params=options,  # type: ignore
        )

    def start(self) -> Command:

        help = "Start the services."
        options = [Option()]

        def callback() -> None:
            pass

        return Command(
            name=inspect.currentframe().f_code.co_name,  # type: ignore
            help=help,
            callback=callback,
            params=options,  # type: ignore
        )

    def stop(self) -> Command:

        help = "Stop the services."
        options = [Option()]

        def callback() -> None:
            pass

        return Command(
            name=inspect.currentframe().f_code.co_name,  # type: ignore
            help=help,
            callback=callback,
            params=options,  # type: ignore
        )
