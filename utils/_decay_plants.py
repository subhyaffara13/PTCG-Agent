
def _decay_plants(farm, step):
    board_size = len(farm["tiles"])
    for y in range(board_size):
        for x in range(board_size):
            tile = farm["tiles"][y][x]
            if not isinstance(tile, dict) or tile.get("kind") != "PLANT":
                continue
            mls = tile["max_lifespan_step"]
            if mls < 0 or step < mls:
                continue
            if (step - mls) % 2 != 0:
                continue
            tile["yield_units"] -= 1
            if tile["yield_units"] <= 0:
                farm["tiles"][y][x] = {"kind": "WEED"}


def _decay_plants(farm, step):
    """One-time crops past their max lifespan lose 1 yield_unit every other
    turn (offsets 0, 2, 4, ... after max_lifespan_step). Plants are removed
    when yield_units hits zero."""
    board_size = len(farm["tiles"])
    for y in range(board_size):
        for x in range(board_size):
            tile = farm["tiles"][y][x]
            if tile is None:
                continue
            mls = tile["max_lifespan_step"]
            if mls < 0 or step < mls:
                continue
            if (step - mls) % 2 != 0:
                continue
            tile["yield_units"] -= 1
            if tile["yield_units"] <= 0:
                farm["tiles"][y][x] = None

