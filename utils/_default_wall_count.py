
def _default_wall_count(params: Mapping[str, Any]) -> int:
    """Quoridor's per-player wall budget.

    OpenSpiel's parameter_specification claims the default is 0 but the C++
    constructor falls back to board_size^2 / 8 only when wall_count is absent
    from the param dict -- not when it's explicitly 0. Both the proxy's
    ``load_game`` path and the wall-counter need the formula.
    """
    raw = int(params.get("wall_count", 0))
    if raw > 0:
        return raw
    board_size = int(params.get("board_size", 9))
    return (board_size * board_size) // 8

