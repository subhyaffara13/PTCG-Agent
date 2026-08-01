
def curves_to_quadratic(curves, max_errors, all_quadratic=True):
    """Return quadratic Bezier splines approximating the input cubic Beziers.

    Args:
        curves: A sequence of *n* curves, each curve being a sequence of four
            2D tuples.
        max_errors: A sequence of *n* floats representing the maximum permissible
            deviation from each of the cubic Bezier curves.
        all_quadratic (bool): If True (default) returned values are a
            quadratic spline. If False, they are either a single quadratic
            curve or a single cubic curve.

    Example::

        >>> curves_to_quadratic( [
        ...   [ (50,50), (100,100), (150,100), (200,50) ],
        ...   [ (75,50), (120,100), (150,75),  (200,60) ]
        ... ], [1,1] )
        [[(50.0, 50.0), (75.0, 75.0), (125.0, 91.66666666666666), (175.0, 75.0), (200.0, 50.0)], [(75.0, 50.0), (97.5, 75.0), (135.41666666666666, 82.08333333333333), (175.0, 67.5), (200.0, 60.0)]]

    The returned splines have "implied oncurve points" suitable for use in
    TrueType ``glif`` outlines - i.e. in the first spline returned above,
    the first quadratic segment runs from (50,50) to
    ( (75 + 125)/2 , (120 + 91.666..)/2 ) = (100, 83.333...).

    Returns:
        If all_quadratic is True, a list of splines, each spline being a list
        of 2D tuples. If ``curves`` is empty, returns an empty list.

        If all_quadratic is False, a list of curves, each curve being a quadratic
        (length 3), or cubic (length 4).

    Raises:
        ValueError: if ``max_errors`` does not match the number of curves.
        fontTools.cu2qu.errors.ApproxNotFoundError: if no suitable approximation
        can be found for all curves with the given parameters.
    """

    curves = [[complex(*p) for p in curve] for curve in curves]
    if len(max_errors) != len(curves):
        raise ValueError("max_errors must match the number of curves")
    if not curves:
        return []

    l = len(curves)
    splines = [None] * l
    last_i = i = 0
    n = 1
    while True:
        spline = cubic_approx_spline(curves[i], n, max_errors[i], all_quadratic)
        if spline is None:
            if n == MAX_N:
                break
            n += 1
            last_i = i
            continue
        splines[i] = spline
        i = (i + 1) % l
        if i == last_i:
            # done. go home
            return [[(s.real, s.imag) for s in spline] for spline in splines]

    raise ApproxNotFoundError(curves)

