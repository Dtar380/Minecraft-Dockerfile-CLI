from click import group

from .cli.builder import Builder
from .cli.manager import Manager


@group()
def cli() -> None:
    pass

cli.add_command(Builder())
cli.add_command(Manager())


def main() -> None:
    cli()


if __name__ == "__main__":
    main()
