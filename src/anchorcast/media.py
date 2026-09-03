from __future__ import annotations

import subprocess
from pathlib import Path


def extract_last_frame(video_path: Path, frame_path: Path) -> Path:
    frame_path.parent.mkdir(parents=True, exist_ok=True)
    duration = probe_duration(video_path)
    seek = max(0.0, duration - 0.08)
    result = subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-ss",
            f"{seek:.3f}",
            "-i",
            str(video_path),
            "-frames:v",
            "1",
            str(frame_path),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0 or not frame_path.exists() or frame_path.stat().st_size == 0:
        tail = (result.stderr or "").strip().splitlines()[-1:] or ["ffmpeg failed to extract last frame"]
        raise RuntimeError(tail[0])
    return frame_path


def probe_duration(video_path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(video_path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(result.stdout.strip())
