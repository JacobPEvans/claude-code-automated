# Claude Code Automated

This project provides a command-line tool to automate interactions with the Claude API, specifically for batch processing of tasks defined in a `PLANNING.md` file.

## Features

- **Plan Generation**: Parses a `PLANNING.md` file to generate detailed, independent prompts for the Claude Batch API.
- **Batch Execution**: Submits the generated prompts to the Claude Batch API and monitors their progress.
- **Result Processing**: Retrieves the results from the batch API and saves them to files.
- **Code Updates**: Applies the changes from the batch API results to the local codebase.

## Usage

```bash
python src/main.py <command> [options]
```

### Commands

- `plan`: Generate detailed prompts from `PLANNING.md`.
- `execute`: Execute the prompts using the Claude Batch API.
- `update`: Apply the results to the codebase.
