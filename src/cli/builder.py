from __future__ import annotations

import inspect
from pathlib import Path
from typing import Any

from InquirerPy import inquirer  # type: ignore
from InquirerPy.validator import EmptyInputValidator  # type: ignore
from click import Command, Option
from yaspin import yaspin  # type: ignore

from ..core.copy_files import copy_files  # type: ignore
from ..core.manage_json import read_json, write_json
from ..core.manage_templates import template_to_file
from ..utils.cli import clear, confirm
from .custom_group import CustomGroup
from .menu import Menus


class Builder(CustomGroup):

    def __init__(self) -> None:
        super().__init__()

    def create(self) -> Command:
        help = (
            "Create all files for the containerization of the server/network."
        )
        options = [Option(["--network"], is_flag=True, default=False)]

        def callback(network: bool = False) -> None:
            clear(0)

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
                    menu.ports = {}

                    service, env = self.__get_data(menu)
                    services.add(service)
                    envs.add(env)

                    clear(0.5)

                    if not confirm(
                        msg=f"Want to continue adding services? (Count: {len(services)})",
                    ):
                        break

            clear(0)
            self.__save_files(
                data={
                    "compose": {
                        "services": services,
                        "networks": networks,
                    },
                    "envs": envs,
                }
            )
            clear(0)
            print("Files saved!")

        return Command(
            name=inspect.currentframe().f_code.co_name,  # type: ignore
            help=help,
            callback=callback,
            params=options,  # type: ignore
        )

    def update(self) -> Command:
        help = "Update the contents of the containers."
        options = [
            Option(["--service"], default=None),
            Option(["--add"], is_flag=True, default=False),
            Option(["--remove"], is_flag=True, default=False),
        ]

        def callback(
            service: str | None = None, add: bool = False, remove: bool = False
        ) -> None:
            clear(0)

            path: Path = Path()

            if not path.exists():
                print("Missing JSON file for services. Use 'create' first.")
                return

            data: dict[str, Any] = read_json(Path()) or {}
            compose: dict[str, Any] = data.get("compose", {}) or {}

            services: set[dict[str, Any]] = set(compose.get("services", []))
            networks: set[str] = set(compose.get("networks", []))
            envs: set[dict[str, Any]] = set(data.get("envs", []))

            if networks:
                pass
            if envs:
                pass

            if not services:
                print("No services found. Use 'create' first.")
                return

        return Command(
            name=inspect.currentframe().f_code.co_name,  # type: ignore
            help=help,
            callback=callback,
            params=options,  # type: ignore
        )

    def build(self) -> Command:
        help = "Build the files for the containerization in case create failed."
        options: list[Option] = []

        def callback(
            service: str | None = None, add: bool = False, remove: bool = False
        ) -> None:
            clear(0)

            path: Path = Path()

            if not path.exists():
                print("Missing JSON file for services. Use 'create' first.")
                return

            data: dict[str, Any] = read_json(Path()) or {}

            if not data:
                print("JSON file is empty. Use 'create' first.")

            clear(0)
            self.__save_files(data, build=True)
            clear(0)
            print("Files saved!")

        return Command(
            name=inspect.currentframe().f_code.co_name,  # type: ignore
            help=help,
            callback=callback,
            params=options,  # type: ignore
        )

    def __get_data(
        self, menu: Menus, get_service: bool = True, get_env: bool = True
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        clear(0.5)

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
            clear(0.5)
            name: str = inquirer.text(  # type: ignore
                message=message, validate=EmptyInputValidator()
            ).execute()

            if confirm(msg=f"Want to name this service '{name}'? "):
                break

        return name

    @yaspin(text="Creating files...", color="cyan")
    def __save_files(self, data: dict[str, Any], build: bool = False) -> None:
        if not build:
            write_json(Path(), data)

        composer: dict[str, Any] = data.get("composer") or {}
        template_to_file(Path(), composer, Path())

        envs: list[dict[str, Any]] = data.get("envs") or []
        for env in envs:
            relative_path = f"servers/{env.get("CONTAINER_NAME")}/.env"  # type: ignore
            template_to_file(Path(), env, Path())
