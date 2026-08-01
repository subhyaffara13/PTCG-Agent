
def splitCubicAtTC(pt1, pt2, pt3, pt4, *ts):
    """Split a cubic Bezier curve at one or more values of t.

    Args:
        pt1,pt2,pt3,pt4: Control points of the Bezier as complex numbers..
        *ts: Positions at which to split the curve.

    Yields:
        Curve segments (each curve segment being four complex numbers).
    """
    a, b, c, d = calcCubicParametersC(pt1, pt2, pt3, pt4)
    yield from _splitCubicAtTC(a, b, c, d, *ts)

