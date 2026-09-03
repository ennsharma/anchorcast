from __future__ import annotations

from pathlib import Path

from anchorcast.media import extract_last_frame
from anchorcast.types import Character, Segment


class IdentityContinuity:
    def start_frame(self, previous: Segment | None, character: Character | None) -> Path | None:
        if character is None:
            return None
        return character.image


class LastFrameContinuity:
    def start_frame(self, previous: Segment | None, character: Character | None) -> Path | None:
        if previous is not None:
            frame_path = previous.path.with_name(f"{previous.path.stem}-last.png")
            return extract_last_frame(previous.path, frame_path)
        if character is None:
            return None
        return character.image
