
def calc_intersect(a, b, c, d):
    """Calculate the intersection of two lines.

    Args:
        a (complex): Start point of first line.
        b (complex): End point of first line.
        c (complex): Start point of second line.
        d (complex): End point of second line.

    Returns:
        complex: Location of intersection if one present, ``complex(NaN,NaN)``
        if no intersection was found.
    """
    ab = b - a
    cd = d - c
    p = ab * 1j
    try:
        h = dot(p, a - c) / dot(p, cd)
    except ZeroDivisionError:
        # if 3 or 4 points are equal, we do have an intersection despite the zero-div:
        # return one of the off-curves so that the algorithm can attempt a one-curve
        # solution if it's within tolerance:
        # https://github.com/linebender/kurbo/pull/484
        if b == c and (a == b or c == d):
            return b
        return complex(NAN, NAN)
    return c + cd * h

