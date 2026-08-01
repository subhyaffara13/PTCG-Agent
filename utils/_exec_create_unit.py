
def _exec_create_unit(game, action, player):
    """Handle create_unit action."""
    unit_type = action.get("unit_type", "")
    x = int(action.get("x", -1))
    y = int(action.get("y", -1))
    if unit_type not in UNIT_DATA:
        return False
    return game.create_unit(unit_type, x, y, player) is not None

