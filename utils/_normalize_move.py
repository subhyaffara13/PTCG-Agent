
def _normalize_move(raw: str) -> str:
    """Lowercase, strip whitespace, and remove obvious wrappers."""
    s = raw.strip().lower()
    # Strip surrounding quotes/brackets and trailing punctuation a model
    # might add (e.g. `{"move": "a7a6."}` or `{"move": "a7a6,"}`).
    s = s.strip("`'\"<>[](){}.,!? \t\n")
    # Remove any internal whitespace ("a7 a6" or "a7\ta6") that some models
    # insert between the from/to squares.
    s = "".join(s.split())
    # Some models write moves with separators OpenSpiel doesn't use: a dash
    # ("a7-a6"), an 'x' ("b2xc3"), or an arrow ("a7->a6"). Drop them so the
    # from/to squares concatenate. "->" first so the arrow is removed as a
    # unit rather than leaving a stray ">".
    s = s.replace("->", "").replace("-", "").replace("x", "")
    return s


def _normalize_move(token: str) -> str:
    return _NOTATION_NOISE_RE.sub("", token.lower())


def _normalize_move(raw: str) -> str | None:
    """Normalize a move string to the canonical ``h r c`` / ``v r c`` form."""
    if not raw:
        return None
    m = _MOVE_TOKEN_RE.search(raw)
    if not m:
        return None
    orientation = m.group(1).lower()
    return f"{orientation} {int(m.group(2))} {int(m.group(3))}"

