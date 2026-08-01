
def rectArea(rect):
    """Determine rectangle area.

    Args:
        rect: Bounding rectangle, expressed as tuples
            ``(xMin, yMin, xMax, yMax)``.

    Returns:
        The area of the rectangle.
    """
    (xMin, yMin, xMax, yMax) = rect
    return (yMax - yMin) * (xMax - xMin)

