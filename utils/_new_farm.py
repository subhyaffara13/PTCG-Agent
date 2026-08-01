
def _new_farm(board_size, starting_money):
    return {
        "money": float(starting_money),
        # tiles[y][x] = None (empty unlocked) | "LOCKED" | dict structure
        "tiles": [
            [_initial_tile(x, y, board_size) for x in range(board_size)]
            for y in range(board_size)
        ],
        "farmer": list(_default_spawn(board_size)),
        "hands": [],
        "unlocked_quadrants": ["NW"],
        "hires_today": 0,
    }


def _new_farm(board_size, starting_money):
    return {
        "money": float(starting_money),
        "seeds": {crop: 0 for crop in CROPS},
        "farmer": [board_size - 1, board_size - 1],
        "tiles": [[None for _ in range(board_size)] for _ in range(board_size)],
    }

