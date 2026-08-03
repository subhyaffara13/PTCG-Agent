import math


def _chandrupatla(func, a, b, *, args=(), kwargs=None, xatol=None, xrtol=None,
                  fatol=None, frtol=0, maxiter=None, callback=None):
    """Find the root of an elementwise function using Chandrupatla's algorithm.

    For each element of the output of `func`, `chandrupatla` seeks the scalar
    root that makes the element 0. This function allows for `a`, `b`, and the
    output of `func` to be of any broadcastable shapes.

    Parameters
    ----------
    func : callable
        The function whose root is desired. The signature must be::

            func(x: ndarray, *args) -> ndarray

         where each element of ``x`` is a finite real and ``args`` is a tuple,
         which may contain an arbitrary number of components of any type(s).
         ``func`` must be an elementwise function: each element ``func(x)[i]``
         must equal ``func(x[i])`` for all indices ``i``. `_chandrupatla`
         seeks an array ``x`` such that ``func(x)`` is an array of zeros.
    a, b : array_like
        The lower and upper bounds of the root of the function. Must be
        broadcastable with one another.
    args : tuple, optional
        Additional positional arguments to be passed to `func`.
    kwargs : dict of str:array_like, optional
        Additional keyword arguments to be passed to `func`.
    xatol, xrtol, fatol, frtol : float, optional
        Absolute and relative tolerances on the root and function value.
        See Notes for details.
    maxiter : int, optional
        The maximum number of iterations of the algorithm to perform.
        The default is the maximum possible number of bisections within
        the (normal) floating point numbers of the relevant dtype.
    callback : callable, optional
        An optional user-supplied function to be called before the first
        iteration and after each iteration.
        Called as ``callback(res)``, where ``res`` is a ``_RichResult``
        similar to that returned by `_chandrupatla` (but containing the current
        iterate's values of all variables). If `callback` raises a
        ``StopIteration``, the algorithm will terminate immediately and
        `_chandrupatla` will return a result.

    Returns
    -------
    res : _RichResult
        An instance of `scipy._lib._util._RichResult` with the following
        attributes. The descriptions are written as though the values will be
        scalars; however, if `func` returns an array, the outputs will be
        arrays of the same shape.

        x : float
            The root of the function, if the algorithm terminated successfully.
        nfev : int
            The number of times the function was called to find the root.
        nit : int
            The number of iterations of Chandrupatla's algorithm performed.
        status : int
            An integer representing the exit status of the algorithm.
            ``0`` : The algorithm converged to the specified tolerances.
            ``-1`` : The algorithm encountered an invalid bracket.
            ``-2`` : The maximum number of iterations was reached.
            ``-3`` : A non-finite value was encountered.
            ``-4`` : Iteration was terminated by `callback`.
            ``1`` : The algorithm is proceeding normally (in `callback` only).
        success : bool
            ``True`` when the algorithm terminated successfully (status ``0``).
        fun : float
            The value of `func` evaluated at `x`.
        xl, xr : float
            The lower and upper ends of the bracket.
        fl, fr : float
            The function value at the lower and upper ends of the bracket.

    Notes
    -----
    Implemented based on Chandrupatla's original paper [1]_.

    If ``xl`` and ``xr`` are the left and right ends of the bracket,
    ``xmin = xl if abs(func(xl)) <= abs(func(xr)) else xr``,
    and ``fmin0 = min(func(a), func(b))``, then the algorithm is considered to
    have converged when ``abs(xr - xl) < xatol + abs(xmin) * xrtol`` or
    ``fun(xmin) <= fatol + abs(fmin0) * frtol``. This is equivalent to the
    termination condition described in [1]_ with ``xrtol = 4e-10``,
    ``xatol = 1e-5``, and ``fatol = frtol = 0``. The default values are
    ``xatol = 4*tiny``, ``xrtol = 4*eps``, ``frtol = 0``, and ``fatol = tiny``,
    where ``eps`` and ``tiny`` are the precision and smallest normal number
    of the result ``dtype`` of function inputs and outputs.

    References
    ----------

    .. [1] Chandrupatla, Tirupathi R.
        "A new hybrid quadratic/bisection algorithm for finding the zero of a
        nonlinear function without using derivatives".
        Advances in Engineering Software, 28(3), 145-149.
        :doi:`10.1016/s0965-9978(96)00051-8`.

    See Also
    --------
    brentq, brenth, ridder, bisect, newton

    Examples
    --------
    >>> from scipy import optimize
    >>> def f(x, c):
    ...     return x**3 - 2*x - c
    >>> c = 5
    >>> res = optimize._chandrupatla._chandrupatla(f, 0, 3, args=(c,))
    >>> res.x
    2.0945514818937463

    >>> c = [3, 4, 5]
    >>> res = optimize._chandrupatla._chandrupatla(f, 0, 3, args=(c,))
    >>> res.x
    array([1.8932892 , 2.        , 2.09455148])

    """
    res = _chandrupatla_iv(func, args, kwargs, xatol, xrtol,
                           fatol, frtol, maxiter, callback)
    func, args, kwargs, xatol, xrtol, fatol, frtol, maxiter, callback = res

    # Initialization
    temp = eim._initialize(func, (a, b), args, kwargs=kwargs)
    func, xs, fs, args, shape, dtype, xp = temp
    x1, x2 = xs
    f1, f2 = fs
    status = xp.full_like(x1, eim._EINPROGRESS,
                          dtype=xp.int32)  # in progress
    nit, nfev = 0, 2  # two function evaluations performed above
    finfo = xp.finfo(dtype)
    xatol = 4*finfo.smallest_normal if xatol is None else xatol
    xrtol = 4*finfo.eps if xrtol is None else xrtol
    fatol = finfo.smallest_normal if fatol is None else fatol
    frtol = frtol * xp.minimum(xp.abs(f1), xp.abs(f2))
    maxiter = (math.log2(finfo.max) - math.log2(finfo.smallest_normal)
               if maxiter is None else maxiter)
    work = _RichResult(x1=x1, f1=f1, x2=x2, f2=f2, x3=None, f3=None, t=0.5,
                       xatol=xatol, xrtol=xrtol, fatol=fatol, frtol=frtol,
                       nit=nit, nfev=nfev, status=status)
    res_work_pairs = [('status', 'status'), ('x', 'xmin'), ('fun', 'fmin'),
                      ('nit', 'nit'), ('nfev', 'nfev'), ('xl', 'x1'),
                      ('fl', 'f1'), ('xr', 'x2'), ('fr', 'f2')]

    def pre_func_eval(work):
        # [1] Figure 1 (first box)
        x = work.x1 + work.t * (work.x2 - work.x1)
        return x

    def post_func_eval(x, f, work):
        # [1] Figure 1 (first diamond and boxes)
        # Note: y/n are reversed in figure; compare to BASIC in appendix
        work.x3, work.f3 = (xp.asarray(work.x2, copy=True),
                            xp.asarray(work.f2, copy=True))
        j = xp.sign(f) == xp.sign(work.f1)
        nj = ~j
        work.x3[j], work.f3[j] = work.x1[j], work.f1[j]
        work.x2[nj], work.f2[nj] = work.x1[nj], work.f1[nj]
        work.x1, work.f1 = x, f

    def check_termination(work):
        # [1] Figure 1 (second diamond)
        # Check for all terminal conditions and record statuses.

        # See [1] Section 4 (first two sentences)
        i = xp.abs(work.f1) < xp.abs(work.f2)
        work.xmin = xp.where(i, work.x1, work.x2)
        work.fmin = xp.where(i, work.f1, work.f2)
        stop = xp.zeros_like(work.x1, dtype=xp.bool)  # termination condition met

        # If function value tolerance is met, report successful convergence,
        # regardless of other conditions. Note that `frtol` has been redefined
        # as `frtol = frtol * minimum(f1, f2)`, where `f1` and `f2` are the
        # function evaluated at the original ends of the bracket.
        i = xp.abs(work.fmin) <= work.fatol + work.frtol
        work.status[i] = eim._ECONVERGED
        stop[i] = True

        # If the bracket is no longer valid, report failure (unless a function
        # tolerance is met, as detected above).
        i = (xp.sign(work.f1) == xp.sign(work.f2)) & ~stop
        NaN = xp.asarray(xp.nan, dtype=work.xmin.dtype)
        work.xmin[i], work.fmin[i], work.status[i] = NaN, NaN, eim._ESIGNERR
        stop[i] = True

        # If the abscissae are non-finite or either function value is NaN,
        # report failure.
        x_nonfinite = ~(xp.isfinite(work.x1) & xp.isfinite(work.x2))
        f_nan = xp.isnan(work.f1) & xp.isnan(work.f2)
        i = (x_nonfinite | f_nan) & ~stop
        work.xmin[i], work.fmin[i], work.status[i] = NaN, NaN, eim._EVALUEERR
        stop[i] = True

        # This is the convergence criterion used in bisect. Chandrupatla's
        # criterion is equivalent to this except with a factor of 4 on `xrtol`.
        work.dx = xp.abs(work.x2 - work.x1)
        work.tol = xp.abs(work.xmin) * work.xrtol + work.xatol
        i = work.dx < work.tol
        work.status[i] = eim._ECONVERGED
        stop[i] = True

        return stop

    def post_termination_check(work):
        # [1] Figure 1 (third diamond and boxes / Equation 1)
        xi1 = (work.x1 - work.x2) / (work.x3 - work.x2)
        with np.errstate(divide='ignore', invalid='ignore'):
            phi1 = (work.f1 - work.f2) / (work.f3 - work.f2)
        alpha = (work.x3 - work.x1) / (work.x2 - work.x1)
        j = ((1 - xp.sqrt(1 - xi1)) < phi1) & (phi1 < xp.sqrt(xi1))

        f1j, f2j, f3j, alphaj = work.f1[j], work.f2[j], work.f3[j], alpha[j]
        t = xp.full_like(alpha, 0.5)
        t[j] = (f1j / (f1j - f2j) * f3j / (f3j - f2j)
                - alphaj * f1j / (f3j - f1j) * f2j / (f2j - f3j))

        # [1] Figure 1 (last box; see also BASIC in appendix with comment
        # "Adjust T Away from the Interval Boundary")
        tl = 0.5 * work.tol / work.dx
        work.t = xp.clip(t, tl, 1 - tl)

    def customize_result(res, shape):
        xl, xr, fl, fr = res['xl'], res['xr'], res['fl'], res['fr']
        i = res['xl'] < res['xr']
        res['xl'] = xp.where(i, xl, xr)
        res['xr'] = xp.where(i, xr, xl)
        res['fl'] = xp.where(i, fl, fr)
        res['fr'] = xp.where(i, fr, fl)
        return shape

    return eim._loop(work, callback, shape, maxiter, func, args, dtype,
                     pre_func_eval, post_func_eval, check_termination,
                     post_termination_check, customize_result, res_work_pairs,
                     xp=xp)

