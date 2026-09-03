from __future__ import annotations

import feedparser

from anchorcast.types import Brief, Playhead


class FeedSource:
    def __init__(self, url: str, *, limit: int = 30) -> None:
        self.url = url
        self.limit = limit
        self._unused: list[Brief] = []
        self._loaded = False

    def next_brief(self, playhead: Playhead | None = None) -> Brief | None:
        if not self._loaded:
            self._unused = self._load()
            self._loaded = True
        if not self._unused:
            return None
        return self._unused.pop(0)

    def _load(self) -> list[Brief]:
        parsed = feedparser.parse(self.url)
        briefs: list[Brief] = []
        for entry in parsed.entries[: self.limit]:
            title = str(getattr(entry, "title", "")).strip()
            if not title:
                continue
            link = str(getattr(entry, "link", "")).strip()
            briefs.append(
                Brief(
                    id=link or title,
                    topic=title,
                    talking_points=(f"I have just heard that {title.rstrip('.')}.",),
                    citations=(link,) if link else (),
                )
            )
        return briefs
