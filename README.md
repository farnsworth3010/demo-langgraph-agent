## demo-langgraph-agent

Lightweight demo showing how to use LangChain agents with a simple ticketing tools (SQLite + Pydantic models) and run them against a local LLM that exposes an OpenAI-compatible HTTP API (for example LM Studio / local Qwen).

## Key technologies

- uv package manager
- Python 3.13+
- LangChain (agents)
- Pydantic (data validation for tickets)
- SQLite (file DB under `data/tickets.db`)
- Local LLM with an OpenAI-compatible endpoint (example: LM Studio running a Qwen model)
- Dev utilities: langgraph-cli (dev dependency listed in pyproject)

## Project layout

- `src/db.py` — small SQLite helpers and initialization
- `src/models/ticket.py` — `pydantic` Ticket model
- `src/repository/ticket_repository.py` — SQL CRUD operations for tickets
- `src/service/ticket_service.py` — business-logic layer validating payloads
- `src/tools.py` — LangChain `@tool` wrappers for creating/listing/reading/deleting tickets
- `src/graph.py` — creates two agents (`support` and `admin`) and initializes the chat model
- `data/tickets.db` — default sqlite database (created automatically if missing)
- `pyproject.toml` — dependencies

## Quick contract

- Inputs: user messages to agents (support/admin) routed through LangChain
- Outputs: agent responses and, when applicable, DB side-effects (new ticket id, deleted id)

## Setup (macOS / zsh)

1. Install requirements with uv:

```bash
uv sync
```

Note: `pyproject.toml` lists the core runtime dependencies (langchain and a few provider packages). If you use other model providers you may need to install their SDKs as well.

## Local LLM (LM Studio / Qwen) guidance

This project expects a chat model available via an OpenAI-compatible HTTP API at `http://localhost:1234/v1` and the model name `qwen/qwen3-4b` (see `src/graph.py`). 

- Run LM Studio (or similar) and enable its OpenAI-compatible REST API. Configure it to host the Qwen model you need and listen on port 1234.

If you use a different base URL or model name, edit `src/graph.py` and change the call to `init_chat_model(...)` accordingly.

The sample code uses `api_key="not_needed"` because the local server in this example doesn't require an api key.

## Run (interactive / local)

Use the LangGraph dev UI (recommended for exploring agents and tools).

### LangGraph dev UI (via `uv` + `langgraph-cli`)

```bash
uv run langgraph dev --no-browser
```

When the command starts it prints a local URL. Copy that URL and open it in your browser — this is the LangGraph / LangSmith Studio UI where you can inspect agents, edit prompts, and run conversations using the `support` and `admin` agents defined in `src/graph.py`.

Tip: the `--no-browser` flag prevents an automatic browser launch; remove it if you want the CLI to open your browser.
It is disabled, because Safari (if set as a default browser) is not connecting to the agent and a special flag is required.

## Configuration and customization

- To change the model or the model server URL edit `src/graph.py` and update `init_chat_model(...)`.
- To persist the DB elsewhere, call `init_db(path)` with an explicit path or override the path returned by `_get_default_db_path()` in `src/db.py`.

## Troubleshooting

- If the agents hang or you get network errors, verify the model server is running and reachable at `http://localhost:1234/v1`.
- If you get missing-package errors, double-check the virtualenv is activated and `uv sync` completed successfully.

## Next steps / improvements

- Add tests for the service and repository layers (happy path + DB empty case).
- Add structured logging for admin destructive operations (delete) and persist reasons for audit.