from __future__ import annotations

import json
from pathlib import Path
from typing import Any


DEFAULT_IGNORE_DIRS = {
    ".git", ".hg", ".svn",
    "__pycache__", ".pytest_cache", ".mypy_cache",
    "node_modules", ".venv", "venv", ".idea", ".vscode",
    "dist", "build",
}


def is_hidden_path(path: Path) -> bool:
    return any(part.startswith(".") for part in path.parts)


def should_ignore_dir(name: str) -> bool:
    return name in DEFAULT_IGNORE_DIRS


def safe_iterdir(p: Path) -> list[Path]:
    try:
        return list(p.iterdir())
    except (PermissionError, FileNotFoundError, OSError):
        return []


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
