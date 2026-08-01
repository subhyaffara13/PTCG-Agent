
def _exec_heal(game, action, player):
    """Handle heal action."""
    healer, target = _get_source_target(game, action, player, "C")
    if healer is None:
        return False
    return game.heal(healer, target) > 0

