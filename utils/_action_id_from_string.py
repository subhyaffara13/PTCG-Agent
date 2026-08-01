
def _action_id_from_string(state: pyspiel.State, action_str: str) -> int:
    """Look up the action id for ``action_str`` in the state's legal actions."""
    player = state.current_player()
    for a in state.legal_actions():
        if state.action_to_string(player, a) == action_str:
            return a
    raise ValueError(f"Action {action_str!r} not in legal actions for player {player}")

