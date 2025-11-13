from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

from importlib_resources import as_file, files  # type: ignore
import jinja2
from yaspin import yaspin  # type: ignore

dicts = dict[str, Any]


class FileManager:

    cwd = Path.cwd()

    def save_files(self, data: dicts, build: bool = False) -> None:
        tmps_path = files("minecraft-docker-cli.assets.templates")
        composer_template = tmps_path.joinpath("docker-compose.yml.j2")
        env_template = tmps_path.joinpath(".env.j2")

        if not build:
            self.write_json(self.cwd.joinpath("data.json"), data)

        composer: dicts = data.get("composer") or {}
        with as_file(composer_template) as composer_path:  # type: ignore
            composer_path = cast(Path, composer_path)
            self.template_to_file(
                composer_path, composer, self.cwd.joinpath("docker-compose.yml")
            )

        services: list[dicts] = composer.get("services", []) or []
        names: list[str] = [service.get("name") for service in services]  # type: ignore
        self.copy_files(self.cwd, names)

        envs: list[dicts] = data.get("envs") or []
        for env in envs:
            relative_path = f"servers/{env.get("CONTAINER_NAME")}/.env"  # type: ignore
            with as_file(env_template) as env_path:  # type: ignore
                env_path = cast(Path, env_path)
                self.template_to_file(
                    env_path, env, self.cwd.joinpath(relative_path)
                )

    @yaspin("Reading JSON...", color="cyan")
    def read_json(self, file: Path) -> dict[Any, Any]:
        with open(file, "r+") as f:
            data = dict(json.load(f))
        return data

    @yaspin("Writting JSON...", color="cyan")
    def write_json(self, file: Path, data: dict[Any, Any]) -> None:
        data_str = json.dumps(data, indent=2)
        with open(file, "w+") as f:
            f.write(data_str)
        return None

    @yaspin("Copying files...", color="cyan")
    def copy_files(self, path: Path, services: list[str]) -> None:
        docker_pkg = files("minecraft-docker-cli.assets.docker")
        dockerfile_res = docker_pkg.joinpath("Dockerfile")
        dockerignore_res = docker_pkg.joinpath(".dockerignore")
        runsh_res = files("minecraft-docker-cli.assets.scripts").joinpath(
            "run.sh"
        )
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

    @yaspin("Rendering template...", color="cyan")
    def template_to_file(
        self, template_path: Path, context: dict[Any, Any], dest_path: Path
    ) -> Path:
        rendered = self.__render_template(template_path, context)
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        dest_path.write_text(rendered, encoding="utf-8")
        return dest_path

    def __render_template(
        self, template_path: Path, context: dict[Any, Any]
    ) -> str:
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(template_path.parent))
        )
        template_obj = env.get_template(template_path.name)
        return template_obj.render(**context)
