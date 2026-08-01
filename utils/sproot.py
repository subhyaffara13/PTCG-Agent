
def sproot(tck, mest=10):
    # see the docstring of `_fitpack_py/sproot`
    t, c, k = tck
    if k != 3:
        raise ValueError("sproot works only for cubic (k=3) splines")
    try:
        c[0][0]
        parametric = True
    except Exception:
        parametric = False
    if parametric:
        return list(map(lambda c, t=t, k=k, mest=mest:
                        sproot([t, c, k], mest), c))
    else:
        if len(t) < 8:
            raise TypeError(f"The number of knots {len(t)}>=8")
        z, m, ier = _fitpack.sproot(t, c, mest)
        if ier == 10:
            raise TypeError("Invalid input data. "
                            "t1<=..<=t4<t5<..<tn-3<=..<=tn must hold.")
        if ier == 0:
            return z[:m]
        if ier == 1:
            warnings.warn(RuntimeWarning("The number of zeros exceeds mest"),
                          stacklevel=2)
            return z[:m]
        raise TypeError("Unknown error")


def sproot(tck, mest=10):
    """
    Find the roots of a cubic B-spline.

    .. legacy:: function

        Specifically, we recommend constructing a `BSpline` object and using the
        following pattern: `PPoly.from_spline(spl).roots()`.

    Given the knots (>=8) and coefficients of a cubic B-spline return the
    roots of the spline.

    Parameters
    ----------
    tck : tuple or a BSpline object
        If a tuple, then it should be a sequence of length 3, containing the
        vector of knots, the B-spline coefficients, and the degree of the
        spline.
        The number of knots must be >= 8, and the degree must be 3.
        The knots must be a montonically increasing sequence.
    mest : int, optional
        An estimate of the number of zeros (Default is 10).

    Returns
    -------
    zeros : ndarray
        An array giving the roots of the spline.

    See Also
    --------
    splprep, splrep, splint, spalde, splev
    bisplrep, bisplev
    BSpline

    Notes
    -----
    Manipulating the tck-tuples directly is not recommended. In new code,
    prefer using the `BSpline` objects.

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

    For some data, this method may miss a root. This happens when one of
    the spline knots (which FITPACK places automatically) happens to
    coincide with the true root. A workaround is to convert to `PPoly`,
    which uses a different root-finding algorithm.

    For example,

    >>> x = [1.96, 1.97, 1.98, 1.99, 2.00, 2.01, 2.02, 2.03, 2.04, 2.05]
    >>> y = [-6.365470e-03, -4.790580e-03, -3.204320e-03, -1.607270e-03,
    ...      4.440892e-16,  1.616930e-03,  3.243000e-03,  4.877670e-03,
    ...      6.520430e-03,  8.170770e-03]
    >>> from scipy.interpolate import splrep, sproot, PPoly
    >>> tck = splrep(x, y, s=0)
    >>> sproot(tck)
    array([], dtype=float64)

    Converting to a PPoly object does find the roots at ``x=2``:

    >>> ppoly = PPoly.from_spline(tck)
    >>> ppoly.roots(extrapolate=False)
    array([2.])


    Further examples are given :ref:`in the tutorial
    <tutorial-interpolate_splXXX>`.

    """
    if isinstance(tck, BSpline):
        if tck.c.ndim > 1:
            mesg = ("Calling sproot() with BSpline objects with c.ndim > 1 is "
                    "not allowed.")
            raise ValueError(mesg)

        t, c, k = tck.tck

        # _impl.sproot expects the interpolation axis to be last, so roll it.
        # NB: This transpose is a no-op if c is 1D.
        sh = tuple(range(c.ndim))
        c = c.transpose(sh[1:] + (0,))
        return _impl.sproot((t, c, k), mest)
    else:
        return _impl.sproot(tck, mest)

