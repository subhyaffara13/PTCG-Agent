
def is_fixed_wall(col, direction, width):
    """Walls workers cannot build or remove: E/W perimeter and the central mirror axis."""
    if direction == "WEST" and col == 0:
        return True
    if direction == "EAST" and col == width - 1:
        return True
    half = width // 2
    if direction == "EAST" and col == half - 1:
        return True
    if direction == "WEST" and col == half:
        return True
    return False

