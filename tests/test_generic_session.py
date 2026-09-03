from __future__ import annotations

from pathlib import Path

from anchorcast.models.base import GenerateRequest
from anchorcast.session import Session
from anchorcast.sources.queue import QueueSource
from anchorcast.types import Brief, Segment


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


def test_session_generates_from_brief_prompt_without_character(tmp_path: Path) -> None:
    source = QueueSource()
    source.submit(
        Brief(
            id="kitten",
            topic="garden",
            prompt="A white kitten chases a butterfly across a sunlit garden.",
        )
    )
    model = FakeModel()
    session = Session(
        model=model,
        source=source,
        workdir=tmp_path / "work",
        buffer_clips=1,
    )
    events = list(session.run(max_segments=1))
    assert events[0].segment.brief.id == "kitten"
    assert model.requests[0].prompt == "A white kitten chases a butterfly across a sunlit garden."
    assert model.requests[0].image_path is None
