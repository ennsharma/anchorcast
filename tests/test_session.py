from __future__ import annotations

from pathlib import Path

from anchorcast.continuity import IdentityContinuity
from anchorcast.models.base import GenerateRequest
from anchorcast.session import Session
from anchorcast.sources.queue import QueueSource
from anchorcast.types import Brief, Character, Segment


class FakeModel:
    def __init__(self) -> None:
        self.requests: list[GenerateRequest] = []

    def generate(self, request: GenerateRequest) -> Segment:
        self.requests.append(request)
        request.output_path.write_bytes(b"fake-video")
        return Segment(
            path=request.output_path,
            duration=15.0,
            generated_in=1.0,
            brief=request.brief,
        )


def _character(tmp_path: Path) -> Character:
    image = tmp_path / "bear.png"
    image.write_bytes(b"png")
    return Character(
        name="Bear",
        image=image,
        visual_prompt="a stuffed bear",
        voice_prompt="soft",
    )


def test_session_fills_buffer_from_queue(tmp_path: Path) -> None:
    source = QueueSource()
    source.submit(Brief(id="one", topic="one", talking_points=("First story.",)))
    source.submit(Brief(id="two", topic="two", talking_points=("Second story.",)))
    model = FakeModel()
    session = Session(
        model=model,
        character=_character(tmp_path),
        source=source,
        workdir=tmp_path / "work",
        continuity=IdentityContinuity(),
        buffer_clips=2,
    )

    events = list(session.run(max_segments=2))

    assert [event.segment.brief.id for event in events] == ["one", "two"]
    assert len(model.requests) == 2
    assert model.requests[0].image_path == session.character.image


def test_session_does_not_run_ahead_of_buffer_without_playhead(tmp_path: Path) -> None:
    source = QueueSource()
    for index in range(5):
        source.submit(Brief(id=str(index), topic=str(index), talking_points=(f"Story {index}.",)))
    session = Session(
        model=FakeModel(),
        character=_character(tmp_path),
        source=source,
        workdir=tmp_path / "work",
        continuity=IdentityContinuity(),
        buffer_clips=2,
    )

    events = list(session.run(max_segments=8))
    assert len(events) == 2
