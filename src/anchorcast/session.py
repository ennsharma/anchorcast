from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

from anchorcast.continuity import IdentityContinuity
from anchorcast.types import (
    Brief,
    Character,
    Continuity,
    GenerateRequest,
    Model,
    Playhead,
    Segment,
    Source,
    StreamEvent,
)


class Session:
    def __init__(
        self,
        *,
        model: Model,
        character: Character,
        source: Source,
        workdir: Path,
        continuity: Continuity | None = None,
        buffer_clips: int = 2,
        idle: Source | None = None,
    ) -> None:
        self.model = model
        self.character = character
        self.source = source
        self.workdir = workdir
        self.continuity = continuity or IdentityContinuity()
        self.buffer_clips = buffer_clips
        self.idle = idle
        self.segments: list[Segment] = []
        self.playing_index = -1
        self.workdir.mkdir(parents=True, exist_ok=True)

    def advance(self, index: int) -> None:
        self.playing_index = max(self.playing_index, index)

    def pump(self) -> StreamEvent | None:
        if not self._should_generate():
            return None
        return self._generate_one()

    def run(self, max_segments: int | None = None) -> Iterator[StreamEvent]:
        while True:
            if max_segments is not None and len(self.segments) >= max_segments:
                return
            if not self._should_generate():
                if max_segments is not None:
                    return
                return
            event = self._generate_one()
            if event is None:
                if max_segments is not None:
                    return
                return
            yield event

    def _should_generate(self) -> bool:
        if self.playing_index < 0:
            return len(self.segments) < self.buffer_clips
        ahead = len(self.segments) - self.playing_index
        return ahead < self.buffer_clips + 1

    def _next_brief(self) -> Brief | None:
        playhead = Playhead(index=max(self.playing_index, 0))
        brief = self.source.next_brief(playhead)
        if brief is not None:
            return brief
        if self.idle is not None:
            return self.idle.next_brief(playhead)
        return None

    def _generate_one(self) -> StreamEvent | None:
        brief = self._next_brief()
        if brief is None:
            return None
        previous = self.segments[-1] if self.segments else None
        image_path = self.continuity.start_frame(previous, self.character)
        index = len(self.segments)
        output_path = self.workdir / f"{index:04d}.mp4"
        request = GenerateRequest(
            prompt=self.character.render_prompt(brief, previous=previous),
            image_path=image_path,
            output_path=output_path,
            brief=brief,
            duration=brief.duration_hint,
        )
        segment = self.model.generate(request)
        self.segments.append(segment)
        return StreamEvent(type="segment.ready", segment=segment, index=index)
