
def _default_spawn(board_size):
    """First free shed-access tile, NWSE preference."""
    for tile in _shed_access_tiles(board_size):
        if _quadrant_of(tile[0], tile[1], board_size) == "NW":
            return tile
    return (0, 0)

