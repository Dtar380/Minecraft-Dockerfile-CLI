from __future__ import annotations

import inspect
from pathlib import Path
from typing import Any

from InquirerPy import inquirer  # type: ignore
from InquirerPy.validator import EmptyInputValidator  # type: ignore
from click import Command, Option
import psutil  # type: ignore

from ..core.manage_json import read_json, write_json  # type: ignore
from ..core.manage_templates import template_to_file
from ..utils.cli import clear, confirm  # type: ignore
from .custom_group import CustomGroup


class Menus:

    def __init__(
        self, network: str | None = None, update: bool = False
    ) -> None:
        self.network = network
        self.update = update

        self.cpus: float = psutil.cpu_count(logical=True) or 0
        self.memory: float = (
            psutil.virtual_memory().available // 1024**2 - 512 or 0
        )

        self.ports: dict[str, int] = {}
        self.resources: dict[str, Any] = {}

        if self.memory < 512:
            print("WARNING: RAM AMOUNT TOO LOW")
        clear(2)

    # Construct service contents for docker-compose
    def service(self, name: str) -> dict[str, Any]:
        self.__get_ports()
        expose = self.__expose()
        not_exposed = set([port for port in self.ports if port not in expose])
        ports = set([f"${{{port}}}:${{{port}}}" for port in not_exposed])
        self.__resources()
        resources = self.resources

        resources["limits"]["memory"] = (
            str(resources["limits"]["memory"] / 1024) + "g"
        )
        resources["reservations"]["memory"] = (
            str(resources["reservations"]["memory"] / 1024) + "g"
        )

        service: dict[str, Any] = {
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

            port_name = inquirer.text(  # type: ignore
                message="Add a name for the port: ",
                validate=EmptyInputValidator(),
            ).execute()

            port = inquirer.number(  # type: ignore
                message="Add port number: ",
                min_allowed=1,
                max_allowed=2**16 - 1,
                default=25565,
                validate=EmptyInputValidator(),
            ).execute()

            if inquirer.confirm(  # type: ignore
                message=f"Want to add {port_name} assigned to port {port}? ",
                default=False,
            ).execute():
                self.ports[port_name] = port

                if inquirer.confirm(  # type: ignore
                    message="Want to add more ports? ", default=False
                ).execute():
                    return None

    def __expose(self) -> set[str]:
        expose: set[str] = set()

        for name, port in self.ports.items():
            clear(1)

            if inquirer.confirm(  # type: ignore
                message=f"Want to expose {name} assigned to {port}? ",
                default=False,
            ).execute():
                expose.add(f"${{{name}}}")

        return expose

    def __resources(self) -> None:
        while True:
            cpus_limit: float = inquirer.number(  # type: ignore
                message="Select a limit of CPUs for this service: ",
                min_allowed=0,
                max_allowed=self.cpus,
                float_allowed=True,
                validate=EmptyInputValidator(),
            ).execute()
            cpus_reservation: float = inquirer.number(  # type: ignore
                message="Select a CPUs allocation for this service: ",
                min_allowed=0,
                max_allowed=cpus_limit,
                float_allowed=True,
                validate=EmptyInputValidator(),
            ).execute()

            memory_limit: float = inquirer.number(  # type: ignore
                message="Select a limit of RAM for this service (in MB): ",
                min_allowed=0,
                max_allowed=self.memory,
                float_allowed=True,
                validate=EmptyInputValidator(),
            ).execute()
            memory_reservation: float = inquirer.number(  # type: ignore
                message="Select a RAM allocation for this service (in MB): ",
                min_allowed=0,
                max_allowed=memory_limit,
                float_allowed=True,
                validate=EmptyInputValidator(),
            ).execute()

            if inquirer.confirm(  # type: ignore
                message="Confirm the RAM and CPU allocation for this service",
                default=False,
            ).execute():
                break

        self.cpus -= cpus_limit
        self.memory -= memory_limit

        self.resources = {
            "limits": {"cpus": cpus_limit, "memory": memory_limit},
            "reservations": {
                "cpus": cpus_reservation,
                "memory": memory_reservation,
            },
        }

    # Construct env file contents
    def env(self, name: str) -> dict[str, Any]:
        heaps = self.__get_heaps()

        return {
            "CONTAINER_NAME": name,
            "SEVER_JAR": self.__get_jar(),
            "JAVA_ARGS": self.__use_args(),
            "MIN_HEAP_SIZE": heaps[0],
            "MAX_HEAP_SIZE": heaps[1],
            "HOST_PORTS": self.ports,
        }

    def __get_jar(self) -> str:
        while True:
            jar: str = inquirer.text(  # type: ignore
                message="Enter your .jar file name: ",
                validate=EmptyInputValidator(),
            ).execute()

            if inquirer.confirm(  # type: ignore
                message=f"Confirm your jar file is {jar}", default=False
            ).execute():
                break

        return jar

    def __use_args(self) -> str:
        if inquirer.confirm(  # type: ignore
            message="Want to use recommended args for the server? ",
            default=False,
        ).execute():
            with open("", "r+") as f:
                data = " ".join(f.readlines())
            return data
        return ""

    def __get_heaps(self) -> list[str]:
        while True:
            min_heap_size: int = int(
                inquirer.number(  # type: ignore
                    message="Select the minimum heap size: ",
                    min_allowed=self.resources["reservations"]["memory"],
                    max_allowed=self.resources["limit"]["memory"],
                    float_allowed=False,
                ).execute()
            )

            max_heap_size: int = int(
                inquirer.number(  # type: ignore
                    message="Select the minimum heap size: ",
                    min_allowed=min_heap_size,
                    max_allowed=self.resources["limit"]["memory"],
                    float_allowed=False,
                ).execute()
            )

            if inquirer.confirm(  # type: ignore
                message="Confirm Heap allocations", default=False
            ).execute():
                break

        return [f"{min_heap_size}M", f"{max_heap_size}M"]


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

            clear(0)

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

                    clear(1)

                    if not inquirer.confirm(  # type: ignore
                        message=f"Want to continue adding services? (Count: {len(services)})",
                        default=False,
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
        clear(1)

        name = self.__get_name(message="Enter the name of the service: ")

        service = {}
        if get_service:
            service = menu.service(name=name)

        env = {}
        if get_env:
            env = menu.env(name=name)

        return (service, env)

    def __get_name(self, message: str) -> str:
        while True:
            name: str = inquirer.text(  # type: ignore
                message=message, validate=EmptyInputValidator()
            ).execute()

            if inquirer.confirm(  # type: ignore
                message=f"Want to name this service '{name}'? ",
                default=False,
            ).execute():
                break

        return name

    def __save_files(self, data: dict[str, Any]) -> None:
        write_json(Path(), data)

        composer: dict[str, Any] = data.get("composer") or {}
        template_to_file(Path(), composer, Path())

        envs: list[dict[str, Any]] = data.get("envs") or []
        for env in envs:
            template_to_file(Path(), env, Path())
