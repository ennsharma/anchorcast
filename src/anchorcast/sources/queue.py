from __future__ import annotations

import heapq

from anchorcast.types import Brief, Playhead


class QueueSource:
    def __init__(self) -> None:
        self._heap: list[tuple[float, int, Brief]] = []
        self._seq = 0

    def submit(self, brief: Brief) -> None:
        heapq.heappush(self._heap, (-brief.priority, self._seq, brief))
        self._seq += 1

    def next_brief(self, playhead: Playhead | None = None) -> Brief | None:
        if not self._heap:
            return None
        _, _, brief = heapq.heappop(self._heap)
        return brief
