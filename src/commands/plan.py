import logging
from src.file_utils import read_file, write_file
from src.planning import parse_tasks_from_planning_md, update_planning_md_with_prompts
from src import config

def plan_command(args):
    """
    Reads tasks from PLANNING.md, converts them into prompts,
    and updates PLANNING.md with the generated prompts.
    """
    logging.info(f"Starting plan generation from: {args.planning_file}")
    content = read_file(args.planning_file)
    if not content:
        logging.error(f"Could not read planning file: {args.planning_file}")
        return

    tasks = parse_tasks_from_planning_md(content)
    if not tasks:
        logging.warning("No new tasks found in the planning file.")
        return

    logging.info(f"Found {len(tasks)} tasks to process.")

    prompts = []
    for i, task in enumerate(tasks):
        prompt = {
            "custom_id": f"task_{i}_{task[:20].replace(' ', '_')}",
            "content": f"CONTEXT: Complete the following task for the `claude-code-automated` project.\nTASK: {task}\nOUTPUT FORMAT: The first line of your response must be a comment with the full path of the file to be updated (e.g., # src/main.py). The rest of the response should be the complete content of the file.",
        }
        prompts.append(prompt)

    new_content = update_planning_md_with_prompts(content, prompts)
    output_file = args.output_file or args.planning_file
    write_file(output_file, new_content)
    logging.info(f"Generated {len(prompts)} prompts and updated {output_file}")
