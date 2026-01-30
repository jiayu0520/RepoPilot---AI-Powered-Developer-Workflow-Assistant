import unittest
from repopilot.analyzer import Analyzer

class TestAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = Analyzer()

    def test_count_file_types(self):
        test_directory = {
            'file1.py': 'content',
            'file2.js': 'content',
            'file3.md': 'content',
            'file4.json': 'content',
            'file5.html': 'content',
            'file6.txt': 'content'
        }
        expected_counts = {
            '.py': 1,
            '.js': 1,
            '.md': 1,
            '.json': 1,
            '.html': 1,
            '.txt': 0
        }
        counts = self.analyzer.count_file_types(test_directory)
        self.assertEqual(counts, expected_counts)

    def test_empty_directory(self):
        test_directory = {}
        expected_counts = {
            '.py': 0,
            '.js': 0,
            '.md': 0,
            '.json': 0,
            '.html': 0,
            '.txt': 0
        }
        counts = self.analyzer.count_file_types(test_directory)
        self.assertEqual(counts, expected_counts)

if __name__ == '__main__':
    unittest.main()