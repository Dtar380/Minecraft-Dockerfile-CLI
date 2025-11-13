from __future__ import annotations

import inspect
from pathlib import Path
from typing import Any, cast

from InquirerPy import inquirer  # type: ignore
from InquirerPy.validator import EmptyInputValidator  # type: ignore
from click import Command, Option
from importlib_resources import as_file, files  # type: ignore
from yaspin import yaspin  # type: ignore

from ..core.copy_files import copy_files  # type: ignore
from ..core.docker import ComposeManager
from ..core.manage_json import read_json, write_json
from ..core.manage_templates import template_to_file
from ..utils.cli import clear, confirm
from .custom_group import CustomGroup
from .menu import Menus

dicts = dict[str, Any]


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

            services: set[dicts] = set([])
            networks: set[str] = set([])
            envs: set[dicts] = set([])

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

            path: Path = self.cwd.joinpath("data.json")

            if not path.exists():
                exit(
                    "ERROR: Missing JSON file for services. Use 'create' first."
                )

            data: dicts = read_json(path) or {}
            compose: dicts = data.get("compose", {}) or {}

            services: list[dicts] = compose.get("services", []) or []
            networks: list[str] = compose.get("networks", []) or []
            envs: list[dicts] = data.get("envs", []) or []

            if not services:
                exit("ERROR: No services found. Use 'create' first.")

            def find_index_by_name(name: str) -> int | None:
                for i, s in enumerate(services):
                    if s.get("name") == name:
                        return i
                return None

            if remove:
                target = service
                if not target:
                    names = [s.get("name") for s in services if s.get("name")]
                    if not names:
                        exit("ERROR: No services found.")

                    target = inquirer.select(  # type: ignore
                        message="Select a service to remove: ", choices=names
                    ).execute()

                idx = find_index_by_name(target)  # type: ignore
                if idx is None:
                    exit(f"ERROR: Service '{target}' not found.")

                if confirm(msg=f"Remove service '{target}'"):
                    services.pop(idx)
                    envs = [
                        e for e in envs if e.get("CONTAINER_NAME") != target
                    ]
                    compose["services"] = services
                    compose["networks"] = networks
                    data["compose"] = compose
                    data["envs"] = envs
                    self.__save_files(data)
                    print(f"Service '{target}' removed and files updated.")

            elif add:
                name = service
                if not name:
                    name = self.__get_name("Enter the name of the service: ")
                if find_index_by_name(name):
                    if not confirm(
                        msg=f"Service '{name}' already exists. Overwrite? "
                    ):
                        exit("ERROR: Add cancelled.")

                    services = [s for s in services if s.get("name") != name]
                    envs = [e for e in envs if e.get("CONTAINER_NAME") != name]

                network = None
                if networks:
                    network = inquirer.select(  # type: ignore
                        message="Select a network: ", choices=networks
                    ).execute()
                menu = Menus(network=network)

                service_obj, env_obj = self.__get_data(menu, name)
                service_obj["name"] = name
                env_obj["CONTAINER_NAME"] = name

                services.append(service_obj)
                envs.append(env_obj)

                if confirm(msg=f"Add/Update service '{name}'"):
                    compose["services"] = services
                    compose["networks"] = networks
                    data["compose"] = compose
                    data["envs"] = envs
                    self.__save_files(data)
                    print(f"Service '{name}' removed and files updated.")

            else:
                print("Use --add or --remove flag.")
                print("Use --services [service] for faster output.")
                for s in services:
                    print(f" - {s.get("name")}")

        return Command(
            name=inspect.currentframe().f_code.co_name,  # type: ignore
            help=help,
            callback=callback,
            params=options,  # type: ignore
        )

    def build(self) -> Command:
        help = "Build the files for the containerization."
        options: list[Option] = []

        def callback() -> None:
            clear(0)

            path: Path = self.cwd.joinpath("data.json")

            if not path.exists():
                exit(
                    "ERROR: Missing JSON file for services. Use 'create' first."
                )

            data: dicts = read_json(path) or {}

            if not data:
                exit("ERROR: JSON file is empty. Use 'create' first.")

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
        self, menu: Menus, name: str | None = None
    ) -> tuple[dicts, dicts]:
        clear(0.5)

        if not name:
            name = self.__get_name(message="Enter the name of the service: ")

        service = menu.service(name=name)
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

    @yaspin(text="Saving files...", color="cyan")
    def __save_files(self, data: dicts, build: bool = False) -> None:
        tmps_path = files("minecraft-docker-cli.assets.templates")
        composer_template = tmps_path.joinpath("docker-compose.yml.j2")
        env_template = tmps_path.joinpath(".env.j2")

        if not build:
            write_json(self.cwd.joinpath("data.json"), data)

        composer: dicts = data.get("composer") or {}
        with as_file(composer_template) as composer_path:  # type: ignore
            composer_path = cast(Path, composer_path)
            template_to_file(
                composer_path, composer, self.cwd.joinpath("docker-compose.yml")
            )

        services: list[dicts] = composer.get("services", []) or []
        names: list[str] = [service.get("name") for service in services]  # type: ignore
        copy_files(self.cwd, names)

        envs: list[dicts] = data.get("envs") or []
        for env in envs:
            relative_path = f"servers/{env.get("CONTAINER_NAME")}/.env"  # type: ignore
            with as_file(env_template) as env_path:  # type: ignore
                env_path = cast(Path, env_path)
                template_to_file(
                    env_path, env, self.cwd.joinpath(relative_path)
                )
