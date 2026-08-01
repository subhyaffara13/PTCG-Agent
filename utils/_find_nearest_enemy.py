
def _find_nearest_enemy(ux, uy, enemy_units):
    """Find the nearest enemy unit by Manhattan distance."""
    return min(enemy_units, key=lambda e: abs(ux - e["x"]) + abs(uy - e["y"]))

