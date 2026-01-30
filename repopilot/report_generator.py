import json
import os

class ReportGenerator:
    def __init__(self, project_summary, file_analysis):
        self.project_summary = project_summary
        self.file_analysis = file_analysis

    def generate_report(self):
        report = {
            "project_summary": self.project_summary,
            "file_analysis": self.file_analysis
        }
        return report

    def save_report(self, report, output_path='data/report.json'):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as report_file:
            json.dump(report, report_file, indent=4)

def create_report(project_summary, file_analysis):
    report_generator = ReportGenerator(project_summary, file_analysis)
    report = report_generator.generate_report()
    report_generator.save_report(report)