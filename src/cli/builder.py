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
        self,
        network: str | None = None,
        update: bool = False,
        defaults: dict[str, Any] | None = None,
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
    def env(
        self, name: str, resources: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        return {}

    def __get_jar(self) -> str:
        return ""

    def __use_args(self) -> str:
        return ""

    def __get_heaps(self) -> dict[str, str]:
        return {}


class Builder(CustomGroup):

    def __init__(self) -> None:
        super().__init__()

    def create(self) -> Command:

        help = ""
        options = [Option(["--network"], is_flag=True, default=False)]

        def callback(network: bool = False) -> None:
            services: set[dict[str, Any]] = set()
            networks: set[str] = set()
            envs: set[dict[str, Any]] = set()

            if not network:
                menu = Menus()

                name = inquirer.text(
                    message="Enter the name of the service: "
                ).execute()

                service = menu.service(name=name)

                resources = service.get("resources") or None
                env = menu.env(name=name, resources=resources)

                services.add(service)
                envs.add(env)

                return None

            network_name = inquirer.text(
                message="Enter the name of the network: "
            ).execute()
            networks.add(network_name)

            menu = Menus(network=network_name)

            while True:
                name = inquirer.text(
                    message="Enter the name of the service: "
                ).execute()

                service = menu.service(name=name)

                resources = service.get("resources") or None
                env = menu.env(name=name, resources=resources)

                services.add(service)
                envs.add(env)

                if not inquirer.confirm(
                    message=f"Want to continue adding services? (Count: {len(services)})",
                    default=True if len(services) < 2 else False,
                ).execute():
                    break

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
