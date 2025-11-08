> [!WARNING]
> Repository Archived — This project explored autonomous batch processing with the Claude API for agentic development workflows. While the architecture and approach remain conceptually valid, the rapid evolution of AI tooling and API capabilities has rendered the implementation obsolete.
> 
> The codebase is preserved for historical reference and may inspire future iterations, but active development has ceased in favor of leveraging more current, native solutions in the AI orchestration space.


# Claude Code Automated

Claude Code Automated is a modular Python tool for automating batch
interactions with the Claude API, following best practices for agentic,
autonomous development. It is designed to streamline the process of planning,
executing, and applying code changes at scale.

## Features

- **Plan Generation**: Parses a `PLANNING.md` file to generate detailed,
  independent prompts for the Claude Batch API.
- **Batch Execution**: Submits the generated prompts to the Claude Batch API
  and monitors their progress asynchronously.
- **Result Processing**: Retrieves and saves results from the batch API,
  handling errors and edge cases robustly.
- **Automated Code Updates**: Applies the results from the batch API to the
  codebase, supporting safe, repeatable updates.
- **Comprehensive Unit Tests**: Includes a full test suite for all modules,
  ensuring reliability and maintainability.
- **Modular Architecture**: Separates CLI, command logic, API integration,
  and utilities for clarity and extensibility.

## Project Structure

- `src/main.py` — Main entry point for the CLI tool
- `src/cli.py` — Argument parser and CLI setup
- `src/commands/` — Modular command implementations (`plan.py`, `execute.py`, `update.py`)
- `src/claude_api.py` — Claude API integration (async, robust error handling)
- `src/file_utils.py` — File and markdown utilities
- `tests/` — Unit tests for all modules
- `PLANNING.md` — In-progress and future tasks
- `CHANGELOG.md` — Completed tasks and project history

## Usage

```bash
python src/main.py <command> [options]
```

### Commands

- `plan` — Generate prompts from `PLANNING.md`.
- `execute` — Execute prompts using the Claude Batch API.
- `update` — Apply results to the codebase.

## Best Practices

- Always keep `PLANNING.md` and `CHANGELOG.md` up to date.
- Write clear, independent tasks for batch processing.
- Review and test all code changes before merging.
- See `CLAUDE.md` for detailed workflow and documentation standards.

## License

This project is licensed under the MIT License.
