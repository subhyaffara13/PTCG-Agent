
def can_move_through(walls_dict, width, col, row, direction):
    """Check if movement from (col, row) in direction is unblocked by walls."""
    row_key = str(row)
    if row_key not in walls_dict:
        return False
    row_walls = walls_dict[row_key]
    if col < 0 or col >= width:
        return False
    if row_walls[col] & DIR_WALL_BIT[direction]:
        return False
    dc, dr = DIR_OFFSETS[direction]
    nc, nr = col + dc, row + dr
    if nc < 0 or nc >= width:
        return False
    nr_key = str(nr)
    if nr_key not in walls_dict:
        return False
    return True

