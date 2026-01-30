from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class SummaryResult:
    project_name: str
    description: str
    modules: List[str]
    file_types: Dict[str, int]
    notes: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "project_name": self.project_name,
            "description": self.description,
            "modules": self.modules,
            "file_types": self.file_types,
            "notes": self.notes,
        }


class Summarizer:
    """
    A simple mock-AI summarizer.

    It receives:
      - project_name (str)
      - project_structure (any; usually dict/tree)
      - file_types_count (dict or Counter)

    It returns a dict (JSON serializable) or SummaryResult-like data.
    """

    def __init__(self, project_name: str, project_structure: Any, file_types_count: Any) -> None:
        self.project_name = project_name
        self.project_structure = project_structure
        self.file_types_count = dict(file_types_count) if file_types_count is not None else {}

    def generate_summary(self) -> Dict[str, Any]:
        file_types = self.file_types_count
        nature = self._infer_nature(file_types)
        top_types = self._top_exts(file_types, top_n=5)

        description = (
            f"「{self.project_name}」推測是一個 {nature} 專案。"
            f"主要檔案類型：{', '.join([f'{k}({v})' for k, v in top_types]) if top_types else '無'}。"
        )

        modules = self._infer_modules(file_types, self.project_structure)

        result = SummaryResult(
            project_name=self.project_name,
            description=description,
            modules=modules,
            file_types=file_types,
            notes=[
                "此為 Mock AI 分析（規則推論），可替換成真實 AI API。",
                "建議保留 Summarizer 的輸出 schema，以方便 report/README 自動化。",
            ],
        )
        return result.to_dict()

    def _infer_nature(self, ft: Dict[str, int]) -> str:
        has_py = ft.get(".py", 0) > 0
        has_js = ft.get(".js", 0) > 0 or ft.get(".ts", 0) > 0
        has_html = ft.get(".html", 0) > 0
        has_md = ft.get(".md", 0) > 0
        has_json = ft.get(".json", 0) > 0

        if has_py and not has_js:
            return "Python 工具/應用"
        if has_js and has_html:
            return "Web/前端應用"
        if has_py and has_js:
            return "多語言/全端整合"
        if has_md and has_json and not (has_py or has_js):
            return "文件/設定導向"
        return "通用軟體"

    def _infer_modules(self, ft: Dict[str, int], structure: Any) -> List[str]:
        modules: List[str] = []
        if ft.get(".py", 0) > 0:
            modules.append("核心程式模組：Python 原始碼（可能含 CLI / service / scripts）")
        if ft.get(".js", 0) > 0 or ft.get(".ts", 0) > 0:
            modules.append("前端/腳本模組：JavaScript/TypeScript")
        if ft.get(".md", 0) > 0:
            modules.append("文件模組：Markdown 文件（README/規格/說明）")
        if ft.get(".json", 0) > 0:
            modules.append("設定/資料模組：JSON 設定或資料")
        if ft.get(".html", 0) > 0 or ft.get(".css", 0) > 0:
            modules.append("介面模組：HTML/CSS 靜態頁面或模板")

        # simple structure hint
        if isinstance(structure, dict):
            children = structure.get("children", [])
            has_tests = any(isinstance(c, dict) and c.get("name") in ("tests", "test") for c in children)
            if has_tests:
                modules.append("測試模組：可能包含單元測試/驗證流程")

        if not modules:
            modules.append("模組資訊不足：檔案類型不足以推論（專案可能很小或以資料為主）")
        return modules

    def _top_exts(self, ft: Dict[str, int], top_n: int = 5) -> List[tuple[str, int]]:
        return sorted(ft.items(), key=lambda x: (-x[1], x[0]))[:top_n]

        
