import json
import re

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
        task_pattern = re.compile(r"^\s*(?:-|\*|\+)\s+(?:\*\*.*\*\*\s*-\s*)?(.*)", re.MULTILINE)

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
