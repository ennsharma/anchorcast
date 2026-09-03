from __future__ import annotations

from pathlib import Path

from anchorcast.sources.idle import IdleSource
from anchorcast.types import Character


def test_idle_brief_makes_no_news_claim() -> None:
    character = Character(
        name="Bear",
        image=Path("missing.png"),
        visual_prompt="a stuffed bear",
        voice_prompt="soft and unhurried",
    )
    brief = IdleSource(character).next_brief()
    assert brief is not None
    assert brief.kind == "idle"
    assert brief.citations == ()
    assert "arrest" not in brief.script().lower()
