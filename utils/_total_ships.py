
def _total_ships(planets, fleets, owner):
    total = 0
    for p in planets:
        if p[3] == owner:
            total += p[4]
    for f in fleets:
        if f[0] == owner:
            total += f[1]
    return total

