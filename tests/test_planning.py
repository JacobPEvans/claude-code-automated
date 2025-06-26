import pytest
from src.planning import (
    parse_tasks_from_planning_md,
    update_planning_md_with_prompts,
    parse_prompts_from_planning_md,
)

def test_parse_tasks_from_planning_md():
    content = """### 📋 Remaining Tasks

- Task 1
- Task 2

## Next Section"""
    tasks = parse_tasks_from_planning_md(content)
    assert tasks == ["Task 1", "Task 2"]

def test_update_planning_md_with_prompts():
    content = "## Generated Prompts\n\nold prompts"
    prompts = [{"id": 1}]
    new_content = update_planning_md_with_prompts(content, prompts)
    assert '"id": 1' in new_content
    assert "old prompts" not in new_content

def test_parse_prompts_from_planning_md():
    content = '''## Generated Prompts

```json
[{"id": 1}]
```'''
    prompts = parse_prompts_from_planning_md(content)
    assert prompts == [{"id": 1}]
