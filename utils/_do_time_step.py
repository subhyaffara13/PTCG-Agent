
def _do_time_step(planets, fleets):
    """Advance one turn: decrement fleets, grow planets, resolve arrivals,
    drop landed fleets. Mirrors GameState::DoTimeStep (game.cpp:123-130).
    """
    for f in fleets:
        if f[5] > 0:
            f[5] -= 1

    arrivals_by_planet = {}
    for f in fleets:
        if f[5] == 0:
            arrivals_by_planet.setdefault(f[3], []).append(f)

    for p in planets:
        if p[3] > 0:
            p[4] += p[5]
        arriving = arrivals_by_planet.get(p[0])
        if p[3] != 0 or arriving:
            _fight_battle(p, arriving or ())

    fleets[:] = [f for f in fleets if f[5] > 0]

