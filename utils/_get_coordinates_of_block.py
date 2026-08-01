
def _get_coordinates_of_block(x, y, width, height, angle=0):
    """
    Get the coordinates of rotated rectangle and rectangle that covers the
    rotated rectangle.
    """

    vertices = _calculate_quad_point_coordinates(x, y, width,
                                                 height, angle)

    # Find min and max values for rectangle
    # adjust so that QuadPoints is inside Rect
    # PDF docs says that QuadPoints should be ignored if any point lies
    # outside Rect, but for Acrobat it is enough that QuadPoints is on the
    # border of Rect.

    pad = 0.00001 if angle % 90 else 0
    min_x = min(v[0] for v in vertices) - pad
    min_y = min(v[1] for v in vertices) - pad
    max_x = max(v[0] for v in vertices) + pad
    max_y = max(v[1] for v in vertices) + pad
    return (tuple(itertools.chain.from_iterable(vertices)),
            (min_x, min_y, max_x, max_y))

