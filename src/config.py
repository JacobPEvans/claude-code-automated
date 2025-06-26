
# Configuration for the Claude Code Automated Development Tool

# API Configuration
ANTHROPIC_API_KEY = None  # Set via environment variable
MODEL_NAME = "claude-3-opus-20240229"
MAX_TOKENS = 4096

# Polling Configuration
POLL_INITIAL_DELAY = 10
POLL_MAX_DELAY = 120
POLL_FACTOR = 1.5

# File Paths
PLANNING_FILE = "PLANNING.md"
RESULTS_DIR = "results"
