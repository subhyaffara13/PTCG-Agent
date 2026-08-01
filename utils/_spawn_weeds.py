
def _spawn_weeds(farm, board_size, weed_chance, rng):
    for y in range(board_size):
        for x in range(board_size):
            if farm["tiles"][y][x] is None and rng.random() < weed_chance:
                farm["tiles"][y][x] = {"kind": "WEED"}

