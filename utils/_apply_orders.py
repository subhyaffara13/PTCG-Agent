
def _apply_orders(orders, planets, fleets, player_owner):
    """Deduct ships from sources and create (or merge into) fleets.

    Mirrors GameState::ExecuteOrder including the same-turn merge by
    matching (owner, source, dest, turns_remaining) — see game.cpp:162-208.

    Precondition: caller must have run `_validate_orders` first; this
    function trusts the orders are well-formed and within budget.
    """
    if not orders:
        return
    for order in orders:
        src, dst, ships = int(order[0]), int(order[1]), int(order[2])
        source = planets[src]
        dest = planets[dst]
        source[4] -= ships
        trip = distance((source[1], source[2]), (dest[1], dest[2]))
        existing = None
        for f in fleets:
            # f[5] == trip means the fleet was launched this same turn
            # (turns_remaining still equals total_trip), so it's the merge
            # target. In-flight fleets from earlier turns have f[5] < trip.
            if f[0] == player_owner and f[2] == src and f[3] == dst and f[5] == trip:
                existing = f
                break
        if existing is not None:
            existing[1] += ships
        else:
            fleets.append([player_owner, ships, src, dst, trip, trip])

