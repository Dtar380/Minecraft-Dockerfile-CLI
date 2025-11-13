from __future__ import annotations

from pathlib import Path
from subprocess import CompletedProcess, run
from time import strftime
from typing import Any

from yaspin import yaspin

from .files import FileManager


class ComposeManager:

    def __init__(self) -> None:
        self.composer_file = Path.cwd().joinpath("docker-compose.yml")
        if not self.composer_file.exists():
            exit(
                "ERROR: docker-compose.yml was not located in current directory."
            )
        self.file_manager = FileManager()

    def __run(
        self, *args: str, capture_output: bool = False
    ) -> CompletedProcess[str]:
        command = ["docker", "compose", "-f", str(self.composer_file), *args]
        result = run(command, text=True, capture_output=capture_output)
        if result.returncode != 0:
            print("ERROR:\n", result.stderr)
        else:
            print("Command run:\n", result.stdout)
        return result

    @yaspin("Building Container...", color="cyan")
    def build(
        self, no_cache: bool = False, pull: bool = False
    ) -> CompletedProcess[str]:
        args = ["build"]
        if no_cache:
            args.append("--no-cache")
        if pull:
            args.append("--pull")
        return self.__run(*args)

    @yaspin("Stopping Services...", color="cyan")
    def stop(self) -> CompletedProcess[str]:
        return self.__run("stop")

    @yaspin("Starting Services...", color="cyan")
    def start(self) -> CompletedProcess[str]:
        return self.__run("start")

    @yaspin("Removing Container...", color="cyan")
    def down(self, remove_volumes: bool = False) -> CompletedProcess[str]:
        args = ["down"]
        if remove_volumes:
            args.append("-v")
        return self.__run(*args)

    @yaspin("Putting Up Container...", color="cyan")
    def up(self, detached: bool = True) -> CompletedProcess[str]:
        args = ["up"]
        if detached:
            args.append("-d")
        return self.__run(*args)

    @yaspin("Backing Up Container...", color="cyan")
    def back_up(self, cwd: Path = Path.cwd()) -> None:
        backup_path = cwd.joinpath(".backup")
        compose_json = cwd.joinpath("data.json")

        backup_path.mkdir(exist_ok=True)
        data: dict[str, Any] = self.file_manager.read_json(compose_json)
        services = data.get("composer", {}).get("services", []) or []
        names: list[str] = [svc.get("name") for svc in services if svc.get("name") is not None]  # type: ignore
        for svc_name in names:
            container_path = svc_name
            tar_file = backup_path.joinpath(
                f"{svc_name}_{strftime("%d-%m-%Y_%H:%M:%S")}.tar.gz"
            )
            container_name = self.__get_container_name(svc_name)
            if container_name:
                run(
                    [
                        "docker",
                        "compose",
                        "cp",
                        f"{container_name}:{container_path}",
                        tar_file,
                    ],
                    check=True,
                )

    def __get_container_name(self, service_name: str) -> str | None:
        result = self.__run("ps", capture_output=True)
        lines = result.stdout.splitlines()
        for line in lines[2:]:  # skip header
            if service_name in line:
                return line.split()[0]
        return None
