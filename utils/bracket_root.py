
def bracket_root(f, xl0, xr0=None, *, xmin=None, xmax=None, factor=None,
                 args=(), kwargs=None, maxiter=1000):
    """Bracket the root of a monotonic, real-valued function of a real variable.

    For each element of the output of `f`, `bracket_root` seeks the scalar
    bracket endpoints ``xl`` and ``xr`` such that ``sign(f(xl)) == -sign(f(xr))``
    elementwise.

    The function is guaranteed to find a valid bracket if the function is monotonic,
    but it may find a bracket under other conditions.

    This function works elementwise when `xl0`, `xr0`, `xmin`, `xmax`, `factor`, and
    the elements of `args` are (mutually broadcastable) arrays.

    Parameters
    ----------
    f : callable
        The function for which the root is to be bracketed. The signature must be::

            f(x: array, *args) -> array

        where each element of ``x`` is a finite real and ``args`` is a tuple,
        which may contain an arbitrary number of arrays that are broadcastable
        with ``x``.

        `f` must be an elementwise function: each element ``f(x)[i]``
        must equal ``f(x[i])`` for all indices ``i``. It must not mutate the
        array ``x`` or the arrays in ``args``.
    xl0, xr0 : float array_like
        Starting guess of bracket, which need not contain a root. If `xr0` is
        not provided, ``xr0 = xl0 + 1``. Must be broadcastable with all other
        array inputs.
    xmin, xmax : float array_like, optional
        Minimum and maximum allowable endpoints of the bracket, inclusive. Must
        be broadcastable with all other array inputs.
    factor : float array_like, default: 2
        The factor used to grow the bracket. See Notes.
    args : tuple of array_like, optional
        Additional positional array arguments to be passed to `f`.
        If the callable for which the root is desired requires arguments that are
        not broadcastable with `x`, wrap that callable with `f` such that `f`
        accepts only `x` and broadcastable ``*args``.
    kwargs : dict of str:array_like, optional
        Additional keyword arguments to be passed to `f`. See `args`.
    maxiter : int, default: 1000
        The maximum number of iterations of the algorithm to perform.

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

            - ``0`` : The algorithm produced a valid bracket.
            - ``-1`` : The bracket expanded to the allowable limits without success.
            - ``-2`` : The maximum number of iterations was reached.
            - ``-3`` : A non-finite value was encountered.
            - ``-4`` : Iteration was terminated by `callback`.
            - ``-5``: The initial bracket does not satisfy`xmin <= xl0 < xr0 < xmax`.

        bracket : 2-tuple of float arrays
            The lower and upper endpoints of the bracket, if the algorithm
            terminated successfully.
        f_bracket : 2-tuple of float arrays
            The values of `f` evaluated at the endpoints of ``res.bracket``,
            respectively.
        nfev : int array
            The number of abscissae at which `f` was evaluated to find the root.
            This is distinct from the number of times `f` is *called* because the
            the function may evaluated at multiple points in a single call.
        nit : int array
            The number of iterations of the algorithm that were performed.

    Notes
    -----
    This function generalizes an algorithm found in pieces throughout the
    `scipy.stats` codebase. The strategy is to iteratively grow the bracket `(l, r)`
    until ``f(l) < 0 < f(r)`` or ``f(r) < 0 < f(l)``. The bracket grows to the left
    as follows.

    - If `xmin` is not provided, the distance between `xl0` and `l` is iteratively
      increased by `factor`.
    - If `xmin` is provided, the distance between `xmin` and `l` is iteratively
      decreased by `factor`. Note that this also *increases* the bracket size.

    Growth of the bracket to the right is analogous.

    Growth of the bracket in one direction stops when the endpoint is no longer
    finite, the function value at the endpoint is no longer finite, or the
    endpoint reaches its limiting value (`xmin` or `xmax`). Iteration terminates
    when the bracket stops growing in both directions, the bracket surrounds
    the root, or a root is found (by chance).

    If two brackets are found - that is, a bracket is found on both sides in
    the same iteration, the smaller of the two is returned.

    If roots of the function are found, both `xl` and `xr` are set to the
    leftmost root.

    See Also
    --------
    find_root

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

    `bracket_root` and `find_root` accept arrays for most arguments.
    For instance, to find the root for a few values of the parameter ``c``
    at once:

    >>> import numpy as np
    >>> c = np.asarray([3, 4, 5])
    >>> res_bracket = elementwise.bracket_root(f, 0, args=(c,))
    >>> res_bracket.bracket
    (array([1., 1., 2.]), array([2., 2., 4.]))
    >>> res_root = elementwise.find_root(f, res_bracket.bracket, args=(c,))
    >>> res_root.x
    array([1.8932892 , 2.        , 2.09455148])

    """  # noqa: E501

    res = _bracket_root(f, xl0, xr0=xr0, xmin=xmin, xmax=xmax, factor=factor,
                        args=args, kwargs=kwargs, maxiter=maxiter)
    res.bracket = res.xl, res.xr
    res.f_bracket = res.fl, res.fr
    del res.xl
    del res.xr
    del res.fl
    del res.fr
    return res

