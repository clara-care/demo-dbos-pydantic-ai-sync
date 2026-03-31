# DBOS sync workflows and  Pydantic AI sync agent run

Demonstrates incompatibilities with the out-of-the-box DBOS and Pydantic AI sync APIs.

## Requirements

- [Python](https://www.python.org/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

## Usage

- `uv sync` - install the project dependencies
- `OPENAI_API_KEY=secret ANTHROPIC_API_KEY=secret uv run worker.py` - start the DBOS worker
- `uv run client.py [openai|anthropic|fallback] 10` - enqueue the DBOS work
