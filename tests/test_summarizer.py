import unittest
from repopilot.summarizer import generate_summary

class TestSummarizer(unittest.TestCase):

    def setUp(self):
        self.project_structure = {
            'name': 'Sample Project',
            'description': 'This is a sample project for testing.',
            'modules': {
                'module1': 'Handles user authentication',
                'module2': 'Processes data and generates reports'
            }
        }

    def test_generate_summary(self):
        summary = generate_summary(self.project_structure)
        self.assertIn('Sample Project', summary)
        self.assertIn('This is a sample project for testing.', summary)
        self.assertIn('Handles user authentication', summary)
        self.assertIn('Processes data and generates reports', summary)

if __name__ == '__main__':
    unittest.main()