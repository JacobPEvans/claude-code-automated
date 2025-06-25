import os
import json
import re

def read_file(filepath):
    """Reads a file and returns its content."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ""

def write_file(filepath, content):
    """Writes content to a file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def parse_tasks_from_planning_md(content):
    """Parses tasks from the PLANNING.md content."""
    try:
        # Look for the "Remaining Tasks" section
        tasks_section_match = re.search(r"### 📋 Remaining Tasks\n(.*?)(?=\n##|\Z)", content, re.DOTALL)
        if not tasks_section_match:
            return []

        tasks_section = tasks_section_match.group(1)
        tasks = []

        # Regex to capture task descriptions from markdown lists
        task_pattern = re.compile(r"^\s*(?:-|\d+\.)\s+(?:\*\*.*?\*\*\s*-\s*)?(.*)", re.MULTILINE)

        for match in task_pattern.finditer(tasks_section):
            task_text = match.group(1).strip()
            if task_text and '[x]' not in match.group(0): # Ignore completed tasks
                tasks.append(task_text)
        return tasks
    except Exception:
        return []

def update_planning_md_with_prompts(content, prompts):
    """Updates the PLANNING.md content with generated prompts."""
    prompts_json = json.dumps(prompts, indent=2)
    new_prompts_section = f"## Generated Prompts\n\n```json\n{prompts_json}\n```"
    # Remove any existing Generated Prompts section and everything after it
    content_without_prompts = re.sub(r"## Generated Prompts[\s\S]*", "", content, flags=re.DOTALL).strip()
    return f"{content_without_prompts}\n\n{new_prompts_section}"

def parse_prompts_from_planning_md(content):
    """Parses the generated prompts from the PLANNING.md content."""
    try:
        json_block_match = re.search(r"## Generated Prompts\n\n```json\n(.*?)\n```", content, re.DOTALL)
        if json_block_match:
            prompts_json = json_block_match.group(1)
            return json.loads(prompts_json)
        return []
    except (json.JSONDecodeError):
        return []

def write_batch_results(results, output_dir="results"):
    """Saves successful batch results to files."""
    os.makedirs(output_dir, exist_ok=True)
    for i, result in enumerate(results.get('succeeded', [])):
        content = result.get('content', '')
        custom_id = result.get('custom_id', f'task_{i}')
        # Create a filename from the custom_id
        safe_filename = re.sub(r'[^a-zA-Z0-9_-]', '_', custom_id)
        output_filename = f"{safe_filename}.txt"
        write_file(os.path.join(output_dir, output_filename), content)
