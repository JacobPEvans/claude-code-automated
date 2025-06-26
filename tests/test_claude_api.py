import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from src.claude_api import get_anthropic_client, poll_batch_completion, process_batch_results
from anthropic import AsyncAnthropic

@patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test_api_key', 'SSL_CERT_FILE': '/etc/ssl/certs/ca-certificates.crt'})
def test_get_anthropic_client():
    client = get_anthropic_client()
    assert isinstance(client, AsyncAnthropic)

@patch('os.environ.get', return_value=None)
def test_get_anthropic_client_no_key(mock_env_get):
    with pytest.raises(ValueError):
        get_anthropic_client()

@pytest.mark.asyncio
async def test_poll_batch_completion(mock_anthropic_client):
    mock_anthropic_client.messages.batches.retrieve.side_effect = [
        MagicMock(processing_status='processing'),
        MagicMock(processing_status='ended')
    ]

    with patch('asyncio.sleep', new_callable=AsyncMock):
        result = await poll_batch_completion(mock_anthropic_client, 'batch_123')
        assert result.processing_status == 'ended'
        assert mock_anthropic_client.messages.batches.retrieve.call_count == 2

@pytest.mark.asyncio
async def test_process_batch_results(mock_anthropic_client):
    results = await process_batch_results(mock_anthropic_client, 'batch_123')
    assert len(results['succeeded']) == 1
    assert results['succeeded'][0]['content'] == 'Success'
    assert len(results['failed']) == 1
    assert results['failed'][0]['error'] == 'Failure'