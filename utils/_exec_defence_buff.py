
def _exec_defence_buff(game, action, player):
    """Handle defence_buff action."""
    sorcerer, target = _get_source_target(game, action, player, "S")
    if sorcerer is None:
        return False
    return game.defence_buff(sorcerer, target)

