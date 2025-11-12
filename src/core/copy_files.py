from __future__ import annotations

from pathlib import Path
from shutil import copyfile


def copy_files(path: Path, services: list[str]) -> None:
    for service in services:
        copyfile(Path(), path.joinpath(f"servers/{service}"))  # Dockerfile
        copyfile(Path(), path.joinpath(f"servers/{service}"))  # .dockerignore
        copyfile(Path(), path.joinpath(f"servers/{service}"))  # run.sh
    copyfile(Path(), path)  # README.md
