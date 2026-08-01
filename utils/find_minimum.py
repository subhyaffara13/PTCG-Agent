
def find_minimum(f, init, /, *, args=(), kwargs=None,
                 tolerances=None, maxiter=100, callback=None):
    """Find the minimum of a unimodal, real-valued function of a real variable.

    For each element of the output of `f`, `find_minimum` seeks the scalar minimizer
    that minimizes the element. This function currently uses Chandrupatla's
    bracketing minimization algorithm [1]_ and therefore requires argument `init`
    to provide a three-point minimization bracket: ``x1 < x2 < x3`` such that
    ``func(x1) >= func(x2) <= func(x3)``, where one of the inequalities is strict.

    Provided a valid bracket, `find_minimum` is guaranteed to converge to a local
    minimum that satisfies the provided `tolerances` if the function is continuous
    within the bracket.

    This function works elementwise when `init` and `args` contain (broadcastable)
    arrays.

    Parameters
    ----------
    f : callable
        The function whose minimizer is desired. The signature must be::

            f(x: array, *args) -> array

        where each element of ``x`` is a finite real and ``args`` is a tuple,
        which may contain an arbitrary number of arrays that are broadcastable
        with ``x``.

        `f` must be an elementwise function: each element ``f(x)[i]``
        must equal ``f(x[i])`` for all indices ``i``. It must not mutate the
        array ``x`` or the arrays in ``args``.

        `find_minimum` seeks an array ``x`` such that ``f(x)`` is an array of
        local minima.
    init : 3-tuple of float array_like
        The abscissae of a standard scalar minimization bracket. A bracket is
        valid if arrays ``x1, x2, x3 = init`` satisfy ``x1 < x2 < x3`` and
        ``func(x1) >= func(x2) <= func(x3)``, where one of the inequalities
        is strict. Arrays must be broadcastable with one another and the arrays
        of `args`.
    args : tuple of array_like, optional
        Additional positional array arguments to be passed to `f`. Arrays
        must be broadcastable with one another and the arrays of `init`.
        If the callable for which the root is desired requires arguments that are
        not broadcastable with `x`, wrap that callable with `f` such that `f`
        accepts only `x` and broadcastable ``*args``.
    kwargs : dict of str:array_like, optional
        Additional keyword arguments to be passed to `f`. See `args`.
    tolerances : dictionary of floats, optional
        Absolute and relative tolerances on the root and function value.
        Valid keys of the dictionary are:

        - ``xatol`` - absolute tolerance on the root
        - ``xrtol`` - relative tolerance on the root
        - ``fatol`` - absolute tolerance on the function value
        - ``frtol`` - relative tolerance on the function value

        See Notes for default values and explicit termination conditions.
    maxiter : int, default: 100
        The maximum number of iterations of the algorithm to perform.
    callback : callable, optional
        An optional user-supplied function to be called before the first
        iteration and after each iteration.
        Called as ``callback(res)``, where ``res`` is a ``_RichResult``
        similar to that returned by `find_minimum` (but containing the current
        iterate's values of all variables). If `callback` raises a
        ``StopIteration``, the algorithm will terminate immediately and
        `find_root` will return a result. `callback` must not mutate
        `res` or its attributes.

    Returns
    -------
    res : _RichResult
        An object similar to an instance of `scipy.optimize.OptimizeResult` with the
        following attributes. The descriptions are written as though the values will
        be scalars; however, if `f` returns an array, the outputs will be
        arrays of the same shape.

        success : bool array
            ``True`` where the algorithm terminated successfully (status ``0``);
            ``False`` otherwise.
        status : int array
            An integer representing the exit status of the algorithm.

            - ``0`` : The algorithm converged to the specified tolerances.
            - ``-1`` : The algorithm encountered an invalid bracket.
            - ``-2`` : The maximum number of iterations was reached.
            - ``-3`` : A non-finite value was encountered.
            - ``-4`` : Iteration was terminated by `callback`.
            - ``1`` : The algorithm is proceeding normally (in `callback` only).

        x : float array
            The minimizer of the function, if the algorithm terminated successfully.
        f_x : float array
            The value of `f` evaluated at `x`.
        nfev : int array
            The number of abscissae at which `f` was evaluated to find the root.
            This is distinct from the number of times `f` is *called* because the
            the function may evaluated at multiple points in a single call.
        nit : int array
            The number of iterations of the algorithm that were performed.
        bracket : tuple of float arrays
            The final three-point bracket.
        f_bracket : tuple of float arrays
            The value of `f` evaluated at the bracket points.

    Notes
    -----
    Implemented based on Chandrupatla's original paper [1]_.

    If ``xl < xm < xr`` are the points of the bracket and ``fl >= fm <= fr``
    (where one of the inequalities is strict) are the values of `f` evaluated
    at those points, then the algorithm is considered to have converged when:

    - ``abs(xr - xm)/2 <= abs(xm)*xrtol + xatol`` or
    - ``(fl - 2*fm + fr)/2 <= abs(fm)*frtol + fatol``.

    The default value of `xrtol` is the square root of the precision of the
    appropriate dtype, and ``xatol = fatol = frtol`` is the smallest normal
    number of the appropriate dtype.

    References
    ----------

    .. [1] Chandrupatla, Tirupathi R. (1998).
        "An efficient quadratic fit-sectioning algorithm for minimization
        without derivatives".
        Computer Methods in Applied Mechanics and Engineering, 152 (1-2),
        211-217. :doi:`10.1016/S0045-7825(97)00190-4`.

    See Also
    --------
    bracket_minimum

    Examples
    --------
    Suppose we wish to minimize the following function.

    >>> def f(x, c=1):
    ...     return (x - c)**2 + 2

    First, we must find a valid bracket. The function is unimodal,
    so `bracket_minium` will easily find a bracket.

    >>> from scipy.optimize import elementwise
    >>> res_bracket = elementwise.bracket_minimum(f, 0)
    >>> res_bracket.success
    True
    >>> res_bracket.bracket
    (0.0, 0.5, 1.5)

    Indeed, the bracket points are ordered and the function value
    at the middle bracket point is less than at the surrounding
    points.

    >>> xl, xm, xr = res_bracket.bracket
    >>> fl, fm, fr = res_bracket.f_bracket
    >>> (xl < xm < xr) and (fl > fm <= fr)
    True

    Once we have a valid bracket, `find_minimum` can be used to provide
    an estimate of the minimizer.

    >>> res_minimum = elementwise.find_minimum(f, res_bracket.bracket)
    >>> res_minimum.x
    1.0000000149011612

    The function value changes by only a few ULPs within the bracket, so
    the minimizer cannot be determined much more precisely by evaluating
    the function alone (i.e. we would need its derivative to do better).

    >>> import numpy as np
    >>> fl, fm, fr = res_minimum.f_bracket
    >>> (fl - fm) / np.spacing(fm), (fr - fm) / np.spacing(fm)
    (0.0, 2.0)

    Therefore, a precise minimum of the function is given by:

    >>> res_minimum.f_x
    2.0

    `bracket_minimum` and `find_minimum` accept arrays for most arguments.
    For instance, to find the minimizers and minima for a few values of the
    parameter ``c`` at once:

    >>> c = np.asarray([1, 1.5, 2])
    >>> res_bracket = elementwise.bracket_minimum(f, 0, args=(c,))
    >>> res_bracket.bracket
    (array([0. , 0.5, 0.5]), array([0.5, 1.5, 1.5]), array([1.5, 2.5, 2.5]))
    >>> res_minimum = elementwise.find_minimum(f, res_bracket.bracket, args=(c,))
    >>> res_minimum.x
    array([1.00000001, 1.5       , 2.        ])
    >>> res_minimum.f_x
    array([2., 2., 2.])

    """

    def reformat_result(res_in):
        res_out = _RichResult()
        res_out.status = res_in.status
        res_out.success = res_in.success
        res_out.x = res_in.x
        res_out.f_x = res_in.fun
        res_out.nfev = res_in.nfev
        res_out.nit = res_in.nit
        res_out.bracket = (res_in.xl, res_in.xm, res_in.xr)
        res_out.f_bracket = (res_in.fl, res_in.fm, res_in.fr)
        res_out._order_keys = ['success', 'status', 'x', 'f_x',
                               'nfev', 'nit', 'bracket', 'f_bracket']
        return res_out

    xl, xm, xr = init
    default_tolerances = dict(xatol=None, xrtol=None, fatol=None, frtol=None)
    tolerances = {} if tolerances is None else tolerances
    default_tolerances.update(tolerances)
    tolerances = default_tolerances

    if callable(callback):
        def _callback(res):
            return callback(reformat_result(res))
    else:
        _callback = callback

    res = _chandrupatla_minimize(f, xl, xm, xr, args=args, kwargs=kwargs, **tolerances,
                                 maxiter=maxiter, callback=_callback)
    return reformat_result(res)

