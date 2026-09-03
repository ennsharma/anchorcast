from __future__ import annotations

import os
import time
import urllib.request
from typing import Any, Literal

import fal_client

from anchorcast.media import probe_duration
from anchorcast.types import GenerateRequest, Segment


def ensure_fal_key() -> str:
    key = os.environ.get("FAL_KEY") or os.environ.get("FALAI_API_KEY")
    if not key:
        raise RuntimeError("Set FAL_KEY or FALAI_API_KEY (fal expects FAL_KEY).")
    os.environ["FAL_KEY"] = key
    return key


class H3Max:
    def __init__(
        self,
        *,
        model_id: str = "minimax/h3-max/image-to-video",
        resolution: Literal["480P", "768P"] = "768P",
        prompt_expansion_mode: Literal["balanced", "quality"] = "balanced",
    ) -> None:
        self.model_id = model_id
        self.resolution = resolution
        self.prompt_expansion_mode = prompt_expansion_mode

    def generate(self, request: GenerateRequest) -> Segment:
        ensure_fal_key()
        request.output_path.parent.mkdir(parents=True, exist_ok=True)
        image_url = fal_client.upload_file(str(request.image_path))
        started = time.perf_counter()
        result: dict[str, Any] = fal_client.subscribe(
            self.model_id,
            arguments={
                "prompt": request.prompt,
                "prompt_expansion_mode": self.prompt_expansion_mode,
                "image_url": image_url,
                "duration": request.duration,
                "resolution": self.resolution,
            },
            with_logs=False,
        )
        elapsed = time.perf_counter() - started
        video = result.get("video") or {}
        url = video.get("url")
        if not url:
            raise RuntimeError(f"H3 Max returned no video URL: {result!r}")
        urllib.request.urlretrieve(url, request.output_path)
        return Segment(
            path=request.output_path,
            duration=probe_duration(request.output_path),
            generated_in=elapsed,
            brief=request.brief,
        )
