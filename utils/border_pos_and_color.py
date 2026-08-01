
def border_pos_and_color(surface):
    """Yields each border position and its color for a given surface.

    Clockwise from the top left corner.
    """
    width, height = surface.get_size()
    right, bottom = width - 1, height - 1

    # Top edge.
    for x in range(width):
        pos = (x, 0)
        yield pos, surface.get_at(pos)

    # Right edge.
    # Top right done in top edge loop.
    for y in range(1, height):
        pos = (right, y)
        yield pos, surface.get_at(pos)

    # Bottom edge.
    # Bottom right done in right edge loop.
    for x in range(right - 1, -1, -1):
        pos = (x, bottom)
        yield pos, surface.get_at(pos)

    # Left edge.
    # Bottom left done in bottom edge loop. Top left done in top edge loop.
    for y in range(bottom - 1, 0, -1):
        pos = (0, y)
        yield pos, surface.get_at(pos)

