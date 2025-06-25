# Testing Guidelines

This document provides instructions for running the unit tests for the
`claude-code-automated` project.

## 1. Install Python (if not already installed)

- On Windows, use [Chocolatey](https://chocolatey.org/):

```bash
choco install python --pre
```

- On Linux/macOS, use your package manager or download from
  [python.org](https://www.python.org/downloads/).

## 2. Create and Activate a Virtual Environment

```bash
python3 -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate
```

## 3. Upgrade pip and Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Install Test Tools

```bash
pip install pytest pytest-cov
```

## 5. Running Tests

- To run all tests:

```bash
pytest
```

- To run with coverage:

```bash
pytest --cov=src
```

## 6. Environment Variables

- Use a `.env` file for sensitive or environment-specific variables. Install `python-dotenv` if needed:

```bash
pip install python-dotenv
```

- Example `.env`:

```env
ANTHROPIC_API_KEY=your-key-here
```

## 7. Best Practices

- Always activate your virtual environment before development or testing.
- Keep dependencies in `requirements.txt` up to date.
- Use `pytest` for all new tests.
- Never commit secrets or credentials.
- Use `.gitignore` to exclude `.env`, `.venv/`, and other local files.
