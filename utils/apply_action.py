
def apply_action(game_state: dict, action: str) -> dict:
    gs = fast_clone_state(game_state)
    hand = list(gs.get("my_hand", []))

    _resolve_base(gs, hand, action)
    gs.pop("legal_actions", None)
    _regenerate_legal_actions(gs)
    _check_win_conditions(gs)
    return gs


def apply_action(game_state: dict, action: str) -> dict:
    gs = fast_clone_state(game_state)
    hand = list(gs.get("my_hand", []))

    _resolve_base(gs, hand, action)
    gs.pop("legal_actions", None)
    _regenerate_legal_actions(gs)
    _check_win_conditions(gs)
    return gs


def apply_action(game_state: dict, action: str) -> dict:
    gs = fast_clone_state(game_state)
    hand = list(gs.get("my_hand", []))

    if action.endswith("_heads") or action.endswith("_tails"):
        _resolve_base(gs, hand, action)
        gs.pop("legal_actions", None)
        _regenerate_legal_actions(gs)
        _check_win_conditions(gs)
        return gs

    _resolve_base(gs, hand, action)
    gs.pop("legal_actions", None)
    _regenerate_legal_actions(gs)
    _check_win_conditions(gs)
    return gs

