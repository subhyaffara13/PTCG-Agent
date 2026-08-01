
def _get_source_target(game, action, player, required_type):
    """
    Extract source and target units from an action dict.

    Returns (source, target) or (None, None) if validation fails.
    """
    from_x = int(action.get("from_x", -1))
    from_y = int(action.get("from_y", -1))
    to_x = int(action.get("to_x", -1))
    to_y = int(action.get("to_y", -1))
    source = game.get_unit_at_position(from_x, from_y)
    target = game.get_unit_at_position(to_x, to_y)
    if source is None or target is None:
        return None, None
    # ``not source.can_attack``: heal/cure/paralyze/haste/buffs all consume the
    # unit's action (like attack/seize), so gate them the same way the action
    # mask does -- one such action per unit per turn.
    if source.player != player or source.type != required_type or not source.can_attack:
        return None, None
    return source, target

