# LLM Chess

A terminal application where a human supervises a chess match between two independent agents. `python-chess` is the sole authority for board state, legal moves, turn order, and outcomes; agents can only propose moves.

## Features

- ASCII board and UCI move history after every approved move
- `C` to approve, `R` to reject, and `S` to stop
- Legal-move validation and technical forfeits after repeated invalid responses
- Standard game-ending outcome detection through `python-chess`
- Deterministic offline fake agents
- Separate, read-only Codex threads for White and Black

## Requirements and installation

- Python 3.12 or newer
- [`uv`](https://docs.astral.sh/uv/)
- Codex CLI for the Codex provider

```bash
uv sync
```

## Run

Offline mode requires no account or network access:

```bash
uv run chess-dev --provider fake --seed 42
```

For Codex, authenticate using the supported runtime and then start a match:

```bash
codex login
uv run chess-dev --provider codex
```

The application keeps the SDK client alive for the match and creates isolated White and Black threads using a read-only sandbox. It does not require an OpenAI Platform or OpenRouter API key and never reads or copies `~/.codex/auth.json`.

## CLI arguments

```text
--provider {fake,codex}   Agent provider (default: fake)
--white-model MODEL      White model; omit for the Codex configured default
--black-model MODEL      Black model; omit for the Codex configured default
--seed INTEGER           Fake-provider seed (default: 0)
--max-retries INTEGER    Invalid responses before forfeit (default: 3)
```

## Tests

Tests are offline and never invoke Codex or another external API:

```bash
uv run pytest
```

## Known limitations

- Moves and history are displayed in UCI notation rather than SAN.
- A Codex match requires a working local Codex installation and completed `codex login`.
- The fake provider plays legal moves but has no chess strategy.
- OpenRouter support is not currently required or included. The provider protocol allows it to be added later without changing the domain or controller.
