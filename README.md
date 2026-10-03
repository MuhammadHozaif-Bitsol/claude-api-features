# Claude API Features

Small Python scripts that each demonstrate one feature of the [Claude API](https://platform.claude.com/docs) using the official `anthropic` SDK and `claude-sonnet-5-5`.

| Script | Feature | What it does |
|---|---|---|
| `scripts/thinking.py` | Extended thinking | Sends a prompt with adaptive thinking enabled and prints the response, including thinking blocks (the default prompt triggers a `redacted_thinking` block). |
| `scripts/images.py` | Vision | Sends a satellite image from `images/` with a structured prompt and prints a wildfire risk assessment for the property. |
| `scripts/citations.py` | Citations | Sends `documents/earth.pdf` with citations enabled and prints each cited passage with its page number. |
| `scripts/caching.py` | Prompt caching | Sends a ~8.4k-token system prompt from `prompts/code_prompt.md` with `cache_control`, so repeat requests read it from the cache. |

## Setup

Requires [uv](https://docs.astral.sh/uv/) and Python 3.12+.

1. Install dependencies:

   ```bash
   uv sync
   ```

2. Create a `.env` file in the project root with your API key:

   ```
   ANTHROPIC_API_KEY=your-key-here
   ```

## Usage

Run any script from the project root:

```bash
uv run scripts/thinking.py
uv run scripts/images.py
uv run scripts/citations.py
uv run scripts/caching.py
```

To see caching work, run `caching.py` twice within five minutes. The first run writes the system prompt to the cache (`cache_creation_input_tokens`); the second reads it back (`cache_read_input_tokens`) at a fraction of the cost.

## Project layout

```
scripts/     one script per feature
images/      sample satellite images for images.py
documents/   PDF used by citations.py
prompts/     long system prompt used by caching.py
```

## Development

Code is linted and formatted with [ruff](https://docs.astral.sh/ruff/):

```bash
uvx ruff check scripts/
uvx ruff format scripts/
```
