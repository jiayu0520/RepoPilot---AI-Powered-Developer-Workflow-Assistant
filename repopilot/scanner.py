from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


# Common directories to ignore in project scanning
DEFAULT_IGNORE_DIRS = {
    ".git", ".hg", ".svn",
    "__pycache__", ".pytest_cache", ".mypy_cache",
    "node_modules", ".venv", "venv", ".idea", ".vscode",
    "dist", "build",
}


def safe_iterdir(p: Path) -> list[Path]:
    """
    Safely list directory entries. Avoid crashing on permission errors.
    """
    try:
        return list(p.iterdir())
    except (PermissionError, FileNotFoundError, OSError):
        return []


def is_hidden_path(path: Path) -> bool:
    """
    Treat any path component starting with '.' as hidden.
    """
    return any(part.startswith(".") for part in path.parts)


def should_ignore_dir(name: str) -> bool:
    return name in DEFAULT_IGNORE_DIRS


@dataclass(frozen=True)
class ScanOptions:
    """
    Scan configuration.
    """
    max_depth: int = 6
    max_files: int = 5000
    include_hidden: bool = False
    follow_symlinks: bool = False
    extra_ignore_dirs: list[str] | None = None


@dataclass
class ScanResult:
    """
    Output of scanning:
    - tree_text: text tree for CLI/README
    - files: file list for analyzer
    - structure: nested dict for summarizer/mock AI
    """
    root: Path
    tree_text: str
    files: list[Path]
    dir_count: int
    file_count: int
    structure: dict[str, Any]


class ProjectScanner:
    """
    Recursively scan a project directory.

    Features:
    - Depth-limited tree output
    - Safety file limit
    - Hidden file/folder control
    - Symlink following control
    - Ignore common dirs (node_modules, .git, venv...)
    """

    def scan(self, root: Path, options: ScanOptions) -> ScanResult:
        root = root.resolve()

        # Safety checks
        if not root.exists() or not root.is_dir():
            raise ValueError(f"Target root is not a directory: {root}")

        ignore_dirs = set(DEFAULT_IGNORE_DIRS)
        if options.extra_ignore_dirs:
            ignore_dirs |= set(options.extra_ignore_dirs)

        files: list[Path] = []
        dir_count = 1  # include root

        # nested structure for mock AI
        structure: dict[str, Any] = {"name": root.name, "type": "dir", "children": []}

        lines: list[str] = [f"{root.name}/"]

        def include_path(p: Path) -> bool:
            """
            Decide whether to include a path based on hidden rule.
            """
            if options.include_hidden:
                return True

            try:
                rel = p.relative_to(root)
            except ValueError:
                # if relative_to fails, include by default
                return True

            return not is_hidden_path(rel)

        def list_entries(cur: Path) -> list[Path]:
            """
            Get sorted entries, filtering ignored dirs & hidden paths.
            """
            entries = safe_iterdir(cur)
            filtered: list[Path] = []

            for e in entries:
                if not include_path(e):
                    continue

                if e.is_dir():
                    if e.name in ignore_dirs:
                        continue

                filtered.append(e)

            # stable output: dirs first, then files; alphabetically
            filtered.sort(key=lambda x: (not x.is_dir(), x.name.lower()))
            return filtered

        def build_tree(cur: Path, prefix: str, depth: int, struct_node: dict[str, Any]) -> None:
            """
            Recursive builder for tree_text + structure + file list.
            """
            nonlocal dir_count, files

            if depth > options.max_depth:
                lines.append(prefix + "└── … (max depth reached)")
                struct_node["children"].append({"name": "…", "type": "note", "reason": "max depth reached"})
                return

            entries = list_entries(cur)
            for idx, p in enumerate(entries):
                is_last = idx == len(entries) - 1
                branch = "└── " if is_last else "├── "
                next_prefix = prefix + ("    " if is_last else "│   ")

                display = p.name + ("/" if p.is_dir() else "")
                if p.is_symlink():
                    display += " (symlink)"

                lines.append(prefix + branch + display)

                if p.is_dir():
                    dir_count += 1
                    child_struct = {"name": p.name, "type": "dir", "children": []}
                    struct_node["children"].append(child_struct)

                    # symlink handling
                    if p.is_symlink() and not options.follow_symlinks:
                        child_struct["note"] = "symlink skipped (follow_symlinks=False)"
                        continue

                    build_tree(p, next_prefix, depth + 1, child_struct)

                else:
                    files.append(p)
                    struct_node["children"].append({"name": p.name, "type": "file"})

                    if len(files) >= options.max_files:
                        lines.append(next_prefix + "└── … (max files reached)")
                        struct_node["children"].append({"name": "…", "type": "note", "reason": "max files reached"})
                        return

        build_tree(root, prefix="", depth=1, struct_node=structure)

        return ScanResult(
            root=root,
            tree_text="\n".join(lines),
            files=files,
            dir_count=dir_count,
            file_count=len(files),
            structure=structure,
        )


