
def find_root(f, init, /, *, args=(), kwargs=None,
              tolerances=None, maxiter=None, callback=None):
    """Find the root of a monotonic, real-valued function of a real variable.

    For each element of the output of `f`, `find_root` seeks the scalar
    root that makes the element 0. This function currently uses Chandrupatla's
    bracketing algorithm [1]_ and therefore requires argument `init` to
    provide a bracket around the root: the function values at the two endpoints
    must have opposite signs.

    Provided a valid bracket, `find_root` is guaranteed to converge to a solution
    that satisfies the provided `tolerances` if the function is continuous within
    the bracket.

    This function works elementwise when `init` and `args` contain (broadcastable)
    arrays.

    Parameters
    ----------
    f : callable
        The function whose root is desired. The signature must be::

            f(x: array, *args) -> array

        where each element of ``x`` is a finite real and ``args`` is a tuple,
        which may contain an arbitrary number of arrays that are broadcastable
        with ``x``.

        `f` must be an elementwise function: each element ``f(x)[i]``
        must equal ``f(x[i])`` for all indices ``i``. It must not mutate the
        array ``x`` or the arrays in ``args``.

        `find_root` seeks an array ``x`` such that ``f(x)`` is an array of zeros.
    init : 2-tuple of float array_like
        The lower and upper endpoints of a bracket surrounding the desired root.
        A bracket is valid if arrays ``xl, xr = init`` satisfy ``xl < xr`` and
        ``sign(f(xl)) == -sign(f(xr))`` elementwise. Arrays be broadcastable with
        one another and `args`.
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
    maxiter : int, optional
        The maximum number of iterations of the algorithm to perform.
        The default is the maximum possible number of bisections within
        the (normal) floating point numbers of the relevant dtype.
    callback : callable, optional
        An optional user-supplied function to be called before the first
        iteration and after each iteration.
        Called as ``callback(res)``, where ``res`` is a ``_RichResult``
        similar to that returned by `find_root` (but containing the current
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
            - ``-1`` : The initial bracket was invalid.
            - ``-2`` : The maximum number of iterations was reached.
            - ``-3`` : A non-finite value was encountered.
            - ``-4`` : Iteration was terminated by `callback`.
            - ``1`` : The algorithm is proceeding normally (in `callback` only).

        x : float array
            The root of the function, if the algorithm terminated successfully.
        f_x : float array
            The value of `f` evaluated at `x`.
        nfev : int array
            The number of abscissae at which `f` was evaluated to find the root.
            This is distinct from the number of times `f` is *called* because the
            the function may evaluated at multiple points in a single call.
        nit : int array
            The number of iterations of the algorithm that were performed.
        bracket : tuple of float arrays
            The lower and upper endpoints of the final bracket.
        f_bracket : tuple of float arrays
            The value of `f` evaluated at the lower and upper endpoints of the
            bracket.

    Notes
    -----
    Implemented based on Chandrupatla's original paper [1]_.

    Let:

    -  ``a, b = init`` be the left and right endpoints of the initial bracket,
    - ``xl`` and ``xr`` be the left and right endpoints of the final bracket,
    - ``xmin = xl if abs(f(xl)) <= abs(f(xr)) else xr`` be the final bracket
      endpoint with the smaller function value, and
    - ``fmin0 = min(f(a), f(b))`` be the minimum of the two values of the
      function evaluated at the initial bracket endpoints.

    Then the algorithm is considered to have converged when

    - ``abs(xr - xl) < xatol + abs(xmin) * xrtol`` or
    - ``fun(xmin) <= fatol + abs(fmin0) * frtol``.

    This is equivalent to the termination condition described in [1]_ with
    ``xrtol = 4e-10``, ``xatol = 1e-5``, and ``fatol = frtol = 0``.
    However, the default values of the `tolerances` dictionary are
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
    bracket_root

    Examples
    --------
    Suppose we wish to find the root of the following function.

    >>> def f(x, c=5):
    ...     return x**3 - 2*x - c

    First, we must find a valid bracket. The function is not monotonic,
    but `bracket_root` may be able to provide a bracket.

    >>> from scipy.optimize import elementwise
    >>> res_bracket = elementwise.bracket_root(f, 0)
    >>> res_bracket.success
    True
    >>> res_bracket.bracket
    (2.0, 4.0)

    Indeed, the values of the function at the bracket endpoints have
    opposite signs.

    >>> res_bracket.f_bracket
    (-1.0, 51.0)

    Once we have a valid bracket, `find_root` can be used to provide
    a precise root.

    >>> res_root = elementwise.find_root(f, res_bracket.bracket)
    >>> res_root.x
    2.0945514815423265

    The final bracket is only a few ULPs wide, so the error between
    this value and the true root cannot be much smaller within values
    that are representable in double precision arithmetic.

    >>> import numpy as np
    >>> xl, xr = res_root.bracket
    >>> (xr - xl) / np.spacing(xl)
    2.0
    >>> res_root.f_bracket
    (-8.881784197001252e-16, 9.769962616701378e-15)

    `bracket_root` and `find_root` accept arrays for most arguments.
    For instance, to find the root for a few values of the parameter ``c``
    at once:

    >>> c = np.asarray([3, 4, 5])
    >>> res_bracket = elementwise.bracket_root(f, 0, args=(c,))
    >>> res_bracket.bracket
    (array([1., 1., 2.]), array([2., 2., 4.]))
    >>> res_root = elementwise.find_root(f, res_bracket.bracket, args=(c,))
    >>> res_root.x
    array([1.8932892 , 2.        , 2.09455148])

    """

    def reformat_result(res_in):
        res_out = _RichResult()
        res_out.status = res_in.status
        res_out.success = res_in.success
        res_out.x = res_in.x
        res_out.f_x = res_in.fun
        res_out.nfev = res_in.nfev
        res_out.nit = res_in.nit
        res_out.bracket = (res_in.xl, res_in.xr)
        res_out.f_bracket = (res_in.fl, res_in.fr)
        res_out._order_keys = ['success', 'status', 'x', 'f_x',
                               'nfev', 'nit', 'bracket', 'f_bracket']
        return res_out

    xl, xr = init
    default_tolerances = dict(xatol=None, xrtol=None, fatol=None, frtol=0)
    tolerances = {} if tolerances is None else tolerances
    default_tolerances.update(tolerances)
    tolerances = default_tolerances

    if callable(callback):
        def _callback(res):
            return callback(reformat_result(res))
    else:
        _callback = callback

    res = _chandrupatla(f, xl, xr, args=args, kwargs=kwargs, **tolerances,
                        maxiter=maxiter, callback=_callback)
    return reformat_result(res)

