
def _ant_glyph(seat: int, carrying: bool) -> str:
    """Glyph for a teammate's ant within the team-local view.

    Uses the seat index (0..players_per_team-1) so both teams render
    identically regardless of which global player ids they happen to
    hold. Searching ants are digits; carrying ants are capital letters.
    """
    if not carrying:
        return str(seat) if 0 <= seat < 10 else "?"
    return chr(ord("A") + seat) if 0 <= seat < 26 else "?"


def _ant_glyph(ant_id: int, carrying: bool) -> str:
    """Single-char glyph for an ant. Digit if searching, capital A/B/...
    if carrying food. Falls back to ``?`` if ant_id is out of A-Z range.
    """
    if not carrying:
        return str(ant_id) if 0 <= ant_id < 10 else "?"
    return chr(ord("A") + ant_id) if 0 <= ant_id < 26 else "?"

