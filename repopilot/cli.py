from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from repopilot.scanner import ProjectScanner, ScanOptions
from repopilot.analyzer import FileTypeAnalyzer
from repopilot.summarizer import Summarizer
from repopilot.report_generator import ReportGenerator
from repopilot.utils.file_utils import write_text


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="RepoPilot",
        description="RepoPilot - AI Powered Developer Workflow Assistant",
    )
    sub = p.add_subparsers(dest="command", required=True)

    scan = sub.add_parser("scan", help="Scan project folder")
    scan.add_argument("target", type=str, help="Target project folder")
    scan.add_argument("--max-depth", type=int, default=6)
    scan.add_argument("--max-files", type=int, default=5000)
    scan.add_argument("--include-hidden", action="store_true")
    scan.add_argument("--follow-symlinks", action="store_true")
    scan.add_argument("--output-dir", type=str, default="data")
    scan.add_argument("--write-readme", action="store_true")
    scan.add_argument("--save-readme-preview", action="store_true")

    return p


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "scan":
        return cmd_scan(args)

    print("[ERROR] Unknown command")
    return 2


def cmd_scan(args: argparse.Namespace) -> int:
    repo_root = Path(__file__).resolve().parent.parent
    output_dir = (repo_root / args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / "report.json"

    target = Path(args.target).expanduser().resolve()
    if not target.exists() or not target.is_dir():
        print(f"[ERROR] Target is not a directory: {target}")
        return 2

    options = ScanOptions(
        max_depth=args.max_depth,
        max_files=args.max_files,
        include_hidden=args.include_hidden,
        follow_symlinks=args.follow_symlinks,
        extra_ignore_dirs=None,
    )

    print("===== RepoPilot Scan =====")
    print(f"Target: {target}")
    print(f"Report: {report_path}")
    print("==========================")

    # Scan
    scanner = ProjectScanner()
    scan_res = scanner.scan(target, options)

    # Analyze
    analyzer = FileTypeAnalyzer()
    analysis_res = analyzer.analyze(scan_res.files)
    analysis_dict = {
        "total_files": analysis_res.total_files,
        "file_types": analysis_res.file_types,
        "top_types": analysis_res.top_types,
    }

    # Mock AI
    summarizer = Summarizer(
        project_name=target.name,
        project_structure=scan_res.structure,
        file_types_count=analysis_res.file_types,
    )
    summary = summarizer.generate_summary()

    payload: dict[str, Any] = {
        "target": str(target),
        "scan": {
            "root": str(scan_res.root),
            "dir_count": scan_res.dir_count,
            "file_count": scan_res.file_count,
            "tree": scan_res.tree_text,
        },
        "analysis": analysis_dict,
        "ai_summary": summary,
    }

    generator = ReportGenerator()
    report = generator.build_report(payload)
    generator.write_report_json(report_path, report)

    readme_text = generator.render_readme(
        project_name=target.name,
        tree_text=scan_res.tree_text,
        analysis=analysis_dict,
        summary=summary,
        usage_examples=[
            f"python main.py scan {target}",
            f"python main.py scan {target} --write-readme",
        ],
    )

    print("\n===== AI Summary =====")
    print(summary.get("description", ""))
    for i, m in enumerate(summary.get("modules", []), 1):
        print(f"{i}. {m}")

    print(f"\n[OK] Report written: {report_path}")

    if args.save_readme_preview:
        preview_path = output_dir / "README.preview.md"
        write_text(preview_path, readme_text)
        print(f"[OK] README preview saved: {preview_path}")

    if args.write_readme:
        written_path = generator.write_readme_to_target(target, readme_text)
        print(f"[OK] README written to target: {written_path}")
    else:
        print("\n===== README Preview =====")
        print(readme_text)

    print("[OK] Done.")
    return 0


