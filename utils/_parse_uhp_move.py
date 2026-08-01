
def _parse_uhp_move(move_str: str) -> tuple[str, str | None, str | None]:
    """Return (from_tile, ref_tile, direction).

    ``direction`` is one of the six cardinal directions, ``"Above"`` for a climb,
    or ``None`` for the first move of the game. ``ref_tile`` is ``None`` only
    for the first move.
    """
    if move_str == "pass":
        return ("pass", None, None)
    parts = move_str.split()
    from_tile = parts[0]
    if len(parts) == 1:
        return (from_tile, None, None)
    token = parts[1]
    if token.startswith("\\"):
        return (from_tile, token[1:], "NW")
    if token.startswith("/"):
        return (from_tile, token[1:], "SW")
    if token.startswith("-"):
        return (from_tile, token[1:], "W")
    if token.endswith("/"):
        return (from_tile, token[:-1], "NE")
    if token.endswith("-"):
        return (from_tile, token[:-1], "E")
    if token.endswith("\\"):
        return (from_tile, token[:-1], "SE")
    return (from_tile, token, "Above")

