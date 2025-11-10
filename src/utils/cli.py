from __future__ import annotations

from os import name, system
from time import sleep

from InquirerPy import inquirer  # type: ignore


def clear(t: float) -> None:
    sleep(t)
    system("cls" if name == "nt" else "clear")


def confirm(msg: str, default: bool = False) -> bool:
    return inquirer.confirm(  # type: ignore
        message=msg, default=default
    ).execute()
