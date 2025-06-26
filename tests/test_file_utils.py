import pytest
from src.file_utils import (
    read_file,
    write_file,
    write_batch_results
)

def test_read_file(tmp_path):
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("test content")
    content = read_file(str(file_path))
    assert content == "test content"

def test_write_file(tmp_path):
    file_path = tmp_path / "test_file.txt"
    write_file(str(file_path), "test content")
    assert file_path.read_text() == "test content"

def test_write_batch_results(tmp_path):
    results = {
        'succeeded': [{'custom_id': 'task_1', 'content': 'content 1'}],
        'failed': []
    }
    results_dir = tmp_path / "results"
    write_batch_results(results, str(results_dir))
    expected_file = results_dir / "succeeded" / "task_1.txt"
    assert expected_file.exists()
    assert expected_file.read_text() == "content 1"
