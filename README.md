# Minecraft Docker CLI

An easy and fast way to set up a Minecraft server or network using Docker containers. This repository provides a small command-line interface (CLI) to create scaffold files, build container definitions, and manage the lifecycle of your Minecraft services using Docker Compose.

## **Installation**

**Prerequisites:**
- Docker Engine (Docker Desktop on Windows) running and configured.
- Docker Compose (bundled with modern Docker Desktop installations).
- Python 3.13+ and `pip`.

**Recommended Installation:**

```powershell
# Create a Virtual Environment
python3 -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install the python package
pip install MinecraftDockerCLI
```
<br>

**Clone repo:**

Extra requirement: `Poetry`.

```powershell
# Clone the repository
git clone https://github.com/Dtar380/Minecraft-Dockerfile-CLI.git
cd Minecraft-Dockerfile-CLI

poetry install
```

> [!NOTE]
> When running the program you would need to be using the poetry environment and run it like `poetry run MinecraftDockerCLI`

## **Usage**

This project provides two main CLI areas (examples below assume running via `python -m src` or after installation via package entrypoint):

- Builder commands — create and update service templates and environment files.
- Manager commands — run, stop and manage containers.

Common examples:

```powershell
# Create scaffolding for a single service (interactive)
python -m src builder create

# Build files from existing `data.json`
python -m src builder build

# Add or remove services from an existing configuration
python -m src builder update --add --service my_service
python -m src builder update --remove --service my_service

# Start containers (first-time):
python -m src manager up --detached

# Stop services
python -m src manager stop

# Tear down and remove volumes
python -m src manager down --rm-volumes

# Open a service terminal (interactive prompt or pass --service)
python -m src manager open_terminal --service my_service
```

Where files are saved and read:
- The CLI saves configuration and intermediate files to the current working directory (for example `data.json`). Keep your project folder where you run the commands.

**Tips & Troubleshooting**

- Ensure Docker Desktop is running and you can run `docker ps` without errors before invoking the CLI.
- On Windows, run PowerShell as Administrator or ensure your user has permissions for Docker.
- If interactive prompts fail, confirm `InquirerPy` was installed (`pip install InquirerPy`).
- If `data.json` is missing, run `builder create` first to scaffold services.

**Contributing**

Contributions are welcome. Please open issues for bugs or feature requests, and submit pull requests for fixes or enhancements.

**License**

This project is licensed under the terms in the `LICENSE` file in the repository root.
