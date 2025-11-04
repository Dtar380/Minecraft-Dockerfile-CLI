from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def read_json(file: Path) -> dict[Any, Any]:
    with open(file, "r+") as f:
        data = dict(json.load(f))
    return data


def write_json(file: Path, data: dict[Any, Any]) -> None:
    data_str = json.dumps(data, indent=2)
    with open(file, "w+") as f:
        f.write(data_str)
    return None
