from __future__ import annotations

from pathlib import Path
from typing import Any

import jinja2


def __render_template(template_path: Path, context: dict[Any, Any]) -> str:
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(template_path.parent))
    )
    template_obj = env.get_template(template_path.name)
    return template_obj.render(**context)


def template_to_file(template_path: Path, context: dict[Any, Any], dest_path: Path) -> Path:
    rendered = __render_template(template_path, context)
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_text(rendered, encoding="utf-8")
    return dest_path
