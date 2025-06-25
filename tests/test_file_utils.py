import unittest
from unittest.mock import mock_open, patch
from src.file_utils import read_file, write_file, parse_tasks_from_planning_md, update_planning_md_with_prompts, parse_prompts_from_planning_md, write_batch_results

class TestFileUtils(unittest.TestCase):

    def test_read_file(self):
        m = mock_open(read_data="test content")
        with patch("builtins.open", m):
            content = read_file("any/path")
            self.assertEqual(content, "test content")

    def test_write_file(self):
        m = mock_open()
        with patch("builtins.open", m):
            write_file("any/path/to/file.txt", "test content")
            m.assert_called_once_with("any/path/to/file.txt", 'w', encoding='utf-8')
            m().write.assert_called_once_with("test content")

    def test_parse_tasks_from_planning_md(self):
        content = """### 📋 Remaining Tasks

- Task 1
- Task 2

## Next Section"""

        tasks = parse_tasks_from_planning_md(content)
        self.assertEqual(tasks, ["Task 1", "Task 2"])

    def test_update_planning_md_with_prompts(self):
        content = "## Generated Prompts\n\nold prompts"
        prompts = [{"id": 1}]
        new_content = update_planning_md_with_prompts(content, prompts)
        self.assertIn('"id": 1', new_content)
        self.assertNotIn("old prompts", new_content)

    def test_parse_prompts_from_planning_md(self):
        content = '''## Generated Prompts

```json
[{"id": 1}]
```'''
        prompts = parse_prompts_from_planning_md(content)
        self.assertEqual(prompts, [{"id": 1}])

    def test_write_batch_results(self):
        results = {
            'succeeded': [{'custom_id': 'task_1', 'content': 'content 1'}],
            'failed': []
        }
        m = mock_open()
        with patch("builtins.open", m):
            with patch("os.makedirs") as mock_makedirs:
                write_batch_results(results, "results_dir")
                mock_makedirs.assert_called_once_with("results_dir", exist_ok=True)
                m.assert_called_once_with("results_dir/task_1.txt", 'w', encoding='utf-8')
                m().write.assert_called_once_with("content 1")

if __name__ == '__main__':
    unittest.main()
