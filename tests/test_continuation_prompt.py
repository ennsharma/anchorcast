from __future__ import annotations

from pathlib import Path

from anchorcast.types import Brief, Character, Segment


def _character() -> Character:
    return Character(
        name="Bear",
        image=Path("bear.png"),
        visual_prompt="Hand-drawn stuffed bear on cream paper.",
        voice_prompt="warm, unhurried cadence",
    )


def test_opening_prompt_does_not_tell_the_model_to_continue() -> None:
    prompt = _character().render_prompt(
        Brief(id="1", topic="rain", talking_points=("It is raining in the wood.",))
    )
    assert "It is raining in the wood." in prompt
    assert "continuation" not in prompt.lower()


def test_followup_prompt_asks_for_an_uninterrupted_take() -> None:
    previous = Segment(
        path=Path("0000.mp4"),
        duration=15.0,
        generated_in=1.0,
        brief=Brief(id="1", topic="rain", talking_points=("It is raining in the wood.",)),
    )
    prompt = _character().render_prompt(
        Brief(id="2", topic="honey", talking_points=("And honey is a different matter entirely.",)),
        previous=previous,
    )
    assert "uninterrupted" in prompt.lower() or "continuation" in prompt.lower()
    assert "do not greet" in prompt.lower()
    assert "And honey is a different matter entirely." in prompt
    assert "It is raining in the wood." in prompt
