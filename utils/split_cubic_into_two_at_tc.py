
def splitCubicIntoTwoAtTC(pt1, pt2, pt3, pt4, t):
    """Split a cubic Bezier curve at t.

    Args:
        pt1,pt2,pt3,pt4: Control points of the Bezier as complex numbers.
        t: Position at which to split the curve.

    Returns:
        A tuple of two curve segments (each curve segment being four complex numbers).
    """
    t2 = t * t
    _1_t = 1 - t
    _1_t_2 = _1_t * _1_t
    _2_t_1_t = 2 * t * _1_t
    pointAtT = (
        _1_t_2 * _1_t * pt1 + 3 * (_1_t_2 * t * pt2 + _1_t * t2 * pt3) + t2 * t * pt4
    )
    off1 = _1_t_2 * pt1 + _2_t_1_t * pt2 + t2 * pt3
    off2 = _1_t_2 * pt2 + _2_t_1_t * pt3 + t2 * pt4

    pt2 = pt1 + (pt2 - pt1) * t
    pt3 = pt4 + (pt3 - pt4) * _1_t

    return ((pt1, pt2, off1, pointAtT), (pointAtT, off2, pt3, pt4))

