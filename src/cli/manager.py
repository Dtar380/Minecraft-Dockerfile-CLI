import inspect

from click import Command, Option
from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator

from .custom_group import CustomGroup


class Manager(CustomGroup):

    def __init__(self) -> None:
        super().__init__()

    def bakcup(self) -> Command:

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
    
    def delete(self) -> Command:

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
    
    def start(self) -> Command:

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
    
    def stop(self) -> Command:

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