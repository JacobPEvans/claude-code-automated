import os

def read_file(filepath):
    """Reads a file and returns its content."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ""

def write_file(filepath, content):
    """Writes content to a file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def write_batch_results(results, output_dir):
    """Writes the results of a batch job to individual files."""
    succeeded_dir = os.path.join(output_dir, 'succeeded')
    failed_dir = os.path.join(output_dir, 'failed')
    os.makedirs(succeeded_dir, exist_ok=True)
    os.makedirs(failed_dir, exist_ok=True)

    for result in results.get('succeeded', []):
        custom_id = result.get('custom_id', 'unknown_id')
        filename = f"{custom_id}.txt"
        write_file(os.path.join(succeeded_dir, filename), result.get('content', ''))

    for result in results.get('failed', []):
        custom_id = result.get('custom_id', 'unknown_id')
        filename = f"{custom_id}.json"
        write_file(os.path.join(failed_dir, filename), str(result.get('error', '')))
