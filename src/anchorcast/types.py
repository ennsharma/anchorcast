from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Protocol


@dataclass(frozen=True)
class Brief:
    id: str
    topic: str
    talking_points: tuple[str, ...]
    citations: tuple[str, ...] = ()
    duration_hint: int = 15
    priority: float = 0.0

    def script(self) -> str:
        return " ".join(point.strip() for point in self.talking_points if point.strip())


@dataclass(frozen=True)
class Character:
    name: str
    image: Path
    visual_prompt: str
    voice_prompt: str

    def render_prompt(self, brief: Brief) -> str:
        return (
            f"{self.visual_prompt} "
            f"The same character as the first frame stays in place and speaks. "
            f"He says, in a {self.voice_prompt}: \"{brief.script()}\""
        )


@dataclass(frozen=True)
class Playhead:
    index: int = 0


@dataclass(frozen=True)
class GenerateRequest:
    prompt: str
    image_path: Path
    output_path: Path
    brief: Brief
    duration: int


@dataclass(frozen=True)
class Segment:
    path: Path
    duration: float
    generated_in: float
    brief: Brief


@dataclass(frozen=True)
class StreamEvent:
    type: Literal["segment.ready"]
    segment: Segment
    index: int


class Model(Protocol):
    def generate(self, request: GenerateRequest) -> Segment: ...


class Source(Protocol):
    def next_brief(self, playhead: Playhead | None = None) -> Brief | None: ...


class Continuity(Protocol):
    def start_frame(self, previous: Segment | None, character: Character) -> Path: ...
