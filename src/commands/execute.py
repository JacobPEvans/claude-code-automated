import asyncio
import logging
from src.claude_api import get_llm_provider
from src.file_utils import read_file
from src.planning import parse_prompts_from_planning_md
from src.file_utils import write_batch_results
from src import config

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
        provider = get_llm_provider()
        requests = []
        for p in prompts_for_api:
            requests.append(
                {
                    "custom_id": p["custom_id"],
                    "method": "POST",
                    "url": "/v1/messages",
                    "body": {
                        "model": config.MODEL_NAME,
                        "max_tokens": config.MAX_TOKENS,
                        "system": "You are an expert Python developer. Implement complete, production-ready code with error handling, documentation, and tests.",
                        "messages": [{"role": "user", "content": p["content"]}],
                    },
                }
            )

        logging.info("Submitting batch request to Claude API...")
        batch = await provider.create_batch(requests=requests)
        logging.info(f"Batch request submitted. Batch ID: {batch.id}")

        logging.info("Waiting for batch to complete...")
        completed_batch = await provider.poll_batch(batch.id)

        if completed_batch:
            logging.info("Batch completed. Processing results...")
            results = await provider.process_batch_results(completed_batch.id)
            write_batch_results(results, args.output_dir)
            logging.info(f"Results saved to {args.output_dir}")
            if results["failed"]:
                logging.warning(f"{len(results['failed'])} tasks failed. Check the logs and results directory.")
        else:
            logging.error("Batch processing failed or was cancelled.")

    except Exception as e:
        logging.error(f"An error occurred during execution: {e}")
