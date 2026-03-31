# DBOS sync workflows and  Pydantic AI sync agent run

Demonstrates incompatibilities with the out-of-the-box DBOS and Pydantic AI sync APIs.

## Requirements

- [Python](https://www.python.org/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

## Usage

- `uv sync` - install the project dependencies
- `ANTHROPIC_API_KEY=secret uv run worker.py` - start the DBOS worker
