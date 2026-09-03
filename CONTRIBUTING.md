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

## Releasing

CI runs pytest and ruff on every push and pull request.

PyPI publishes from a version tag via [trusted publishing](https://docs.pypi.org/trusted-publishers/). No API token in GitHub secrets.

1. Bump `version` in `pyproject.toml` and `src/anchorcast/__init__.py`, and add a `CHANGELOG.md` entry.
2. On PyPI: Publishing → add a trusted publisher (`scrollmark/anchorcast`, workflow `publish.yml`, environment `pypi`). Needed once, before the first release.
3. Tag and push:

```bash
git tag v0.1.0
git push origin v0.1.0
```

The tag must match the package version (`v0.1.0` for `0.1.0`). The `pypi` GitHub Environment must exist on the repo.

## License

Contributions are MIT, same as the rest of the project.
