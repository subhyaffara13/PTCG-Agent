
def splev(x, tck, der=0, ext=0):
    # see the docstring of `_fitpack_py/splev`
    t, c, k = tck
    try:
        c[0][0]
        parametric = True
    except Exception:
        parametric = False
    if parametric:
        return list(map(lambda c, x=x, t=t, k=k, der=der:
                        splev(x, [t, c, k], der, ext), c))
    else:
        if not (0 <= der <= k):
            raise ValueError(f"0<=der={der}<=k={k} must hold")
        if ext not in (0, 1, 2, 3):
            raise ValueError(f"ext = {ext} not in (0, 1, 2, 3) ")

        x = asarray(x)
        shape = x.shape
        x = atleast_1d(x).ravel()
        if der == 0:
            y, ier = _fitpack.splev(t, c, k, x, ext)
        else:
            y, ier = _fitpack.splder(t, c, k, der, x, ext)

        if ier == 10:
            raise ValueError("Invalid input data")
        if ier == 1:
            raise ValueError("Found x value not in the domain")
        if ier:
            raise TypeError("An error occurred")

        return y.reshape(shape)


def splev(x, tck, der=0, ext=0):
    """
    Evaluate a B-spline or its derivatives.

    .. legacy:: function

        Specifically, we recommend constructing a `BSpline` object and using
        its ``__call__`` method.

    Given the knots and coefficients of a B-spline representation, evaluate
    the value of the smoothing polynomial and its derivatives. This is a
    wrapper around the FORTRAN routines splev and splder of FITPACK.

    Parameters
    ----------
    x : array_like
        An array of points at which to return the value of the smoothed
        spline or its derivatives. If `tck` was returned from `splprep`,
        then the parameter values, u should be given.
    tck : BSpline instance or tuple
        If a tuple, then it should be a sequence of length 3 returned by
        `splrep` or `splprep` containing the knots, coefficients, and degree
        of the spline. (Also see Notes.)
    der : int, optional
        The order of derivative of the spline to compute (must be less than
        or equal to k, the degree of the spline).
    ext : int, optional
        Controls the value returned for elements of ``x`` not in the
        interval defined by the knot sequence.

        * if ext=0, return the extrapolated value.
        * if ext=1, return 0
        * if ext=2, raise a ValueError
        * if ext=3, return the boundary value.

        The default value is 0.

    Returns
    -------
    y : ndarray or list of ndarrays
        An array of values representing the spline function evaluated at
        the points in `x`.  If `tck` was returned from `splprep`, then this
        is a list of arrays representing the curve in an N-D space.

    See Also
    --------
    splprep, splrep, sproot, spalde, splint
    bisplrep, bisplev
    BSpline

    Notes
    -----
    Manipulating the tck-tuples directly is not recommended. In new code,
    prefer using `BSpline` objects.

    References
    ----------
    .. [1] C. de Boor, "On calculating with b-splines", J. Approximation
        Theory, 6, p.50-62, 1972.
    .. [2] M. G. Cox, "The numerical evaluation of b-splines", J. Inst. Maths
        Applics, 10, p.134-149, 1972.
    .. [3] P. Dierckx, "Curve and surface fitting with splines", Monographs
        on Numerical Analysis, Oxford University Press, 1993.

    Examples
    --------
    Examples are given :ref:`in the tutorial <tutorial-interpolate_splXXX>`.

    A comparison between `splev`, `splder` and `spalde` to compute the derivatives of a 
    B-spline can be found in the `spalde` examples section.

    """
    if isinstance(tck, BSpline):
        if tck.c.ndim > 1:
            mesg = ("Calling splev() with BSpline objects with c.ndim > 1 is "
                    "not allowed. Use BSpline.__call__(x) instead.")
            raise ValueError(mesg)

        # remap the out-of-bounds behavior
        try:
            extrapolate = {0: True, }[ext]
        except KeyError as e:
            raise ValueError(f"Extrapolation mode {ext} is not supported "
                             "by BSpline.") from e

        return tck(x, der, extrapolate=extrapolate)
    else:
        return _impl.splev(x, tck, der, ext)

