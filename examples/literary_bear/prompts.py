from __future__ import annotations

from anchorcast.types import Brief, Character, Segment


def talking_head_prompt(
    character: Character,
    brief: Brief,
    previous: Segment | None = None,
) -> str:
    if previous is None:
        take = "Opening take. Begin speaking naturally, with no title card and no introduction of a show."
    else:
        ending = previous.brief.script()[-160:]
        take = (
            "Uninterrupted continuation of the same take. "
            "Do not greet, do not restart, do not recap, do not sign off, "
            "do not say the character's name. Same voice, same room, mouth already moving. "
            f"The previous line ended: \"{ending}\""
        )
    return (
        f"{character.visual_prompt} {take} "
        f"The same character as the first frame stays in place and speaks. "
        f"He says, in a {character.voice_prompt}: \"{brief.script()}\""
    )
