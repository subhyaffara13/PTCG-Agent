
def _step_toward(from_x, from_y, to_x, to_y, board, occupied, map_w, map_h):
    """
    Return the best adjacent position that moves toward the target.
    Uses simple greedy Manhattan distance minimisation.
    """
    best_pos = None
    best_dist = abs(from_x - to_x) + abs(from_y - to_y)

    non_walkable = {"w", "o"}

    for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        nx, ny = from_x + dx, from_y + dy
        if 0 <= nx < map_w and 0 <= ny < map_h:
            if (nx, ny) not in occupied:
                tile = board[ny][nx] if ny < len(board) and nx < len(board[ny]) else "o"
                if tile not in non_walkable:
                    dist = abs(nx - to_x) + abs(ny - to_y)
                    if dist < best_dist:
                        best_dist = dist
                        best_pos = (nx, ny)

    return best_pos

