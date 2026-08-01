
def ensure_wall_consistency(walls_dict, row_num, width):
    """Ensure north/south wall consistency between adjacent rows."""
    row_key = str(row_num)
    prev_key = str(row_num - 1)

    if row_key not in walls_dict:
        return

    row = walls_dict[row_key]

    # If previous row exists, sync south walls
    if prev_key in walls_dict:
        prev_row = walls_dict[prev_key]
        for c in range(width):
            # If current row has south wall, previous row must have north wall
            if row[c] & WALL_S:
                prev_row[c] |= WALL_N
            else:
                prev_row[c] &= ~WALL_N
            # If previous row has north wall, current row must have south wall
            if prev_row[c] & WALL_N:
                row[c] |= WALL_S
            else:
                row[c] &= ~WALL_S

