
def _alive_players(planets, fleets):
    alive = set()
    for p in planets:
        if p[3] > 0:
            alive.add(p[3])
    for f in fleets:
        if f[0] > 0:
            alive.add(f[0])
    return alive

