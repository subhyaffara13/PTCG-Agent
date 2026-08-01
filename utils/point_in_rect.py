
def pointInRect(p, rect):
    """Test if a point is inside a bounding rectangle.

    Args:
        p: A 2D tuple representing a point.
        rect: A bounding rectangle expressed as a tuple
            ``(xMin, yMin, xMax, yMax)``.

    Returns:
        ``True`` if the point is inside the rectangle, ``False`` otherwise.
    """
    (x, y) = p
    xMin, yMin, xMax, yMax = rect
    return (xMin <= x <= xMax) and (yMin <= y <= yMax)

