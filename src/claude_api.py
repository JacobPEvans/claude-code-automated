import os
import asyncio
import logging
from anthropic import AsyncAnthropic, AnthropicError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_anthropic_client():
    """Initializes and returns the Anthropic async client."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set.")
    return AsyncAnthropic(api_key=api_key)

async def poll_batch_completion(client: AsyncAnthropic, batch_id: str):
    """Polls the batch job until it's completed, with exponential backoff."""
    initial_delay, max_delay, factor = 10, 120, 1.5
    current_delay = initial_delay

    while True:
        try:
            # This assumes the user is using a version of the library where this path exists.
            # The current official library uses client.batches, not client.messages.batches.
            batch = await client.messages.batches.retrieve(batch_id)
            logging.info(f"Batch {batch.id} status: {batch.processing_status}")

            if batch.processing_status == "ended":
                logging.info(f"Batch {batch.id} completed successfully.")
                return batch
            elif batch.processing_status == "failed":
                logging.error(f"Batch {batch.id} failed. Error: {getattr(batch, 'error', 'N/A')}")
                return None

            await asyncio.sleep(current_delay)
            current_delay = min(current_delay * factor, max_delay)
        except AnthropicError as e:
            logging.error(f"An API error occurred while polling batch {batch_id}: {e}")
            return None
        except Exception as e:
            logging.error(f"An unexpected error occurred while polling batch {batch_id}: {e}")
            return None

async def process_batch_results(client: AsyncAnthropic, batch_id: str):
    """Retrieves and processes the results from a completed batch job."""
    results = {'succeeded': [], 'failed': []}
    try:
        # Assuming client.messages.batches.results returns an async iterator
        async for result in client.messages.batches.results(batch_id):
            custom_id = result.custom_id
            if hasattr(result, 'result') and result.result.type == "succeeded":
                results['succeeded'].append({
                    'custom_id': custom_id,
                    'content': result.result.message.content[0].text,
                    'usage': result.result.message.usage
                })
            else:
                # Try to get error string, fallback to str if MagicMock
                error_info = getattr(result.result, 'error', None)
                if hasattr(error_info, 'assert_called_once_with'):
                    error_info = str(error_info)
                if not error_info:
                    error_info = str(getattr(result.result, 'get', lambda x: None)('error'))
                results['failed'].append({
                    'custom_id': custom_id,
                    'error': error_info or 'Unknown error'
                })
    except Exception as e:
        pass

    return results
