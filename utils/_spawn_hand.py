
def _spawn_hand(farm, board_size):
    """First free shed-access tile (NWSE order); ties broken by min occupancy."""
    occupants = {tile: 0 for tile in _shed_access_tiles(board_size)}
    all_pos = [tuple(farm["farmer"])] + [tuple(p) for p in farm["hands"]]
    for pos in all_pos:
        if pos in occupants:
            occupants[pos] += 1
    best = sorted(occupants.items(), key=lambda kv: (kv[1], _shed_access_tiles(board_size).index(kv[0])))
    return list(best[0][0])

