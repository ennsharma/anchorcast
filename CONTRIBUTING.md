# Contributing

Thanks for looking at Anchorcast. The useful work is the `Session` / `Model` / `Source` / `Brief` interface. Keep that small.

## Setup

```bash
python3.11 -m pip install -e ".[dev]"
python3.11 -m pytest
python3.11 -m ruff check src tests
```

Python 3.11+ and ffmpeg on `PATH`. Unit tests must not call fal.

## Pull requests

- One idea per PR
- Tests for behavior changes
- Do not land YouTube / Twitch / TikTok / payments in this repo
- Match existing style: double quotes, type hints

Coding agents should read [AGENTS.md](AGENTS.md).

## License

Contributions are MIT, same as the rest of the project.
