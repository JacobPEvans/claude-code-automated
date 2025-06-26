import pytest
from unittest.mock import MagicMock, AsyncMock

@pytest.fixture
def mock_anthropic_client():
    """Fixture for mocking the Anthropic client."""
    mock_client = MagicMock()
    mock_client.messages.batches.retrieve = AsyncMock()
    mock_client.messages.batches.results = MagicMock()

    # Mocking the async iterator for results
    async def async_iterator_mock(batch_id):
        yield MagicMock(
            custom_id='task_1',
            result=MagicMock(
                type='succeeded',
                message=MagicMock(
                    content=[MagicMock(text='Success')],
                    usage=MagicMock()
                )
            )
        )
        yield MagicMock(
            custom_id='task_2',
            result=MagicMock(
                type='failed',
                error='Failure'
            )
        )

    mock_client.messages.batches.results.side_effect = async_iterator_mock
    return mock_client
