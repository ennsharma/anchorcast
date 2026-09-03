from __future__ import annotations

from pathlib import Path

from anchorcast import Character, FeedSource, IdleSource, Session
from anchorcast.continuity import LastFrameContinuity
from anchorcast.models import H3Max

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    character = Character(
        name="Bear",
        image=ROOT / "examples" / "characters" / "literary-bear" / "pooh-1926.png",
        visual_prompt=(
            "Hand-drawn 1926 book illustration of a stuffed bear of very little brain. "
            "Pencil and light watercolor on cream paper. No clothing."
        ),
        voice_prompt="warm, soft, slightly posh, unhurried stuffed-bear cadence",
    )
    source = FeedSource("https://feeds.bbci.co.uk/news/world/rss.xml")
    session = Session(
        model=H3Max(),
        character=character,
        source=source,
        idle=IdleSource(character),
        workdir=ROOT / ".anchorcast",
        continuity=LastFrameContinuity(),
        buffer_clips=2,
    )
    for event in session.run(max_segments=2):
        clip = event.segment
        print(f"{event.index:02d}  {clip.duration:.1f}s in {clip.generated_in:.1f}s  {clip.brief.topic}")


if __name__ == "__main__":
    main()
