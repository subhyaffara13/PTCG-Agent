
def cubic_approx_control(t, p0, p1, p2, p3):
    """Approximate a cubic Bezier using a quadratic one.

    Args:
        t (double): Position of control point.
        p0 (complex): Start point of curve.
        p1 (complex): First handle of curve.
        p2 (complex): Second handle of curve.
        p3 (complex): End point of curve.

    Returns:
        complex: Location of candidate control point on quadratic curve.
    """
    _p1 = p0 + (p1 - p0) * 1.5
    _p2 = p3 + (p2 - p3) * 1.5
    return _p1 + (_p2 - _p1) * t

