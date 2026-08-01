
def _execute_action(game, action, player):
    """
    Translate a single action dict into a GameState method call.

    Returns True on success, False on invalid action.
    """
    atype = action.get("type", "")

    handlers = {
        "create_unit": _exec_create_unit,
        "move": _exec_move,
        "attack": _exec_attack,
        "seize": _exec_seize,
        "heal": _exec_heal,
        "cure": _exec_cure,
        "paralyze": _exec_paralyze,
        "haste": _exec_haste,
        "defence_buff": _exec_defence_buff,
        "attack_buff": _exec_attack_buff,
        "end_turn": lambda _g, _a, _p: True,
    }

    handler = handlers.get(atype)
    if handler is None:
        return False

    try:
        return handler(game, action, player)
    except Exception:  # pylint: disable=broad-except
        logger.exception("Error executing action: %s", action)
        return False

