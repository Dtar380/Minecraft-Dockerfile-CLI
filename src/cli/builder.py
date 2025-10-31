import inspect

from click import Command, Option
from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator

from .custom_group import CustomGroup


class Builder(CustomGroup):

    def __init__(self) -> None:
        super().__init__()

    def create(self) -> Command:

        help = ""
        options = [
            Option()
        ]

        def callback() -> None:
            pass

        return Command(
            name=inspect.currentframe().f_code.co_name, # type: ignore
            help=help,
            callback=callback,
            params=options # type: ignore
        )
    
    def update(self) -> Command:

        help = ""
        options = [
            Option()
        ]

        def callback() -> None:
            pass

        return Command(
            name = inspect.currentframe().f_code.co_name, # type: ignore
            help=help,
            callback=callback,
            params=options # type: ignore
        )