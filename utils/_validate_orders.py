
def _validate_orders(orders, planets, player_owner):
    """Replay a player's orders against a snapshot of their planet ships
    using the same checks as GameState::ExecuteOrder (game.cpp:180-210).

    Returns True iff `orders` is a list (possibly empty) and every order in
    it is valid. None is treated as invalid — "no action" is `[]`, and
    None only appears upstream when core.py marked the agent
    TIMEOUT/ERROR/INVALID.
    """
    if not isinstance(orders, list):
        return False
    if not orders:
        return True

    # Per-source running totals so we catch "sum of orders > planet ships".
    ships_remaining = {}
    num_planets = len(planets)
    for order in orders:
        if not isinstance(order, (list, tuple)) or len(order) != 3:
            return False
        try:
            src = int(order[0])
            dst = int(order[1])
            ships = int(order[2])
        except (TypeError, ValueError):
            return False
        if ships <= 0:
            return False
        if src < 0 or src >= num_planets:
            return False
        if dst < 0 or dst >= num_planets:
            return False
        if src == dst:
            return False
        source = planets[src]
        if source[3] != player_owner:
            return False
        available = ships_remaining.setdefault(src, source[4])
        if ships > available:
            return False
        ships_remaining[src] = available - ships
    return True

