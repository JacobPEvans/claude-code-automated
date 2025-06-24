import os
import logging
from src.file_utils import read_file, write_file

def update_command(args):
    """
    Applies the code changes from the results directory to the project.
    """
    logging.info(f"Updating project in: {args.project_dir}")
    results_dir = args.results_dir

    if not os.path.isdir(results_dir):
        logging.error(f"Results directory not found: {results_dir}")
        return

    for filename in os.listdir(results_dir):
        if filename.endswith(".txt"):
            result_filepath = os.path.join(results_dir, filename)
            content = read_file(result_filepath)

            if not content:
                logging.warning(f"Result file is empty: {filename}")
                continue

            lines = content.split('\n')
            first_line = lines[0].strip()

            if first_line.startswith("#"):
                target_file_path = first_line[1:].strip()
                if os.path.isabs(target_file_path):
                    logging.warning(f"Skipping absolute path found in {filename}: {target_file_path}")
                    continue

                full_path = os.path.join(args.project_dir, target_file_path)
                code_content = '\n'.join(lines[1:])

                logging.info(f"Applying changes to: {full_path}")
                write_file(full_path, code_content)
            else:
                logging.warning(f"Could not find target file path in {filename}")
