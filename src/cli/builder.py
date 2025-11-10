from __future__ import annotations

import inspect
from pathlib import Path
from typing import Any

from InquirerPy import inquirer  # type: ignore
from InquirerPy.validator import EmptyInputValidator  # type: ignore
from click import Command, Option
from yaspin import yaspin  # type: ignore

from ..core.manage_json import read_json, write_json  # type: ignore
from ..core.manage_templates import template_to_file
from ..utils.cli import clear, confirm
from .custom_group import CustomGroup
from .menu import Menus


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

                    if not confirm(
                        msg=f"Want to continue adding services? (Count: {len(services)})",
                    ):
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

            if confirm(msg=f"Want to name this service '{name}'? "):
                break

        return name

    def __save_files(self, data: dict[str, Any]) -> None:
        write_json(Path(), data)

        composer: dict[str, Any] = data.get("composer") or {}
        template_to_file(Path(), composer, Path())

        envs: list[dict[str, Any]] = data.get("envs") or []
        for env in envs:
            template_to_file(Path(), env, Path())
