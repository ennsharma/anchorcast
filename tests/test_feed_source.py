from __future__ import annotations

from pathlib import Path

from anchorcast.sources.feed import FeedSource


def test_feed_maps_rss_items_to_cited_briefs(tmp_path: Path) -> None:
    rss = tmp_path / "feed.xml"
    rss.write_text(
        """<?xml version="1.0"?>
        <rss version="2.0">
          <channel>
            <title>Wood News</title>
            <item>
              <title>Honey harvest delayed</title>
              <link>https://example.com/honey</link>
            </item>
          </channel>
        </rss>
        """,
        encoding="utf-8",
    )
    source = FeedSource(str(rss))
    brief = source.next_brief()
    assert brief is not None
    assert brief.topic == "Honey harvest delayed"
    assert brief.citations == ("https://example.com/honey",)
    assert brief.kind == "story"
    assert source.next_brief() is None
