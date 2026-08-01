
def linePointAtT(pt1, pt2, t):
    """Finds the point at time `t` on a line.

    Args:
        pt1, pt2: Coordinates of the line as 2D tuples.
        t: The time along the line.

    Returns:
        A 2D tuple with the coordinates of the point.
    """
    return ((pt1[0] * (1 - t) + pt2[0] * t), (pt1[1] * (1 - t) + pt2[1] * t))

