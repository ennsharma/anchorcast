from __future__ import annotations

from anchorcast.sources.feed import FeedSource
from anchorcast.types import Brief, Playhead

from examples.literary_bear.scripts import write_idle, write_script


class LiteraryNewsSource:
    def __init__(self, url: str, *, llm: bool = False) -> None:
        self.url = url
        self.llm = llm
        self._feed = FeedSource(url)
        self._index = 0
        self._last_script = ""

    def next_brief(self, playhead: Playhead | None = None) -> Brief | None:
        raw = self._feed.next_brief(playhead)
        if raw is None:
            self._feed = FeedSource(self.url)
            raw = self._feed.next_brief(playhead)
        if raw is None:
            script = write_idle(previous=self._last_script, index=self._index)
            brief = Brief(
                id=f"idle-{self._index}",
                topic="sitting still",
                talking_points=(script,),
            )
        else:
            script = write_script(
                headline=raw.topic,
                previous=self._last_script,
                index=self._index,
                llm=self.llm,
            )
            brief = Brief(
                id=raw.id,
                topic=raw.topic,
                talking_points=(script,),
                citations=raw.citations,
            )
        self._last_script = script
        self._index += 1
        return brief
