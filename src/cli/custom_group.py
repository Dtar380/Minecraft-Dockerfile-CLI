import inspect

from click import Group, Command


class CustomGroup(Group):

    def __init__(self) -> None:
        super().__init__()
        self.__register_commands()

    def __register_commands(self) -> None:
        for _, method in inspect.getmembers(self, predicate=inspect.ismethod):
            result = method()
            if isinstance(result, Command):
                self.add_command(result)