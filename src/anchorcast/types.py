from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Protocol


@dataclass(frozen=True)
class Brief:
    id: str
    topic: str = ""
    talking_points: tuple[str, ...] = ()
    citations: tuple[str, ...] = ()
    duration_hint: int = 15
    priority: float = 0.0
    prompt: str | None = None

    def script(self) -> str:
        return " ".join(point.strip() for point in self.talking_points if point.strip())


@dataclass(frozen=True)
class Character:
    name: str
    image: Path
    visual_prompt: str = ""
    voice_prompt: str = ""


@dataclass(frozen=True)
class Playhead:
    index: int = 0


@dataclass(frozen=True)
class GenerateRequest:
    prompt: str
    output_path: Path
    brief: Brief
    duration: int
    image_path: Path | None = None


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


RenderPrompt = Callable[[Brief, Segment | None], str]


class Model(Protocol):
    def generate(self, request: GenerateRequest) -> Segment: ...


class Source(Protocol):
    def next_brief(self, playhead: Playhead | None = None) -> Brief | None: ...


class Continuity(Protocol):
    def start_frame(self, previous: Segment | None, character: Character | None) -> Path | None: ...
