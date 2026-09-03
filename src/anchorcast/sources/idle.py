from __future__ import annotations

from anchorcast.types import Brief, Character, Playhead


class IdleSource:
    def __init__(self, character: Character) -> None:
        self.character = character

    def next_brief(self, playhead: Playhead | None = None) -> Brief | None:
        return Brief(
            id="idle",
            topic="sitting still",
            talking_points=(
                "I am only a bear of very little brain, sitting quite still "
                "and thinking of nothing in particular, which is a pleasant thing to do.",
            ),
        )
