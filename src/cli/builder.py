from __future__ import annotations

import inspect
from pathlib import Path, PurePath
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
        self, network: str | None = None, update: bool = False
    ) -> None:
        self.network = network
        self.update = update
        self.ports: dict[str, int] = {}
        self.resources = dict[str, Any]

    # Construct service contents for docker-compose
    def service(self, name: str) -> dict[str, Any]:
        self.__get_ports()
        ports = [f"${{{port}}}:${{{port}}}" for port, _ in self.ports.items()]
        expose = self.__expose()
        resources = self.__resources()

        service = {
            "name": name,
            "build": {"context": f"./servers/{name}/"},
            "env_file": f"./servers/{name}/.env",
            "volume": f"./servers/{name}:/{name}",
        }

        if ports:
            service["ports"] = ports
        if expose:
            service["expose"] = expose  # type: ignore
        if self.network:
            service["networks"] = self.network
        if resources:
            service["resources"] = resources

        return service

    def __get_ports(self) -> None:
        while True:
            clear(1)

            port_name = inquirer.text(
                message="Add a name for the port: ",
                validate=EmptyInputValidator(),
            ).execute()

            port = inquirer.number(
                message="Add port number: ",
                min_allowed=1,
                max_allowed=2**16 - 1,
                default=25565,
                validate=EmptyInputValidator(),
            ).execute()

            if inquirer.confirm(
                message=f"Want to add {port_name} assigned to port {port}? ",
                default=True,
            ).execute():
                self.ports[port_name] = port

            if inquirer.confirm(
                message="Want to add more ports? ", default=False
            ).execute():
                break

    def __expose(self) -> set[int]:
        expose: set[int] = set()

        for name, port in self.ports.items():
            if inquirer.confirm(
                message=f"Want to expose {name} assigned to {port}? ",
                default=False,
            ).execute():
                expose.add(port)

        return expose

    def __resources(self) -> dict[str, Any]:
        return {}

    # Construct env file contents
    def env(self, name: str) -> dict[str, Any]:
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

            clear(1)

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
                    menu.ports = {}

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
            env = menu.env(name=name)

        return (service, env)

    def __get_name(self, message: str) -> str:
        return str(
            inquirer.text(
                message=message, validate=EmptyInputValidator()
            ).execute()
        )

    def __save_files(self, data: dict[str, Any]) -> None:
        write_json(Path(), data)

        composer: dict[str, Any] = data.get("composer") or {}
        template_to_file(Path(), composer, Path())

        envs: list[dict[str, Any]] = data.get("envs") or []
        for env in envs:
            template_to_file(Path(), env, Path())
