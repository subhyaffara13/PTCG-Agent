
def update_bounds(b, v):
    if v is None:
        return
    for axis in range(3):
        b[axis][0] = min([b[axis][0], v[axis]])
        b[axis][1] = max([b[axis][1], v[axis]])


def updateBounds(bounds, p, min=min, max=max):
    """Add a point to a bounding rectangle.

    Args:
        bounds: A bounding rectangle expressed as a tuple
            ``(xMin, yMin, xMax, yMax), or None``.
        p: A 2D tuple representing a point.
        min,max: functions to compute the minimum and maximum.

    Returns:
        The updated bounding rectangle ``(xMin, yMin, xMax, yMax)``.
    """
    (x, y) = p
    if bounds is None:
        return x, y, x, y
    xMin, yMin, xMax, yMax = bounds
    return min(xMin, x), min(yMin, y), max(xMax, x), max(yMax, y)

