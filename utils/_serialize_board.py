
def _serialize_board(game):
    """Convert the game grid to a 2D array of terrain type codes."""
    board = []
    for y in range(game.grid.height):
        row = []
        for x in range(game.grid.width):
            tile = game.grid.get_tile(x, y)
            row.append(tile.type)
        board.append(row)
    return board

