import json
import os
import unittest
from repopilot.report_generator import generate_report

class TestReportGenerator(unittest.TestCase):

    def setUp(self):
        self.test_data = {
            "project_name": "Test Project",
            "description": "This is a test project.",
            "file_types": {
                ".py": 5,
                ".js": 2,
                ".md": 1,
                ".json": 1,
                ".html": 0
            },
            "modules": [
                {"name": "module1", "description": "This is module 1."},
                {"name": "module2", "description": "This is module 2."}
            ]
        }
        self.output_file = 'data/report.json'

    def test_generate_report(self):
        generate_report(self.test_data)
        self.assertTrue(os.path.exists(self.output_file))

        with open(self.output_file, 'r') as f:
            report = json.load(f)

        self.assertEqual(report['project_name'], self.test_data['project_name'])
        self.assertEqual(report['description'], self.test_data['description'])
        self.assertEqual(report['file_types'], self.test_data['file_types'])
        self.assertEqual(report['modules'], self.test_data['modules'])

    def tearDown(self):
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

if __name__ == '__main__':
    unittest.main()