import argparse
from repopilot.scanner import Scanner
from repopilot.analyzer import Analyzer
from repopilot.summarizer import Summarizer
from repopilot.report_generator import ReportGenerator

def main():
    parser = argparse.ArgumentParser(description="RepoPilot - AI Powered Developer Workflow Assistant")
    parser.add_argument('command', choices=['scan'], help='Command to execute')
    parser.add_argument('target', help='Target project directory to scan')

    args = parser.parse_args()

    if args.command == 'scan':
        scanner = Scanner(args.target)
        structure = scanner.scan_directory()
        
        analyzer = Analyzer(structure)
        file_types_count = analyzer.analyze_file_types()
        
        summarizer = Summarizer(file_types_count)
        project_summary = summarizer.generate_summary()
        
        report_generator = ReportGenerator(project_summary)
        report_generator.generate_report()

        print("Scan complete. Report generated.")

if __name__ == "__main__":
    main()