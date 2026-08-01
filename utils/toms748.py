
def toms748(f, a, b, args=(), k=1,
            xtol=_xtol, rtol=_rtol, maxiter=_iter,
            full_output=False, disp=True):
    """
    Find a root using TOMS Algorithm 748 method.

    Implements the Algorithm 748 method of Alefeld, Potro and Shi to find a
    root of the function `f` on the interval ``[a , b]``, where `f(a)` and
    `f(b)` must have opposite signs.

    It uses a mixture of inverse cubic interpolation and
    "Newton-quadratic" steps. [APS1995].

    Parameters
    ----------
    f : function
        Python function returning a scalar. The function :math:`f`
        must be continuous, and :math:`f(a)` and :math:`f(b)`
        have opposite signs.
    a : scalar,
        lower boundary of the search interval
    b : scalar,
        upper boundary of the search interval
    args : tuple, optional
        containing extra arguments for the function `f`.
        `f` is called by ``f(x, *args)``.
    k : int, optional
        The number of Newton quadratic steps to perform each
        iteration. ``k>=1``.
    xtol : scalar, optional
        The computed root ``x0`` will satisfy ``np.isclose(x, x0,
        atol=xtol, rtol=rtol)``, where ``x`` is the exact root. The
        parameter must be positive.
    rtol : scalar, optional
        The computed root ``x0`` will satisfy ``np.isclose(x, x0,
        atol=xtol, rtol=rtol)``, where ``x`` is the exact root.
    maxiter : int, optional
        If convergence is not achieved in `maxiter` iterations, an error is
        raised. Must be >= 0.
    full_output : bool, optional
        If `full_output` is False, the root is returned. If `full_output` is
        True, the return value is ``(x, r)``, where `x` is the root, and `r` is
        a `RootResults` object.
    disp : bool, optional
        If True, raise RuntimeError if the algorithm didn't converge.
        Otherwise, the convergence status is recorded in the `RootResults`
        return object.

    Returns
    -------
    root : float
        Approximate root of `f`
    r : `RootResults` (present if ``full_output = True``)
        Object containing information about the convergence. In particular,
        ``r.converged`` is True if the routine converged.

    See Also
    --------
    brentq, brenth, ridder, bisect, newton
    fsolve : find roots in N dimensions.
    elementwise.find_root : efficient elementwise 1-D root-finder

    Notes
    -----
    `f` must be continuous.
    Algorithm 748 with ``k=2`` is asymptotically the most efficient
    algorithm known for finding roots of a four times continuously
    differentiable function.
    In contrast with Brent's algorithm, which may only decrease the length of
    the enclosing bracket on the last step, Algorithm 748 decreases it each
    iteration with the same asymptotic efficiency as it finds the root.

    For easy statement of efficiency indices, assume that `f` has 4
    continuous deriviatives.
    For ``k=1``, the convergence order is at least 2.7, and with about
    asymptotically 2 function evaluations per iteration, the efficiency
    index is approximately 1.65.
    For ``k=2``, the order is about 4.6 with asymptotically 3 function
    evaluations per iteration, and the efficiency index 1.66.
    For higher values of `k`, the efficiency index approaches
    the kth root of ``(3k-2)``, hence ``k=1`` or ``k=2`` are
    usually appropriate.

    As mentioned in the parameter documentation, the computed root ``x0`` will
    satisfy ``np.isclose(x, x0, atol=xtol, rtol=rtol)``, where ``x`` is the
    exact root. In equation form, this terminating condition is ``abs(x - x0)
    <= xtol + rtol * abs(x0)``.

    The default value ``xtol=2e-12`` may lead to surprising behavior if one
    expects `toms748` to always compute roots with relative error near machine
    precision. Care should be taken to select `xtol` for the use case at hand.
    Setting ``xtol=5e-324``, the smallest subnormal number, will ensure the
    highest level of accuracy. Larger values of `xtol` may be useful for saving
    function evaluations when a root is at or near zero in applications where
    the tiny absolute differences available between floating point numbers near
    zero are not meaningful.

    References
    ----------
    .. [APS1995]
       Alefeld, G. E. and Potra, F. A. and Shi, Yixun,
       *Algorithm 748: Enclosing Zeros of Continuous Functions*,
       ACM Trans. Math. Softw. Volume 221(1995)
       https://doi.org/10.1145/210089.210111

    Examples
    --------
    >>> def f(x):
    ...     return (x**3 - 1)  # only one real root at x = 1

    >>> from scipy import optimize
    >>> root, results = optimize.toms748(f, 0, 2, full_output=True)
    >>> root
    1.0
    >>> results
          converged: True
               flag: converged
     function_calls: 11
         iterations: 5
               root: 1.0
             method: toms748
    """
    if xtol <= 0:
        raise ValueError(f"xtol too small ({xtol:g} <= 0)")
    if rtol < _rtol / 4:
        raise ValueError(f"rtol too small ({rtol:g} < {_rtol/4:g})")
    maxiter = operator.index(maxiter)
    if maxiter < 1:
        raise ValueError("maxiter must be greater than 0")
    if not np.isfinite(a):
        raise ValueError(f"a is not finite {a}")
    if not np.isfinite(b):
        raise ValueError(f"b is not finite {b}")
    if a >= b:
        raise ValueError(f"a and b are not an interval [{a}, {b}]")
    if not k >= 1:
        raise ValueError(f"k too small ({k} < 1)")

    if not isinstance(args, tuple):
        args = (args,)
    f = _wrap_nan_raise(f)
    solver = TOMS748Solver()
    result = solver.solve(f, a, b, args=args, k=k, xtol=xtol, rtol=rtol,
                          maxiter=maxiter, disp=disp)
    x, function_calls, iterations, flag = result
    return _results_select(full_output, (x, function_calls, iterations, flag),
                           "toms748")

