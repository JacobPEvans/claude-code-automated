import os
import asyncio
from anthropic import Anthropic

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def create_batch_requests(prompts):
    requests = []
    for i, prompt in enumerate(prompts):
        request = {
            "custom_id": f"request-{i}",
            "params": {
                "model": "claude-3-opus-20240229",
                "max_tokens": 4000,
                "messages": [{"role": "user", "content": prompt}]
            }
        }
        requests.append(request)
    return requests

async def poll_batch_completion(client, batch_id):
    initial_delay, max_delay, current_delay = 30, 300, 30

    while True:
        batch = await client.messages.batches.retrieve(batch_id)

        if batch.processing_status == "ended":
            return batch
        elif batch.processing_status == "failed":
            return None

        await asyncio.sleep(current_delay)
        current_delay = min(current_delay * 1.2, max_delay)

def process_batch_results(client, batch_id):
    results = {'succeeded': [], 'failed': [], 'canceled': [], 'expired': []}

    for result in client.messages.batches.results(batch_id):
        custom_id = result.custom_id

        if result.result.type == "succeeded":
            results['succeeded'].append({
                'custom_id': custom_id,
                'content': result.result.message.content[0].text,
                'usage': result.result.message.usage
            })
        else:
            results['failed'].append({
                'custom_id': custom_id,
                'error': result.result.error
            })

    return results
