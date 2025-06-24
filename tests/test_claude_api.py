import unittest
from unittest.mock import patch, MagicMock, AsyncMock
from src.claude_api import get_anthropic_client, poll_batch_completion, process_batch_results

class TestClaudeApi(unittest.IsolatedAsyncioTestCase):

    @patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test_api_key', 'SSL_CERT_FILE': '/etc/ssl/certs/ca-certificates.crt'})
    def test_get_anthropic_client(self):
        from anthropic import AsyncAnthropic # Import here to re-evaluate with mock
        client = get_anthropic_client()
        self.assertIsInstance(client, AsyncAnthropic)

    @patch('os.environ.get', return_value=None)
    def test_get_anthropic_client_no_key(self, mock_env_get):
        with self.assertRaises(ValueError):
            get_anthropic_client()

    async def test_poll_batch_completion(self):
        mock_client = MagicMock()
        mock_client.messages = MagicMock()
        mock_client.messages.batches = MagicMock()
        mock_client.messages.batches.retrieve = AsyncMock()

        mock_client.messages.batches.retrieve.side_effect = [
            MagicMock(processing_status='processing'),
            MagicMock(processing_status='ended')
        ]

        with patch('asyncio.sleep', new_callable=AsyncMock):
            result = await poll_batch_completion(mock_client, 'batch_123')
            self.assertEqual(result.processing_status, 'ended')
            self.assertEqual(mock_client.messages.batches.retrieve.call_count, 2)

    async def test_process_batch_results(self):
        mock_client = MagicMock()
        mock_client.messages = MagicMock()
        mock_client.messages.batches = MagicMock()

        # Mocking an async iterator
        succeeded_result = MagicMock(custom_id='req1')
        succeeded_result.result.type = 'succeeded'
        succeeded_result.result.message.content = [MagicMock(text='Success')]
        succeeded_result.result.message.usage = MagicMock()
        failed_result = MagicMock(custom_id='req2')
        failed_result.result.type = 'failed'
        failed_result.result.error = 'Failure'

        async def mock_async_iterator(batch_id):
            yield succeeded_result
            yield failed_result

        mock_client.messages.batches.results = mock_async_iterator

        results = await process_batch_results(mock_client, 'batch_123')
        self.assertEqual(len(results['succeeded']), 1)
        self.assertEqual(results['succeeded'][0]['content'], 'Success')
        self.assertEqual(len(results['failed']), 1)
        self.assertEqual(results['failed'][0]['error'], 'Failure')

if __name__ == '__main__':
    unittest.main()
