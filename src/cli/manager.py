#################################################
# IMPORTS
#################################################
from __future__ import annotations

import inspect

from InquirerPy import inquirer  # type: ignore
from InquirerPy.validator import EmptyInputValidator  # type: ignore
from click import Command, Option

from ..core.docker import ComposeManager
from .custom_group import CustomGroup


#################################################
# CODE
#################################################
class Manager(CustomGroup):

    def __init__(self) -> None:
        super().__init__()
        self.compose_manager = ComposeManager()

    def backup(self) -> Command:

        help = "Create a backup of the files inside the containers to their respective build directories."
        options = [Option()]

        def callback() -> None:
            self.compose_manager.back_up(self.cwd)

        return Command(
            name=inspect.currentframe().f_code.co_name,  # type: ignore
            help=help,
            callback=callback,
            params=options,  # type: ignore
        )

    def up(self) -> Command:
        help = "Start up the container (first time start)."
        options = [Option(["--detached"], is_flag=True, default=False)]

        def callback(detached: bool = False) -> None:
            self.compose_manager.up(detached)

        return Command(
            name=inspect.currentframe().f_code.co_name,  # type: ignore
            help=help,
            callback=callback,
            params=options,  # type: ignore
        )

    def down(self) -> Command:

        help = "Delete the container."
        options = [Option(["--rm-volumes"], is_flag=True, default=True)]

        def callback(rm_volumes: bool = True) -> None:
            self.compose_manager.down(rm_volumes)

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
            self.compose_manager.start()

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
            self.compose_manager.stop()

        return Command(
            name=inspect.currentframe().f_code.co_name,  # type: ignore
            help=help,
            callback=callback,
            params=options,  # type: ignore
        )
