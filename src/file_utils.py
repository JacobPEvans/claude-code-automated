import os

def read_planning_md(filepath="PLANNING.md"):
    with open(filepath, 'r') as f:
        return f.read()

def write_planning_md(content, filepath="PLANNING.md"):
    with open(filepath, 'w') as f:
        f.write(content)

def write_batch_results(results, output_dir="results"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i, result in enumerate(results['succeeded']):
        with open(os.path.join(output_dir, f"result_{i}.txt"), 'w') as f:
            f.write(result['content'])
