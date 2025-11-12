from __future__ import annotations

from pathlib import Path
from typing import Iterable

from importlib_resources import files  # type: ignore


def copy_files(path: Path, services: list[str] | Iterable[str]) -> None:
    # Resolve resource traversables
    docker_pkg = files("minecraft-docker-cli.assets.docker")
    dockerfile_res = docker_pkg.joinpath("Dockerfile")
    dockerignore_res = docker_pkg.joinpath(".dockerignore")
    runsh_res = files("minecraft-docker-cli.assets.scripts").joinpath("run.sh")
    readme_res = files("minecraft-docker-cli.assets").joinpath("README.md")

    # Ensure base path exists
    if not path.exists():
        raise ValueError("Path doesnt exist")

    # Read bytes from resources once
    dockerfile_bytes = dockerfile_res.read_bytes()
    dockerignore_bytes = dockerignore_res.read_bytes()
    runsh_bytes = runsh_res.read_bytes()
    readme_bytes = readme_res.read_bytes()

    # Write files for each service
    for service in services:
        dest_dir = path.joinpath("servers", service)
        dest_dir.mkdir(parents=True, exist_ok=True)

        (dest_dir / "Dockerfile").write_bytes(dockerfile_bytes)
        (dest_dir / ".dockerignore").write_bytes(dockerignore_bytes)
        (dest_dir / "run.sh").write_bytes(runsh_bytes)

    # Write top-level README into the given path
    (path / "README.md").write_bytes(readme_bytes)
