import os
import asyncio
import logging
from abc import ABC, abstractmethod
from anthropic import AsyncAnthropic, AnthropicError
from src import config

class LLMProvider(ABC):
    @abstractmethod
    async def create_batch(self, requests):
        pass

    @abstractmethod
    async def poll_batch(self, batch_id):
        pass

    @abstractmethod
    async def process_batch_results(self, batch_id):
        pass

class AnthropicProvider(LLMProvider):
    def __init__(self):
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set.")
        self.client = AsyncAnthropic(api_key=api_key)

    async def create_batch(self, requests):
        return await self.client.messages.batches.create(requests=requests)

    async def poll_batch(self, batch_id):
        current_delay = config.POLL_INITIAL_DELAY
        while True:
            try:
                batch = await self.client.messages.batches.retrieve(batch_id)
                logging.info(f"Batch {batch.id} status: {batch.processing_status}")

                if batch.processing_status == "ended":
                    logging.info(f"Batch {batch.id} completed successfully.")
                    return batch
                elif batch.processing_status == "failed":
                    logging.error(f"Batch {batch.id} failed. Error: {getattr(batch, 'error', 'N/A')}")
                    return None

                await asyncio.sleep(current_delay)
                current_delay = min(current_delay * config.POLL_FACTOR, config.POLL_MAX_DELAY)
            except AnthropicError as e:
                logging.error(f"An API error occurred while polling batch {batch_id}: {e}")
                return None
            except Exception as e:
                logging.error(f"An unexpected error occurred while polling batch {batch_id}: {e}")
                return None

    async def process_batch_results(self, batch_id):
        results = {'succeeded': [], 'failed': []}
        try:
            async for result in self.client.messages.batches.results(batch_id):
                custom_id = result.custom_id
                if hasattr(result, 'result') and result.result.type == "succeeded":
                    results['succeeded'].append({
                        'custom_id': custom_id,
                        'content': result.result.message.content[0].text,
                        'usage': result.result.message.usage
                    })
                else:
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
