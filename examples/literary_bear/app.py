from __future__ import annotations

import argparse
import json
import os
import threading
import time
import webbrowser
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from anchorcast import Character, Session
from anchorcast.continuity import LastFrameContinuity
from anchorcast.models import H3Max

from examples.literary_bear.source import LiteraryNewsSource

ROOT = Path(__file__).resolve().parent.parent.parent
EXAMPLE = Path(__file__).resolve().parent
PLAYER = EXAMPLE / "player.html"
DEFAULT_FEED = "https://feeds.bbci.co.uk/news/world/rss.xml"


def _character() -> Character:
    return Character(
        name="Bear",
        image=ROOT / "examples" / "characters" / "literary-bear" / "pooh-1926.png",
        visual_prompt=(
            "Hand-drawn 1926 E.H. Shepard book illustration of a stuffed bear of very little brain. "
            "Pencil and light watercolor on cream paper. Round stuffed body, no clothing, "
            "sitting in a quiet wood. Locked-off camera, gentle breathing, mouth moving to speech."
        ),
        voice_prompt="warm, soft, slightly posh, unhurried stuffed-bear cadence",
    )


class LiveState:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.generating = False
        self.error: str | None = None
        self._lock = threading.Lock()
        self._stop = threading.Event()

    def snapshot(self) -> dict[str, object]:
        with self._lock:
            clips = [
                {
                    "index": index,
                    "url": f"/media/{Path(segment.path).name}",
                    "topic": segment.brief.topic,
                    "script": segment.brief.script(),
                    "duration": segment.duration,
                    "generated_in": segment.generated_in,
                }
                for index, segment in enumerate(self.session.segments)
            ]
            generating = self.generating
            error = self.error
            playhead = max(self.session.playing_index, 0)
        return {
            "clips": clips,
            "generating": generating,
            "error": error,
            "buffer_target": self.session.buffer_clips,
            "buffer_ahead": max(0, len(clips) - playhead),
        }

    def heartbeat(self, playing_index: int) -> None:
        with self._lock:
            self.session.advance(playing_index)

    def loop(self) -> None:
        while not self._stop.is_set():
            with self._lock:
                self.generating = True
            try:
                event = self.session.pump()
                if event is not None:
                    clip = event.segment
                    print(
                        f"clip {event.index:02d}: {clip.duration:.1f}s in {clip.generated_in:.1f}s — {clip.brief.topic}",
                        flush=True,
                    )
                    print(f"        {clip.brief.script()}", flush=True)
            except Exception as exc:  # noqa: BLE001
                with self._lock:
                    self.error = str(exc)
                print(f"generation failed: {exc}", flush=True)
                time.sleep(8)
            finally:
                with self._lock:
                    self.generating = False
            time.sleep(0.4)

    def stop(self) -> None:
        self._stop.set()


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args: object, state: LiveState, **kwargs: object) -> None:
        self.state = state
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, format: str, *args: object) -> None:
        if self.path.startswith("/api/"):
            return
        super().log_message(format, *args)

    def do_GET(self) -> None:  # noqa: N802
        try:
            parsed = urlparse(self.path)
            if parsed.path in {"/", "/index.html"}:
                body = PLAYER.read_bytes()
                self._send(body, "text/html; charset=utf-8")
                return
            if parsed.path == "/api/state":
                body = json.dumps(self.state.snapshot()).encode("utf-8")
                self._send(body, "application/json")
                return
            if parsed.path.startswith("/media/"):
                name = Path(parsed.path).name
                path = self.state.session.workdir / name
                if not path.is_file():
                    self.send_error(404)
                    return
                data = path.read_bytes()
                self._send(data, "video/mp4")
                return
            super().do_GET()
        except (BrokenPipeError, ConnectionResetError):
            return

    def do_POST(self) -> None:  # noqa: N802
        try:
            if urlparse(self.path).path != "/api/heartbeat":
                self.send_error(404)
                return
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length) if length else b"{}"
            body = json.loads(raw.decode("utf-8") or "{}")
            self.state.heartbeat(int(body.get("playing_index", -1)))
            self._send(b'{"ok":true}', "application/json")
        except (BrokenPipeError, ConnectionResetError, ValueError, json.JSONDecodeError):
            return

    def _send(self, body: bytes, content_type: str) -> None:
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)


def dry_run(feed: str, llm: bool) -> None:
    source = LiteraryNewsSource(feed, llm=llm)
    print("Dry run — scripts only, no video.\n")
    for index in range(6):
        brief = source.next_brief()
        assert brief is not None
        print(f"{index:02d}  {brief.topic}")
        print(f"    {brief.script()}\n")


def live(feed: str, llm: bool, host: str, port: int) -> None:
    session = Session(
        model=H3Max(),
        character=_character(),
        source=LiteraryNewsSource(feed, llm=llm),
        workdir=ROOT / ".anchorcast" / "literary-bear",
        continuity=LastFrameContinuity(),
        buffer_clips=2,
    )
    state = LiveState(session)
    thread = threading.Thread(target=state.loop, name="director", daemon=True)
    thread.start()
    server = ThreadingHTTPServer((host, port), partial(Handler, state=state))
    url = f"http://{host}:{port}/"
    print(f"Literary bear livestream: {url}", flush=True)
    print("Ctrl+C to stop. Promo H3 Max 768P is about $0.30 per 15s clip.", flush=True)
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        state.stop()
        server.shutdown()


def main() -> None:
    parser = argparse.ArgumentParser(description="Continuous literary-bear news stream on Anchorcast.")
    parser.add_argument("--feed", default=DEFAULT_FEED, help="RSS/Atom URL")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--dry-run", action="store_true", help="Print continuing scripts without calling fal.")
    parser.add_argument("--llm", action="store_true", help="Write scripts with gpt-4o-mini (needs OPENAI_API_KEY).")
    parser.add_argument("--no-llm", action="store_true", help="Use rotating templates even if OPENAI_API_KEY is set.")
    args = parser.parse_args()
    llm = False if args.no_llm else (args.llm or bool(os.environ.get("OPENAI_API_KEY")))
    if args.dry_run:
        dry_run(args.feed, llm=llm)
        return
    live(args.feed, llm=llm, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
