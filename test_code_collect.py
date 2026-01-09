#!/usr/bin/env python3
"""
Unit tests for code-collect
Run with: python3 test_code_collect.py
"""

import unittest
import tempfile
import subprocess
from pathlib import Path
from unittest.mock import patch

# Import functions from code-collect
import sys
sys.path.insert(0, '.')
exec(open('code-collect').read().replace('if __name__ == \'__main__\':', 'if False:'))

class TestCodeCollect(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()
        self.base_path = Path(self.test_dir)
        
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.test_dir)
    
    def create_test_file(self, path, content="test content"):
        """Helper to create test files"""
        file_path = self.base_path / path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
        return file_path
    
    def test_is_text_file(self):
        """Test text file detection"""
        # Test known text extensions
        self.assertTrue(is_text_file(Path("test.py")))
        self.assertTrue(is_text_file(Path("test.js")))
        self.assertTrue(is_text_file(Path("test.md")))
        self.assertTrue(is_text_file(Path("test.json")))
        
        # Test non-text extensions
        self.assertFalse(is_text_file(Path("test.jpg")))
        self.assertFalse(is_text_file(Path("test.exe")))
        self.assertFalse(is_text_file(Path("test.bin")))
    
    def test_load_gitignore_patterns(self):
        """Test .gitignore pattern loading"""
        gitignore_content = """
# Comment
node_modules/
*.log
dist/
.env
"""
        self.create_test_file('.gitignore', gitignore_content)
        
        patterns = load_gitignore_patterns(self.base_path)
        expected_patterns = ['node_modules/', '*.log', 'dist/', '.env']
        self.assertEqual(patterns, expected_patterns)
    
    def test_load_gitignore_patterns_missing_file(self):
        """Test .gitignore loading when file doesn't exist"""
        patterns = load_gitignore_patterns(self.base_path)
        self.assertEqual(patterns, [])
    
    def test_matches_gitignore_pattern(self):
        """Test gitignore pattern matching"""
        patterns = ['node_modules/', '*.log', 'dist/', '.env']
        
        # Test directory patterns
        file1 = self.create_test_file('node_modules/package.json')
        self.assertTrue(matches_gitignore_pattern(file1, self.base_path, patterns))
        
        # Test glob patterns
        file2 = self.create_test_file('debug.log')
        self.assertTrue(matches_gitignore_pattern(file2, self.base_path, patterns))
        
        # Test exact match
        file3 = self.create_test_file('.env')
        self.assertTrue(matches_gitignore_pattern(file3, self.base_path, patterns))
        
        # Test non-matching file
        file4 = self.create_test_file('src/main.py')
        self.assertFalse(matches_gitignore_pattern(file4, self.base_path, patterns))
    
    def test_should_ignore_builtin_patterns(self):
        """Test built-in ignore patterns"""
        # Test built-in patterns
        file1 = self.create_test_file('.git/config')
        self.assertTrue(should_ignore(file1, self.base_path))
        
        file2 = self.create_test_file('__pycache__/module.pyc')
        self.assertTrue(should_ignore(file2, self.base_path))
        
        file3 = self.create_test_file('node_modules/package.json')
        self.assertTrue(should_ignore(file3, self.base_path))
        
        # Test non-ignored file
        file4 = self.create_test_file('src/main.py')
        self.assertFalse(should_ignore(file4, self.base_path))
    
    def test_should_ignore_with_gitignore(self):
        """Test ignore logic with gitignore patterns"""
        gitignore_patterns = ['*.log', 'temp/']
        
        # Test gitignore pattern
        file1 = self.create_test_file('debug.log')
        self.assertTrue(should_ignore(file1, self.base_path, gitignore_patterns))
        
        # Test directory pattern
        file2 = self.create_test_file('temp/file.txt')
        self.assertTrue(should_ignore(file2, self.base_path, gitignore_patterns))
        
        # Test non-ignored file
        file3 = self.create_test_file('src/main.py')
        self.assertFalse(should_ignore(file3, self.base_path, gitignore_patterns))
    
    def test_get_language_from_extension(self):
        """Test language detection from file extensions"""
        self.assertEqual(get_language_from_extension(Path("test.py")), "python")
        self.assertEqual(get_language_from_extension(Path("test.js")), "javascript")
        self.assertEqual(get_language_from_extension(Path("test.ts")), "typescript")
        self.assertEqual(get_language_from_extension(Path("test.md")), "markdown")
        self.assertEqual(get_language_from_extension(Path("test.unknown")), "")
    
    def test_format_file_content(self):
        """Test file content formatting"""
        test_content = "def hello():\n    return 'world'"
        file_path = self.create_test_file('src/test.py', test_content)
        
        formatted = format_file_content(file_path, self.base_path)
        expected = f"// src/test.py\n```python\n{test_content}\n```\n"
        self.assertEqual(formatted, expected)
    
    def test_get_files(self):
        """Test file discovery"""
        # Create test files
        self.create_test_file('src/main.py', 'print("hello")')
        self.create_test_file('src/utils.js', 'console.log("test")')
        self.create_test_file('README.md', '# Test')
        self.create_test_file('.git/config', 'git config')  # Should be ignored
        self.create_test_file('node_modules/package.json', '{}')  # Should be ignored
        
        files = get_files(self.test_dir)
        file_names = [f.name for f in files]
        
        # Should include text files
        self.assertIn('main.py', file_names)
        self.assertIn('utils.js', file_names)
        self.assertIn('README.md', file_names)
        
        # Should exclude ignored files
        self.assertNotIn('config', file_names)
        self.assertNotIn('package.json', file_names)
    
    @patch('subprocess.run')
    def test_get_git_modified_files(self, mock_run):
        """Test git modified files detection"""
        # Mock git diff output
        mock_run.return_value.stdout = "src/main.py\nREADME.md\n"
        mock_run.return_value.returncode = 0
        
        # Create the files that git reports as modified
        self.create_test_file('src/main.py')
        self.create_test_file('README.md')
        
        files = get_git_modified_files(self.base_path)
        file_names = [f.name for f in files]
        
        self.assertIn('main.py', file_names)
        self.assertIn('README.md', file_names)
        mock_run.assert_called_once()
    
    @patch('subprocess.run')
    def test_get_git_staged_files(self, mock_run):
        """Test git staged files detection"""
        # Mock git diff --cached output
        mock_run.return_value.stdout = "src/test.py\n"
        mock_run.return_value.returncode = 0
        
        # Create the file that git reports as staged
        self.create_test_file('src/test.py')
        
        files = get_git_staged_files(self.base_path)
        file_names = [f.name for f in files]
        
        self.assertIn('test.py', file_names)
        mock_run.assert_called_once()
    
    @patch('subprocess.run')
    def test_git_functions_handle_errors(self, mock_run):
        """Test git functions handle errors gracefully"""
        # Mock git command failure
        mock_run.side_effect = subprocess.CalledProcessError(1, 'git')
        
        files = get_git_modified_files(self.base_path)
        self.assertEqual(files, [])
        
        files = get_git_staged_files(self.base_path)
        self.assertEqual(files, [])
    
    def test_file_size_limit(self):
        """Test file size limits"""
        # Create a large file (over 1MB)
        large_content = "x" * (MAX_FILE_SIZE + 1)
        self.create_test_file('large.txt', large_content)
        
        # Create a normal file
        self.create_test_file('normal.txt', 'small content')
        
        files = get_files(self.test_dir)
        file_names = [f.name for f in files]
        
        # Should exclude large file
        self.assertNotIn('large.txt', file_names)
        # Should include normal file
        self.assertIn('normal.txt', file_names)

if __name__ == '__main__':
    print("🧪 Running code-collect unit tests...")
    unittest.main(verbosity=2)
