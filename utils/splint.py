
def splint(a, b, tck, full_output=0):
    # see the docstring of `_fitpack_py/splint`
    t, c, k = tck
    try:
        c[0][0]
        parametric = True
    except Exception:
        parametric = False
    if parametric:
        return list(map(lambda c, a=a, b=b, t=t, k=k:
                        splint(a, b, [t, c, k]), c))
    else:
        aint = _fitpack.splint(t, c, k, a, b)
        if full_output:
            return aint, None
        else:
            return aint


def splint(a, b, tck, full_output=0):
    """
    Evaluate the definite integral of a B-spline between two given points.

    .. legacy:: function

        Specifically, we recommend constructing a `BSpline` object and using its
        ``integrate`` method.

    Parameters
    ----------
    a, b : float
        The end-points of the integration interval.
    tck : tuple or a BSpline instance
        If a tuple, then it should be a sequence of length 3, containing the
        vector of knots, the B-spline coefficients, and the degree of the
        spline (see `splev`).
    full_output : int, optional
        Non-zero to return optional output.

    Returns
    -------
    integral : float
        The resulting integral.
    wrk : ndarray
        An array containing the integrals of the normalized B-splines
        defined on the set of knots.
        (Only returned if `full_output` is non-zero)

    See Also
    --------
    splprep, splrep, sproot, spalde, splev
    bisplrep, bisplev
    BSpline

    Notes
    -----
    `splint` silently assumes that the spline function is zero outside the data
    interval (`a`, `b`).

    Manipulating the tck-tuples directly is not recommended. In new code,
    prefer using the `BSpline` objects.

    References
    ----------
    .. [1] P.W. Gaffney, The calculation of indefinite integrals of b-splines",
        J. Inst. Maths Applics, 17, p.37-41, 1976.
    .. [2] P. Dierckx, "Curve and surface fitting with splines", Monographs
        on Numerical Analysis, Oxford University Press, 1993.

    Examples
    --------
    Examples are given :ref:`in the tutorial <tutorial-interpolate_splXXX>`.

    """
    if isinstance(tck, BSpline):
        if tck.c.ndim > 1:
            mesg = ("Calling splint() with BSpline objects with c.ndim > 1 is "
                    "not allowed. Use BSpline.integrate() instead.")
            raise ValueError(mesg)

        if full_output != 0:
            mesg = (f"full_output = {full_output} is not supported. Proceeding as if "
                    "full_output = 0")

        return tck.integrate(a, b, extrapolate=False)
    else:
        return _impl.splint(a, b, tck, full_output)

