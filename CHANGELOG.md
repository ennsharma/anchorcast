# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] — 2026-09-03

### Changed

- `Character` is optional on `Session`. No still means `H3Max` uses text-to-video (`minimax/h3-max/text-to-video`).
- `Brief.prompt` is the generic slot text. Talking-head prompt assembly moved to `examples/literary_bear/prompts.py` (`render_prompt=`).
- `Continuity.start_frame` may return `None`.

## [0.1.0] — 2026-09-03

### Added

- `Session` with a generate-ahead buffer
- `Brief`, `Character`, `Segment`, and `StreamEvent` types
- `H3Max` model adapter (`minimax/h3-max/image-to-video`)
- `QueueSource`, `FeedSource`, and `IdleSource`
- `LastFrameContinuity` and `IdentityContinuity`
- MIT license
- GitHub Actions CI (pytest, ruff) and tag-triggered PyPI publish
- `Session.pump()` for live apps
- Follow-up clips prompt the model to continue the take
- `examples/literary_bear` continuous news stream with continuing spoken lines

`Brief` has no paid/unpaid taxonomy. Use `priority` to order the queue.
