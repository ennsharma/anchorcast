from __future__ import annotations

from examples.literary_bear.scripts import FORBIDDEN_OPENERS, write_script


def test_followup_scripts_do_not_reuse_stock_openers() -> None:
    previous = "Good afternoon, in a manner of speaking. Today's news has wandered into the wood."
    for index in range(1, 8):
        script = write_script(
            headline="Honey harvest delayed by rain",
            previous=previous,
            index=index,
        )
        previous = script
        lowered = script.lower()
        for opener in FORBIDDEN_OPENERS:
            assert not lowered.startswith(opener), script
        assert "i have just heard" not in lowered
        assert "oh, bother" not in lowered
        word_count = len(script.split())
        assert 20 <= word_count <= 60, script
