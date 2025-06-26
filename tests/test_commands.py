import pytest
from unittest.mock import patch, MagicMock, AsyncMock
import argparse
from src.commands.plan import plan_command
from src.commands.execute import execute_command
from src.commands.update import update_command

@patch('src.commands.plan.read_file', return_value='### 📋 Remaining Tasks\n- task 1')
@patch('src.commands.plan.write_file')
def test_plan_command(mock_write_file, mock_read_file):
    args = argparse.Namespace(planning_file='plan.md', output_file=None)
    plan_command(args)
    mock_read_file.assert_called_once_with('plan.md')
    mock_write_file.assert_called_once()

@pytest.mark.asyncio
@patch('src.commands.execute.get_anthropic_client')
@patch('src.commands.execute.read_file', return_value='## Generated Prompts\n\n```json\n[{"custom_id": "1", "content": "test content"}]\n```')
@patch('src.commands.execute.poll_batch_completion', new_callable=AsyncMock)
@patch('src.commands.execute.process_batch_results', new_callable=AsyncMock)
@patch('src.commands.execute.write_batch_results')
async def test_execute_command(mock_write_results, mock_process, mock_poll, mock_read_file, mock_get_client):
    mock_client = MagicMock()
    mock_client.messages.batches.create = AsyncMock(return_value=MagicMock(id='batch_123'))
    mock_get_client.return_value = mock_client

    mock_poll.return_value = MagicMock(id='batch_123')
    mock_process.return_value = {'succeeded': [], 'failed': []}

    args = argparse.Namespace(planning_file='plan.md', output_dir='results')
    await execute_command(args)

    mock_read_file.assert_called_once_with('plan.md')
    mock_get_client.assert_called_once()
    mock_client.messages.batches.create.assert_called_once()
    mock_poll.assert_called_once()
    mock_process.assert_called_once()
    mock_write_results.assert_called_once()

@patch('os.path.isdir', return_value=True)
@patch('os.listdir', return_value=['result1.txt'])
@patch('src.commands.update.read_file', return_value='# src/test.py\nprint("hello")')
@patch('src.commands.update.write_file')
def test_update_command(mock_write_file, mock_read_file, mock_listdir, mock_isdir):
    args = argparse.Namespace(project_dir='.', results_dir='results')
    update_command(args)
    mock_isdir.assert_called_with('results/succeeded')
    mock_listdir.assert_called_with('results/succeeded')
    mock_read_file.assert_called_with('results/succeeded/result1.txt')
    mock_write_file.assert_called_with('./src/test.py', 'print("hello")')