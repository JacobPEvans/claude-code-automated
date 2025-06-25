import argparse
import asyncio

def create_parser():
    """Creates and configures the argument parser for the application."""
    parser = argparse.ArgumentParser(description="Claude Code Automated Development Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Plan command
    plan_parser = subparsers.add_parser("plan", help="Generate prompts from PLANNING.md")
    plan_parser.add_argument("--planning-file", default="PLANNING.md", help="Path to the planning file.")
    plan_parser.add_argument(
        "--output-file", help="Path to save the updated planning file (defaults to overwriting the input file)."
    )

    # Execute command
    exec_parser = subparsers.add_parser("execute", help="Execute prompts using the Claude Batch API")
    exec_parser.add_argument("--planning-file", default="PLANNING.md", help="Path to the planning file with prompts.")
    exec_parser.add_argument("--output-dir", default="results", help="Directory to save batch results.")

    # Update command
    update_parser = subparsers.add_parser("update", help="Apply code changes from results")
    update_parser.add_argument("--project-dir", default=".", help="The root directory of the project to update.")
    update_parser.add_argument("--results-dir", default="results", help="Directory where results are stored.")

    return parser
