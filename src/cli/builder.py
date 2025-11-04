from __future__ import annotations

import inspect
from typing import Any

from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator
from click import Command, Option

from ..core.manage_json import read_json, write_json  # type: ignore
from ..core.manage_templates import template_to_file
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

            services: set[dict[str, Any]] = set([])
            networks: set[str] = set([])
            envs: set[dict[str, Any]] = set([])

            if not network:
                menu = Menus()
                service, env = self.__get_data(menu)
                services.add(service)
                envs.add(env)

            else:
                network_name = self.__get_name(
                    message="Enter the name of the network: "
                )
                networks.add(network_name)

                menu = Menus(network=network_name)

                while True:
                    service, env = self.__get_data(menu)
                    services.add(service)
                    envs.add(env)

                    if not inquirer.confirm(
                        message=f"Want to continue adding services? (Count: {len(services)})",
                        default=True if len(services) < 2 else False,
                    ).execute():
                        break

            self.__save_files(
                data={
                    "compose": {
                        "services": services,
                        "networks": networks,
                    },
                    "envs": envs,
                }
            )

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

    def __get_data(
        self, menu: Menus, get_service: bool = True, get_env: bool = True
    ) -> tuple[dict[str, Any], dict[str, Any]]:

        name = self.__get_name(message="Enter the name of the service: ")

        service = {}
        if get_service:
            service = menu.service(name=name)

        env = {}
        if get_env:
            resources = service.get("resources") or None
            env = menu.env(name=name, resources=resources)

        return (service, env)

    def __get_name(self, message: str) -> str:
        return str(
            inquirer.text(
                message=message, validate=EmptyInputValidator()
            ).execute()
        )

    def __save_files(self, data: dict[str, Any]) -> None:
        write_json()

        composer = data.get("composer")
        template_to_file()

        envs = data.get("envs")
        for env in envs:
            template_to_file()
