
def _exec_move(game, action, player):
    """Handle move action."""
    from_x = int(action.get("from_x", -1))
    from_y = int(action.get("from_y", -1))
    to_x = int(action.get("to_x", -1))
    to_y = int(action.get("to_y", -1))
    unit = game.get_unit_at_position(from_x, from_y)
    if unit is None or unit.player != player:
        return False
    return game.move_unit(unit, to_x, to_y)

