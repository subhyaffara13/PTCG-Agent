
def _exec_attack(game, action, player):
    """Handle attack action."""
    from_x = int(action.get("from_x", -1))
    from_y = int(action.get("from_y", -1))
    to_x = int(action.get("to_x", -1))
    to_y = int(action.get("to_y", -1))
    attacker = game.get_unit_at_position(from_x, from_y)
    target = game.get_unit_at_position(to_x, to_y)
    if attacker is None or target is None:
        return False
    # ``not attacker.can_attack`` mirrors get_legal_actions (which only offers
    # attack/seize/abilities while can_attack) and prevents a unit from acting
    # more than once per turn -- e.g. attacking twice or seizing a structure
    # to completion in a single turn.
    if attacker.player != player or target.player == player or not attacker.can_attack:
        return False
    game.attack(attacker, target)
    return True

