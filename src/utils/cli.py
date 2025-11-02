from os import system, name
from time import sleep


def clear(t: float) -> None:
    sleep(t)
    system("cls" if name == "nt" else "clear")
