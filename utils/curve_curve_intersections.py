
def curveCurveIntersections(curve1, curve2):
    """Finds intersections between a curve and a curve.

    Args:
        curve1: List of coordinates of the first curve segment as 2D tuples.
        curve2: List of coordinates of the second curve segment as 2D tuples.

    Returns:
        A list of ``Intersection`` objects, each object having ``pt``, ``t1``
        and ``t2`` attributes containing the intersection point, time on first
        segment and time on second segment respectively.

    Examples::
        >>> curve1 = [ (10,100), (90,30), (40,140), (220,220) ]
        >>> curve2 = [ (5,150), (180,20), (80,250), (210,190) ]
        >>> intersections = curveCurveIntersections(curve1, curve2)
        >>> len(intersections)
        3
        >>> intersections[0].pt
        (81.7831487395506, 109.88904552375288)
    """
    if _is_linelike(curve1):
        line1 = curve1[0], curve1[-1]
        if _is_linelike(curve2):
            line2 = curve2[0], curve2[-1]
            return lineLineIntersections(*line1, *line2)
        else:
            hits = curveLineIntersections(curve2, line1)
            # curve is passed first to this fn but is the second segment, so
            # we need to swap t1/t2 in the result
            return [Intersection(pt=x.pt, t1=x.t2, t2=x.t1) for x in hits]
    elif _is_linelike(curve2):
        line2 = curve2[0], curve2[-1]
        return curveLineIntersections(curve1, line2)

    intersection_ts = _curve_curve_intersections_t(curve1, curve2)
    return [
        Intersection(pt=segmentPointAtT(curve1, ts[0]), t1=ts[0], t2=ts[1])
        for ts in intersection_ts
    ]

