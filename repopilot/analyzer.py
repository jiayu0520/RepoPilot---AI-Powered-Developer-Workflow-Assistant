from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AnalyzerResult:
    total_files: int
    file_types: dict[str, int]
    top_types: list[tuple[str, int]]


class FileTypeAnalyzer:
    """
    Count file extensions: .py .js .md .json .html ...
    """

    def analyze(self, files: list[Path]) -> AnalyzerResult:
        c: Counter[str] = Counter()

        for p in files:
            ext = p.suffix.lower().strip()
            if not ext:
                ext = "(no_ext)"
            elif not ext.startswith("."):
                ext = "." + ext
            c[ext] += 1

        sorted_items = sorted(c.items(), key=lambda x: (-x[1], x[0]))
        return AnalyzerResult(
            total_files=sum(c.values()),
            file_types=dict(sorted_items),
            top_types=sorted_items[:10],
        )

