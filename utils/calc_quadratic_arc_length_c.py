
def calcQuadraticArcLengthC(pt1, pt2, pt3):
    """Calculates the arc length for a quadratic Bezier segment.

    Args:
        pt1: Start point of the Bezier as a complex number.
        pt2: Handle point of the Bezier as a complex number.
        pt3: End point of the Bezier as a complex number.

    Returns:
        Arc length value.
    """
    # Analytical solution to the length of a quadratic bezier.
    # Documentation: https://github.com/fonttools/fonttools/issues/3055
    d0 = pt2 - pt1
    d1 = pt3 - pt2
    d = d1 - d0
    n = d * 1j
    scale = abs(n)
    if scale == 0.0:
        return abs(pt3 - pt1)
    origDist = _dot(n, d0)
    if abs(origDist) < epsilon:
        if _dot(d0, d1) >= 0:
            return abs(pt3 - pt1)
        a, b = abs(d0), abs(d1)
        return (a * a + b * b) / (a + b)
    x0 = _dot(d, d0) / origDist
    x1 = _dot(d, d1) / origDist
    Len = abs(2 * (_intSecAtan(x1) - _intSecAtan(x0)) * origDist / (scale * (x1 - x0)))
    return Len

