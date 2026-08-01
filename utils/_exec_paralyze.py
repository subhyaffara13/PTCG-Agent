
def _exec_paralyze(game, action, player):
    """Handle paralyze action."""
    mage, target = _get_source_target(game, action, player, "M")
    if mage is None:
        return False
    return game.paralyze(mage, target)

