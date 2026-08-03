import math


def nearest_enemy(obs, config=None):
    """Each owned planet sends half its ships to its nearest non-self
    planet that isn't already owned by us."""
    player = _get(obs, "player", 1)
    planets = _get(obs, "planets", []) or []
    moves = []
    for p in planets:
        if p[3] != player or p[4] < 2:
            continue
        ships = p[4] // 2
        candidates = [t for t in planets if t[3] != player]
        if not candidates:
            continue
        target = min(candidates, key=lambda t: math.hypot(p[1] - t[1], p[2] - t[2]))
        moves.append([p[0], target[0], ships])
    return moves

