from typing import Any

def _sub_turn_squares(
    state: Mapping[str, Any],
    move_history: list[str],
    phase: str,
    num_cols: int,
) -> tuple[str | None, str | None]:
    """Return ``(from_sq, to_sq)`` algebraic for the in-progress turn.

    Prefers the action ids surfaced by the updated proxy (always accurate);
    falls back to the trailing entries of ``move_history`` so the harness
    still works when dropped into a notebook where the proxy module isn't
    on the path (per ``deserialize_game_and_state`` comment at the top of
    this file).
    """
    from_sq: str | None = None
    to_sq: str | None = None
    from_id = state.get("from_action")
    to_id = state.get("to_action")
    if isinstance(from_id, int):
        from_sq = _action_to_algebraic(from_id, num_cols)
    if isinstance(to_id, int):
        to_sq = _action_to_algebraic(to_id, num_cols)
    if from_sq is None and phase == "to" and move_history:
        from_sq = move_history[-1]
    elif from_sq is None and phase == "shoot" and len(move_history) >= 2:
        from_sq = move_history[-2]
        to_sq = to_sq if to_sq is not None else move_history[-1]
    return from_sq, to_sq

