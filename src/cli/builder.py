from __future__ import annotations

import inspect

from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator
from click import Command, Option

from .custom_group import CustomGroup
from ..utils.cli import clear


class Builder(CustomGroup):

    def __init__(self) -> None:
        super().__init__()

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
