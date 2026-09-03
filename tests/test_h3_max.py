from __future__ import annotations

from pathlib import Path
from typing import Any

from anchorcast.models.h3_max import H3Max
from anchorcast.types import Brief, GenerateRequest


def test_h3_max_uses_text_to_video_when_no_start_image(
    monkeypatch: Any,
    tmp_path: Path,
) -> None:
    captured: dict[str, object] = {}

    monkeypatch.setenv("FAL_KEY", "test-key")
    monkeypatch.setattr(
        "anchorcast.models.h3_max.fal_client.upload_file",
        lambda path: (_ for _ in ()).throw(AssertionError("T2V should not upload an image")),
    )

    def fake_subscribe(model_id: str, arguments: dict[str, object], with_logs: bool = False) -> dict[str, object]:
        captured["model_id"] = model_id
        captured["arguments"] = arguments
        return {"video": {"url": "https://example.invalid/clip.mp4"}}

    monkeypatch.setattr("anchorcast.models.h3_max.fal_client.subscribe", fake_subscribe)
    monkeypatch.setattr(
        "anchorcast.models.h3_max.urllib.request.urlretrieve",
        lambda url, path: Path(path).write_bytes(b"mp4"),
    )
    monkeypatch.setattr("anchorcast.models.h3_max.probe_duration", lambda path: 15.0)

    output = tmp_path / "0000.mp4"
    brief = Brief(id="1", topic="kitten", prompt="A white kitten chases a butterfly.")
    H3Max().generate(
        GenerateRequest(
            prompt="A white kitten chases a butterfly.",
            image_path=None,
            output_path=output,
            brief=brief,
            duration=15,
        )
    )
    assert captured["model_id"] == "minimax/h3-max/text-to-video"
    args = captured["arguments"]
    assert isinstance(args, dict)
    assert "image_url" not in args
    assert args["prompt"] == "A white kitten chases a butterfly."
