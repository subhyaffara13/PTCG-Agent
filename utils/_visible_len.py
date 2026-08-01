
def _visible_len(s: str) -> int:
    """Return the visible length of a string, ignoring OSC 8 escape sequences."""
    return len(_OSC8_RE.sub("", s))


def _visible_len(s: str) -> int:
    return len(_strip_ansi(s))

