from __future__ import annotations

from anchorcast.sources.queue import QueueSource
from anchorcast.types import Brief


def test_queue_returns_highest_priority_first() -> None:
    source = QueueSource()
    source.submit(Brief(id="a", topic="eggs", talking_points=("Why eggs?",), priority=1.0))
    source.submit(Brief(id="b", topic="rates", talking_points=("Mortgage rates.",), priority=10.0))

    first = source.next_brief()
    second = source.next_brief()
    assert first is not None
    assert second is not None
    assert first.id == "b"
    assert second.id == "a"
    assert source.next_brief() is None
