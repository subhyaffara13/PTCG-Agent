
def _exec_cure(game, action, player):
    """Handle cure action."""
    curer, target = _get_source_target(game, action, player, "C")
    if curer is None:
        return False
    return game.cure(curer, target)

