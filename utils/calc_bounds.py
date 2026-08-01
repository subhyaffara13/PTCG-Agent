
def calcBounds(array):
    """Calculate the bounding rectangle of a 2D points array.

    Args:
        array: A sequence of 2D tuples.

    Returns:
        A four-item tuple representing the bounding rectangle ``(xMin, yMin, xMax, yMax)``.
    """
    if not array:
        return 0, 0, 0, 0
    xs = [x for x, y in array]
    ys = [y for x, y in array]
    return min(xs), min(ys), max(xs), max(ys)

