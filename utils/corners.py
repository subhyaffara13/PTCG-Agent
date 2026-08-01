
def corners(surface):
    """Returns a tuple with the corner positions of the given surface.

    Clockwise from the top left corner.
    """
    width, height = surface.get_size()
    return ((0, 0), (width - 1, 0), (width - 1, height - 1), (0, height - 1))


def corners(mask):
    """Returns a tuple with the corner positions of the given mask.

    Clockwise from the top left corner.
    """
    width, height = mask.get_size()
    return ((0, 0), (width - 1, 0), (width - 1, height - 1), (0, height - 1))

