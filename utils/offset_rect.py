
def offsetRect(rect, dx, dy):
    """Offset a bounding box rectangle.

    Args:
        rect: A bounding rectangle expressed as a tuple
            ``(xMin, yMin, xMax, yMax)``.
        dx: Amount to offset the rectangle along the X axis.
        dY: Amount to offset the rectangle along the Y axis.

    Returns:
        An offset bounding rectangle.
    """
    (xMin, yMin, xMax, yMax) = rect
    return xMin + dx, yMin + dy, xMax + dx, yMax + dy

