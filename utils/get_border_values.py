
def get_border_values(surface, width, height):
    """Returns a list containing lists with the values of the surface's
    borders.
    """
    border_top = [surface.get_at((x, 0)) for x in range(width)]
    border_left = [surface.get_at((0, y)) for y in range(height)]
    border_right = [surface.get_at((width - 1, y)) for y in range(height)]
    border_bottom = [surface.get_at((x, height - 1)) for x in range(width)]

    return [border_top, border_left, border_right, border_bottom]

