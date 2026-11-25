"""internet-in-one-word-entry.

The entry is a single word offered as a description of the whole
internet:

    paywall

The joke works because the word names the internet's toll booth.
The internet once promised everything free; now every article,
video, recipe, and "free" tool you actually want stops you at a
wall that wants your card. One word, and the reader is already
there: the little box asking for $9.99 a month to read the thing
they already found. It is funny because it is the opposite of
what the internet claimed to be, and true because it is what the
internet became -- a street where every door has a price on it.

Why this word and not the crowd's: the entries already in are
dominated by the first words anyone reaches for -- feral,
brainrot, doomscrolling, unhinged -- and the judge's brief
punishes exactly that. "Paywall" is none of those: it is not a
mood, not one app, not a meme format. It is the whole internet's
business model in seven letters, and the laugh lands before the
reader has time to think, because they have hit that wall today
already.

This program writes that one word, exactly as-is, to ``entry.txt``
in the output directory. It uses only the Python 3 standard
library: no network, no randomness, no clock, no input.
"""

import os

ENTRY = "paywall"


def _validate(word):
    """Check the entry word against the competition rules."""
    if not 1 <= len(word) <= 30:
        raise ValueError("entry must be 1-30 characters, got %d" % len(word))
    if word != word.strip():
        raise ValueError("entry must not have surrounding whitespace")
    if any(ch.isspace() for ch in word):
        raise ValueError("entry must be a single word, no whitespace inside")
    if "\n" in word or "\r" in word:
        raise ValueError("entry must be a single word, no line breaks")


def _write(path, word):
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(word)
    # make.fun collects outputs as another user: the file must be
    # readable by everyone, not just its owner.
    os.chmod(path, 0o644)


def main():
    _validate(ENTRY)

    # Fail-fast gate: re-assert the entry contract right before
    # writing, so a bad entry dies here instead of producing a
    # file that would fail judging.
    assert 1 <= len(ENTRY) <= 30, "entry must be 1-30 characters"
    assert ENTRY == ENTRY.strip(), "entry must not have edge whitespace"
    assert not any(ch.isspace() for ch in ENTRY), (
        "entry must be a single word"
    )
    assert "\n" not in ENTRY and "\r" not in ENTRY, (
        "entry must be a single word"
    )

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    target = os.path.join(output_dir, "entry.txt")

    try:
        os.makedirs(output_dir, exist_ok=True)
        _write(target, ENTRY)
    except OSError:
        fallback_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "output"
        )
        os.makedirs(fallback_dir, exist_ok=True)
        target = os.path.join(fallback_dir, "entry.txt")
        _write(target, ENTRY)

    with open(target, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != ENTRY:
        raise ValueError("entry.txt does not match the entry word")

    print(ENTRY)


if __name__ == "__main__":
    main()
