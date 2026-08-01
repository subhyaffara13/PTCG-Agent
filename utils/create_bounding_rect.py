
def create_bounding_rect(surface, surf_color, default_pos):
    """Create a rect to bound all the pixels that don't match surf_color.

    The default_pos parameter is used to position the bounding rect for the
    case where all pixels match the surf_color.
    """
    width, height = surface.get_clip().size
    xmin, ymin = width, height
    xmax, ymax = -1, -1
    get_at = surface.get_at  # For possible speed up.

    surface.lock()  # For possible speed up.

    for y in range(height):
        for x in range(width):
            if get_at((x, y)) != surf_color:
                xmin = min(x, xmin)
                xmax = max(x, xmax)
                ymin = min(y, ymin)
                ymax = max(y, ymax)

    surface.unlock()

    if -1 == xmax:
        # No points means a 0 sized rect positioned at default_pos.
        return pygame.Rect(default_pos, (0, 0))
    return pygame.Rect((xmin, ymin), (xmax - xmin + 1, ymax - ymin + 1))


def create_bounding_rect(points):
    """Creates a bounding rect from the given points."""
    xmin = xmax = points[0][0]
    ymin = ymax = points[0][1]

    for x, y in points[1:]:
        xmin = min(x, xmin)
        xmax = max(x, xmax)
        ymin = min(y, ymin)
        ymax = max(y, ymax)

    return pygame.Rect((xmin, ymin), (xmax - xmin + 1, ymax - ymin + 1))

