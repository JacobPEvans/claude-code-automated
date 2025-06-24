import argparse
import asyncio
import json
import os
from src.claude_api import client, create_batch_requests, poll_batch_completion, process_batch_results
from src.file_utils import read_planning_md, write_planning_md, write_batch_results

def plan(args):
    print(f"Planning using file: {args.planning_file}")
    content = read_planning_md(args.planning_file)

    try:
        start_index = content.index("### 📋 Remaining Tasks")
        end_index = content.index("## Task Decomposition (DECOMP Method)")
        tasks_section = content[start_index:end_index]

        tasks = []
        for line in tasks_section.split('\n'):
            line = line.strip()
            if (line.startswith('- ') or '. ' in line) and '[x]' not in line:
                parts = line.split('-', 2)
                if len(parts) > 1:
                    task_text = parts[-1].strip()
                    if task_text and not task_text.startswith('Path to the') and not task_text.startswith('Directory to save') and not task_text.startswith('The root directory'):
                        tasks.append(task_text)

        prompts = []
        for i, task in enumerate(tasks):
            prompt = {
              "custom_id": f"task_{i}",
              "params": {
                "model": "claude-3-opus-20240229",
                "max_tokens": 4096,
                "system": "You are an expert Python developer. Implement complete, production-ready code with error handling, documentation, and tests.",
                "messages": [{
                  "role": "user",
                  "content": f"CONTEXT: Complete the following task for the `claude-code-automated` project.\nTASK: {task}\nOUTPUT FORMAT: The first line of your response must be a comment with the full path of the file to be updated (e.g., # src/main.py). The rest of the response should be the complete content of the file."
                }]
              }
            }
            prompts.append(prompt)

        prompts_json = json.dumps(prompts, indent=2)

        new_content = content.replace("## Generated Prompts\n\n_This section will be populated by the `plan` command._", f"## Generated Prompts\n\n```json\n{prompts_json}\n```")
        write_planning_md(new_content, args.output_file)
        print(f"Generated {len(prompts)} prompts and updated {args.output_file}")

    except ValueError:
        print("Could not find '### 📋 Remaining Tasks' section in the planning file.")


async def execute(args):
    print(f"Executing prompts from: {args.planning_file}")
    content = read_planning_md(args.planning_file)

    try:
        start_index = content.index("## Generated Prompts")
        json_block = content[start_index:]
        json_start = json_block.index("```json") + len("```json\n")
        json_end = json_block.index("```", json_start)
        prompts_json = json_block[json_start:json_end]

        requests = json.loads(prompts_json)

        print(f"Found {len(requests)} prompts to execute.")

        print("Submitting batch request to Claude API...")
        batch = client.messages.batches.create(requests=requests)
        print(f"Batch request submitted. Batch ID: {batch.id}")

        print("Waiting for batch to complete...")
        completed_batch = await poll_batch_completion(client, batch.id)

        if completed_batch:
            print("Batch completed. Processing results...")
            results = process_batch_results(client, completed_batch.id)
            write_batch_results(results, args.output_dir)
            print(f"Results saved to {args.output_dir}")
        else:
            print("Batch processing failed.")

    except (ValueError, json.JSONDecodeError) as e:
        print(f"Error processing planning file: {e}")
        print("Could not find or parse the 'Generated Prompts' JSON block in the planning file. Please run the 'plan' command first.")


def update(args):
    print(f"Updating project in: {args.project_dir}")
    results_dir = args.results_dir

    if not os.path.exists(results_dir):
        print(f"Results directory not found: {results_dir}")
        return

    for filename in os.listdir(results_dir):
        if filename.endswith(".txt"):
            filepath = os.path.join(results_dir, filename)
            with open(filepath, 'r') as f:
                content = f.read()

            first_line = content.split('\n', 1)[0]
            if first_line.startswith('#'):
                target_file = first_line[1:].strip()
                target_filepath = os.path.join(args.project_dir, target_file)

                print(f"Updating file: {target_filepath}")

                code_content = content.split('\n', 1)[1]

                os.makedirs(os.path.dirname(target_filepath), exist_ok=True)
                with open(target_filepath, 'w') as f:
                    f.write(code_content)
            else:
                print(f"Could not determine target file for {filename}")


def main():
    parser = argparse.ArgumentParser(description='A tool to automate Claude API batch calls.')
    subparsers = parser.add_subparsers(dest='command')

    # Plan command
    plan_parser = subparsers.add_parser('plan', help='Generate detailed prompts from PLANNING.md')
    plan_parser.add_argument('--planning-file', default='PLANNING.md', help='Path to the PLANNING.md file')
    plan_parser.add_argument('--output-file', default='PLANNING.md', help='Path to write the generated prompts')

    # Execute command
    execute_parser = subparsers.add_parser('execute', help='Execute the prompts using the Claude Batch API')
    execute_parser.add_argument('--planning-file', default='PLANNING.md', help='Path to the PLANNING.md file with generated prompts')
    execute_parser.add_argument('--output-dir', default='results', help='Directory to save the batch results')

    # Update command
    update_parser = subparsers.add_parser('update', help='Apply the results to the codebase')
    update_parser.add_argument('--results-dir', default='results', help='Directory with the batch results')
    update_parser.add_argument('--project-dir', default='.', help='The root directory of the project to apply changes to')


    args = parser.parse_args()

    if args.command == 'plan':
        plan(args)
    elif args.command == 'execute':
        asyncio.run(execute(args))
    elif args.command == 'update':
        update(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
