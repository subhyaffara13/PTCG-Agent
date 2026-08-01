
def _exec_attack_buff(game, action, player):
    """Handle attack_buff action."""
    sorcerer, target = _get_source_target(game, action, player, "S")
    if sorcerer is None:
        return False
    return game.attack_buff(sorcerer, target)

