from __future__ import annotations

from os import name, system
from time import sleep


def clear(t: float) -> None:
    sleep(t)
    system("cls" if name == "nt" else "clear")
