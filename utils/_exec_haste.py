
def _exec_haste(game, action, player):
    """Handle haste action."""
    sorcerer, target = _get_source_target(game, action, player, "S")
    if sorcerer is None:
        return False
    return game.haste(sorcerer, target)

