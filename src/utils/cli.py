#################################################
# IMPORTS
#################################################
from __future__ import annotations

from os import name, system
from time import sleep

from InquirerPy import inquirer  # type: ignore


#################################################
# CODE
#################################################
def clear(t: float) -> None:
    """
    Sleep t seconds and clear the console.
    """
    sleep(t)
    system("cls" if name == "nt" else "clear")


def confirm(msg: str, default: bool = True) -> bool:
    """
    Ask for confirmation with custom message and default value
    """
    return inquirer.confirm(  # type: ignore
        message=msg, default=default
    ).execute()
