#################################################
# IMPORTS
#################################################
from __future__ import annotations

from click import group

from .cli.builder import Builder
from .cli.manager import Manager


#################################################
# CODE
#################################################
# Create the main group for the CLI
@group()
def cli() -> None:
    pass


# Add the two command groups
cli.add_command(Builder())
cli.add_command(Manager())


# Create the main entry point
def main() -> None:
    cli()


# Execute the programm
if __name__ == "__main__":
    main()
