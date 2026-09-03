from __future__ import annotations

from anchorcast.continuity import IdentityContinuity, LastFrameContinuity
from anchorcast.session import Session
from anchorcast.sources import FeedSource, IdleSource, QueueSource
from anchorcast.types import Brief, Character, Playhead, Segment, StreamEvent

__version__ = "0.1.0"

__all__ = [
    "Brief",
    "Character",
    "FeedSource",
    "H3Max",
    "IdentityContinuity",
    "IdleSource",
    "LastFrameContinuity",
    "Playhead",
    "QueueSource",
    "Segment",
    "Session",
    "StreamEvent",
    "__version__",
]


def __getattr__(name: str) -> object:
    if name == "H3Max":
        from anchorcast.models.h3_max import H3Max

        return H3Max
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
