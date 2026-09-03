# Agent notes

This repository is a **Python client** for generative livestreams. It is not a YouTube app, not a character, and not a news show.

## Layout

- `src/anchorcast/` — library
- `tests/` — pytest, no fal network calls
- `examples/` — apps that consume the library, including a literary-bear news stream

## Architecture

Keep these boundaries:

| Layer | Owns |
| --- | --- |
| `Brief` | What to say next (topic, talking points, citations) |
| `Model` | `generate(request) -> Segment` |
| `Source` | `next_brief(playhead) -> Brief \| None` |
| `Continuity` | Which still starts the next clip |
| `Session` | Generate-ahead buffer and events |

Do **not** add YouTube, Twitch, TikTok, Stripe, or Super Chat integrations here. Those belong in a later backend that maps platform events into `Brief`s on a `QueueSource`.

Do **not** let `IdleSource` (or any default source) invent news claims. Idle is character bits only.

## Python

- 3.11+
- Double quotes
- Type annotations on public functions and dataclasses
- `gpt-5.6-luna` for OpenAI calls in examples (cheap GPT-5.6 tier)

## Checks

```bash
python3.11 -m pip install -e ".[dev]"
python3.11 -m pytest
python3.11 -m ruff check src tests
```

New behavior needs a failing test first unless it is config, examples, or generated files.

The H3 Max adapter hits fal. Do not call it from unit tests. Use a fake `Model`.
