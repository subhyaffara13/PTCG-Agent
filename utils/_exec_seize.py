
def _exec_seize(game, action, player):
    """Handle seize action."""
    x = int(action.get("x", -1))
    y = int(action.get("y", -1))
    unit = game.get_unit_at_position(x, y)
    # ``not unit.can_attack`` keeps a unit to one action per turn: without it a
    # unit could seize a structure repeatedly in a single turn (each seize deals
    # its HP as damage), capturing a tower/HQ far faster than intended.
    if unit is None or unit.player != player or not unit.can_attack:
        return False
    tile = game.grid.get_tile(x, y)
    if tile is None or not tile.is_capturable() or tile.player == player:
        return False
    game.seize(unit)
    return True

