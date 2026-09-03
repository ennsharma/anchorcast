from __future__ import annotations

FORBIDDEN_OPENERS: tuple[str, ...] = (
    "oh, bother",
    "oh bother",
    "oh,",
    "ah,",
    "ah ",
    "well,",
    "quite ",
    "how ",
    "it seems",
    "i have just heard",
    "i am only a bear of very little brain",
    "one wonders",
    "i must confess",
    "i must say",
)

SCRIPT_MODEL = "gpt-5.6-luna"

_OPENINGS: tuple[str, ...] = (
    "Today the world has sent a little news into the wood. {headline}. I shall hold it carefully, like a pot that might spill.",
    "There is news, as there so often is. {headline}. I do not pretend to understand all of it, only to sit with it a moment.",
)

_MID: tuple[str, ...] = (
    "And then this: {headline}. I turn it over like a pebble and find I am no wiser, which is a familiar feeling.",
    "Which brings us, sideways, to {headline}. A large thing, I think, though it fits poorly in a small head.",
    "{headline}. Well. That is rather a lot of world at once. I shall breathe, and then think one small think about it.",
    "Meanwhile — it is always meanwhile, somewhere — {headline}. How very odd, and yet how like Tuesday.",
    "Not the same as before. {headline}. I am trying to keep the stories from mixing, like honey and condensed milk.",
    "If I may continue, {headline}. I say 'if I may' because nobody has asked me to stop, which is encouraging.",
    "Another leaf has blown in. {headline}. I pin it with a paw so it does not leave before I have looked.",
    "As for {headline}: I have no moral ready. I have only the sentence, and the sitting that comes after a sentence.",
)

_IDLE: tuple[str, ...] = (
    "Where was I. Honey, I think. Or the shape of a cloud that looked briefly like a jar. Never mind. The sitting is the important part.",
    "A small silence is also news, in its way. I shall keep it company until the next sentence arrives.",
    "I have not finished the last thought, which is just as well, because it was a very small thought and might blow away.",
    "The wood is doing nothing in particular, and I am helping it. This is a kind of work.",
)


def _spoken_headline(headline: str) -> str:
    words = headline.strip().rstrip(".").split()
    if len(words) > 16:
        return " ".join(words[:16])
    return " ".join(words)


def write_script(
    *,
    headline: str,
    previous: str,
    index: int,
    llm: bool = False,
) -> str:
    if llm:
        try:
            return _write_llm(headline=headline, previous=previous, index=index)
        except Exception:
            pass
    return _write_template(headline=headline, previous=previous, index=index)


def write_idle(*, previous: str, index: int) -> str:
    return _IDLE[index % len(_IDLE)]


def _write_template(*, headline: str, previous: str, index: int) -> str:
    spoken = _spoken_headline(headline)
    if index == 0 or not previous.strip():
        return _OPENINGS[index % len(_OPENINGS)].format(headline=spoken)
    return _MID[(index - 1) % len(_MID)].format(headline=spoken)


def _write_llm(*, headline: str, previous: str, index: int) -> str:
    from openai import OpenAI

    client = OpenAI()
    continuation = (
        "This is a continuation of an ongoing take. Pick up mid-thought. "
        f"The previous spoken line was: {previous}"
        if previous.strip()
        else "This is the first clip of the take."
    )
    response = client.chat.completions.create(
        model=SCRIPT_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You write spoken dialogue for a 1926 literary Winnie-the-Pooh "
                    "(A. A. Milne / E. H. Shepard, not Disney) on an ongoing radio take about the news. "
                    "About 35 to 45 words. Output only the spoken words. "
                    "Do not start with Oh, Ah, Well, Quite, How, It seems, One wonders, I must, or Oh bother. "
                    "Do not greet, recap, or sign off. Do not ask the listener a question. "
                    "Do not mention honey, bees, or the wood unless the headline does. "
                    "If this is a continuation, start mid-thought: a conjunction or the subject of the headline. "
                    "Do not invent facts beyond the headline. Vary the opening from the previous line. "
                    "Stay gentle, slightly posh, and a little confused — in the sentences, not in a stock preface."
                ),
            },
            {
                "role": "user",
                "content": f"{continuation}\nHeadline: {headline}",
            },
        ],
        reasoning_effort="low",
    )
    text = (response.choices[0].message.content or "").strip().strip('"')
    if not text:
        raise RuntimeError("empty script")
    lowered = text.lower()
    if any(lowered.startswith(opener) for opener in FORBIDDEN_OPENERS):
        raise RuntimeError("stock opener")
    return text
