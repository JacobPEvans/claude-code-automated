import asyncio
import logging
from src.claude_api import get_anthropic_client, poll_batch_completion, process_batch_results
from src.file_utils import read_file, parse_prompts_from_planning_md, write_batch_results

async def execute_command(args):
    """
    Executes the prompts from PLANNING.md using the Claude Batch API.
    """
    logging.info(f"Executing prompts from: {args.planning_file}")
    content = read_file(args.planning_file)
    if not content:
        logging.error(f"Could not read planning file: {args.planning_file}")
        return

    prompts_for_api = parse_prompts_from_planning_md(content)
    if not prompts_for_api:
        logging.error("No prompts found in the planning file. Run 'plan' first.")
        return

    logging.info(f"Found {len(prompts_for_api)} prompts to execute.")

    try:
        client = get_anthropic_client()
        requests = []
        for p in prompts_for_api:
            requests.append(
                {
                    "custom_id": p["custom_id"],
                    "method": "POST",
                    "url": "/v1/messages",
                    "body": {
                        "model": "claude-3-opus-20240229",
                        "max_tokens": 4096,
                        "system": "You are an expert Python developer. Implement complete, production-ready code with error handling, documentation, and tests.",
                        "messages": [{"role": "user", "content": p["content"]}],
                    },
                }
            )

        logging.info("Submitting batch request to Claude API...")
        batch = await client.messages.batches.create(requests=requests)
        logging.info(f"Batch request submitted. Batch ID: {batch.id}")

        logging.info("Waiting for batch to complete...")
        completed_batch = await poll_batch_completion(client, batch.id)

        if completed_batch:
            logging.info("Batch completed. Processing results...")
            results = await process_batch_results(client, completed_batch.id)
            write_batch_results(results, args.output_dir)
            logging.info(f"Results saved to {args.output_dir}")
            if results["failed"]:
                logging.warning(f"{len(results['failed'])} tasks failed. Check the logs and results directory.")
        else:
            logging.error("Batch processing failed or was cancelled.")

    except Exception as e:
        logging.error(f"An error occurred during execution: {e}")
