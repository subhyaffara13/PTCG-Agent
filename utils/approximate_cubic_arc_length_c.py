
def approximateCubicArcLengthC(pt1, pt2, pt3, pt4):
    """Approximates the arc length for a cubic Bezier segment.

    Args:
        pt1,pt2,pt3,pt4: Control points of the Bezier as complex numbers.

    Returns:
        Arc length value.
    """
    # This, essentially, approximates the length-of-derivative function
    # to be integrated with the best-matching seventh-degree polynomial
    # approximation of it.
    #
    # https://en.wikipedia.org/wiki/Gaussian_quadrature#Gauss.E2.80.93Lobatto_rules

    # abs(BezierCurveC[3].diff(t).subs({t:T})) for T in sorted(0, .5±(3/7)**.5/2, .5, 1),
    # weighted 1/20, 49/180, 32/90, 49/180, 1/20 respectively.
    v0 = abs(pt2 - pt1) * 0.15
    v1 = abs(
        -0.558983582205757 * pt1
        + 0.325650248872424 * pt2
        + 0.208983582205757 * pt3
        + 0.024349751127576 * pt4
    )
    v2 = abs(pt4 - pt1 + pt3 - pt2) * 0.26666666666666666
    v3 = abs(
        -0.024349751127576 * pt1
        - 0.208983582205757 * pt2
        - 0.325650248872424 * pt3
        + 0.558983582205757 * pt4
    )
    v4 = abs(pt4 - pt3) * 0.15

    return v0 + v1 + v2 + v3 + v4

