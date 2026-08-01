
def _action_to_algebraic(action: int, num_cols: int) -> str:
    """Convert a pyspiel action id to algebraic notation.

    Amazons encodes every sub-action (from / to / shoot) as
    ``row * num_cols + col`` (0-indexed), so the same conversion works in
    all three phases regardless of the action_to_string format pyspiel
    happens to use. ``num_cols`` is read from the live observation rather
    than hardcoded because OpenSpiel ships different default sizes by build.
    """
    return _cell_to_algebraic(action // num_cols, action % num_cols)

