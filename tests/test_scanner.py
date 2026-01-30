import os
import unittest
from repopilot.scanner import DirectoryScanner

class TestDirectoryScanner(unittest.TestCase):

    def setUp(self):
        self.scanner = DirectoryScanner()

    def test_scan_empty_directory(self):
        os.makedirs('test_empty_dir', exist_ok=True)
        result = self.scanner.scan('test_empty_dir')
        self.assertEqual(result, {})

    def test_scan_directory_with_files(self):
        os.makedirs('test_dir', exist_ok=True)
        with open('test_dir/file1.py', 'w') as f:
            f.write('# Sample Python file')
        with open('test_dir/file2.md', 'w') as f:
            f.write('# Sample Markdown file')
        
        result = self.scanner.scan('test_dir')
        expected = {
            'file1.py': 'file',
            'file2.md': 'file'
        }
        self.assertIn('file1.py', result)
        self.assertIn('file2.md', result)

    def tearDown(self):
        import shutil
        shutil.rmtree('test_empty_dir', ignore_errors=True)
        shutil.rmtree('test_dir', ignore_errors=True)

if __name__ == '__main__':
    unittest.main()