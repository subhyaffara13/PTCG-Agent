
def ridder(f, a, b, args=(),
           xtol=_xtol, rtol=_rtol, maxiter=_iter,
           full_output=False, disp=True):
    """
    Find a root of a function in an interval using Ridder's method.

    Parameters
    ----------
    f : function
        Python function returning a number. f must be continuous, and f(a) and
        f(b) must have opposite signs.
    a : scalar
        One end of the bracketing interval [a,b].
    b : scalar
        The other end of the bracketing interval [a,b].
    args : tuple, optional
        Containing extra arguments for the function `f`.
        `f` is called by ``apply(f, (x)+args)``.
    xtol : number, optional
        The computed root ``x0`` will satisfy ``np.isclose(x, x0,
        atol=xtol, rtol=rtol)``, where ``x`` is the exact root. The
        parameter must be positive.
    rtol : number, optional
        The computed root ``x0`` will satisfy ``np.isclose(x, x0,
        atol=xtol, rtol=rtol)``, where ``x`` is the exact root. The
        parameter cannot be smaller than its default value of
        ``4*np.finfo(float).eps``.
    maxiter : int, optional
        If convergence is not achieved in `maxiter` iterations, an error is
        raised. Must be >= 0.
    full_output : bool, optional
        If `full_output` is False, the root is returned. If `full_output` is
        True, the return value is ``(x, r)``, where `x` is the root, and `r` is
        a `RootResults` object.
    disp : bool, optional
        If True, raise RuntimeError if the algorithm didn't converge.
        Otherwise, the convergence status is recorded in any `RootResults`
        return object.

    Returns
    -------
    root : float
        Root of `f` between `a` and `b`.
    r : `RootResults` (present if ``full_output = True``)
        Object containing information about the convergence.
        In particular, ``r.converged`` is True if the routine converged.

    See Also
    --------
    brentq, brenth, bisect, newton : 1-D root-finding
    fixed_point : scalar fixed-point finder
    elementwise.find_root : efficient elementwise 1-D root-finder

    Notes
    -----
    Uses [Ridders1979]_ method to find a root of the function `f` between the
    arguments `a` and `b`. Ridders' method is faster than bisection, but not
    generally as fast as the Brent routines. [Ridders1979]_ provides the
    classic description and source of the algorithm. A description can also be
    found in any recent edition of Numerical Recipes.

    The routine used here diverges slightly from standard presentations in
    order to be a bit more careful of tolerance.

    As mentioned in the parameter documentation, the computed root ``x0`` will
    satisfy ``np.isclose(x, x0, atol=xtol, rtol=rtol)``, where ``x`` is the
    exact root. In equation form, this terminating condition is ``abs(x - x0)
    <= xtol + rtol * abs(x0)``.

    The default value ``xtol=2e-12`` may lead to surprising behavior if one
    expects `ridder` to always compute roots with relative error near machine
    precision. Care should be taken to select `xtol` for the use case at hand.
    Setting ``xtol=5e-324``, the smallest subnormal number, will ensure the
    highest level of accuracy. Larger values of `xtol` may be useful for saving
    function evaluations when a root is at or near zero in applications where
    the tiny absolute differences available between floating point numbers near
    zero are not meaningful.

    References
    ----------
    .. [Ridders1979]
       Ridders, C. F. J. "A New Algorithm for Computing a
       Single Root of a Real Continuous Function."
       IEEE Trans. Circuits Systems 26, 979-980, 1979.

    Examples
    --------

    >>> def f(x):
    ...     return (x**2 - 1)

    >>> from scipy import optimize

    >>> root = optimize.ridder(f, 0, 2)
    >>> root
    1.0

    >>> root = optimize.ridder(f, -2, 0)
    >>> root
    -1.0
    """
    if not isinstance(args, tuple):
        args = (args,)
    maxiter = operator.index(maxiter)
    if xtol <= 0:
        raise ValueError(f"xtol too small ({xtol:g} <= 0)")
    if rtol < _rtol:
        raise ValueError(f"rtol too small ({rtol:g} < {_rtol:g})")
    f = _wrap_nan_raise(f)
    r = _zeros._ridder(f, a, b, xtol, rtol, maxiter, args, full_output, disp)
    return results_c(full_output, r, "ridder")

