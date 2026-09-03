from __future__ import annotations

from pathlib import Path

from examples.literary_bear.prompts import talking_head_prompt
from anchorcast.types import Brief, Character, Segment


def _character() -> Character:
    return Character(
        name="Bear",
        image=Path("bear.png"),
        visual_prompt="Hand-drawn stuffed bear on cream paper.",
        voice_prompt="warm, unhurried cadence",
    )


def test_talking_head_prompt_includes_brief_script_and_voice() -> None:
    brief = Brief(
        id="1",
        topic="rain",
        talking_points=("It is raining in the wood.", "I shall think about honey."),
    )
    prompt = talking_head_prompt(_character(), brief)
    assert "Hand-drawn stuffed bear" in prompt
    assert "warm, unhurried cadence" in prompt
    assert "It is raining in the wood." in prompt
    assert "continuation" not in prompt.lower()


def test_talking_head_followup_asks_for_an_uninterrupted_take() -> None:
    previous = Segment(
        path=Path("0000.mp4"),
        duration=15.0,
        generated_in=1.0,
        brief=Brief(id="1", topic="rain", talking_points=("It is raining in the wood.",)),
    )
    prompt = talking_head_prompt(
        _character(),
        Brief(id="2", topic="honey", talking_points=("And honey is a different matter entirely.",)),
        previous=previous,
    )
    assert "uninterrupted" in prompt.lower() or "continuation" in prompt.lower()
    assert "do not greet" in prompt.lower()
    assert "And honey is a different matter entirely." in prompt
    assert "It is raining in the wood." in prompt
