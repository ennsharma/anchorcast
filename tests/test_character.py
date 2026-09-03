from __future__ import annotations

from pathlib import Path

from anchorcast.types import Brief, Character


def test_character_prompt_includes_brief_script_and_voice() -> None:
    character = Character(
        name="Bear",
        image=Path("bear.png"),
        visual_prompt="Hand-drawn stuffed bear on cream paper.",
        voice_prompt="warm, unhurried cadence",
    )
    brief = Brief(
        id="1",
        topic="rain",
        talking_points=("It is raining in the wood.", "I shall think about honey."),
    )
    prompt = character.render_prompt(brief)
    assert "Hand-drawn stuffed bear" in prompt
    assert "warm, unhurried cadence" in prompt
    assert "It is raining in the wood." in prompt
