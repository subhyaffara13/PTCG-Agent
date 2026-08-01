
def bracket_minimum(f, xm0, *, xl0=None, xr0=None, xmin=None, xmax=None,
                     factor=None, args=(), kwargs=None, maxiter=1000):
    """Bracket the minimum of a unimodal, real-valued function of a real variable.

    For each element of the output of `f`, `bracket_minimum` seeks the scalar
    bracket points ``xl < xm < xr`` such that ``fl >= fm <= fr`` where one of the
    inequalities is strict.

    The function is guaranteed to find a valid bracket if the function is
    strongly unimodal, but it may find a bracket under other conditions.

    This function works elementwise when `xm0`, `xl0`, `xr0`, `xmin`, `xmax`, `factor`,
    and the elements of `args` are (mutually broadcastable) arrays.

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
    xm0 : float array_like
        Starting guess for middle point of bracket.
    xl0, xr0 : float array_like, optional
        Starting guesses for left and right endpoints of the bracket. Must
        be broadcastable with all other array inputs.
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
            - ``-1`` : The bracket expanded to the allowable limits. Assuming
              unimodality, this implies the endpoint at the limit is a minimizer.
            - ``-2`` : The maximum number of iterations was reached.
            - ``-3`` : A non-finite value was encountered.
            - ``-4`` : ``None`` shall pass.
            - ``-5`` : The initial bracket does not satisfy
              `xmin <= xl0 < xm0 < xr0 <= xmax`.

        bracket : 3-tuple of float arrays
            The left, middle, and right points of the bracket, if the algorithm
            terminated successfully.
        f_bracket : 3-tuple of float arrays
            The function value at the left, middle, and right points of the bracket.
        nfev : int array
            The number of abscissae at which `f` was evaluated to find the root.
            This is distinct from the number of times `f` is *called* because the
            the function may evaluated at multiple points in a single call.
        nit : int array
            The number of iterations of the algorithm that were performed.

    Notes
    -----
    Similar to `scipy.optimize.bracket`, this function seeks to find real
    points ``xl < xm < xr`` such that ``f(xl) >= f(xm)`` and ``f(xr) >= f(xm)``,
    where at least one of the inequalities is strict. Unlike `scipy.optimize.bracket`,
    this function can operate in a vectorized manner on array input, so long as
    the input arrays are broadcastable with each other. Also unlike
    `scipy.optimize.bracket`, users may specify minimum and maximum endpoints
    for the desired bracket.

    Given an initial trio of points ``xl = xl0``, ``xm = xm0``, ``xr = xr0``,
    the algorithm checks if these points already give a valid bracket. If not,
    a new endpoint, ``w`` is chosen in the "downhill" direction, ``xm`` becomes the new
    opposite endpoint, and either `xl` or `xr` becomes the new middle point,
    depending on which direction is downhill. The algorithm repeats from here.

    The new endpoint `w` is chosen differently depending on whether or not a
    boundary `xmin` or `xmax` has been set in the downhill direction. Without
    loss of generality, suppose the downhill direction is to the right, so that
    ``f(xl) > f(xm) > f(xr)``. If there is no boundary to the right, then `w`
    is chosen to be ``xr + factor * (xr - xm)`` where `factor` is controlled by
    the user (defaults to 2.0) so that step sizes increase in geometric proportion.
    If there is a boundary, `xmax` in this case, then `w` is chosen to be
    ``xmax - (xmax - xr)/factor``, with steps slowing to a stop at
    `xmax`. This cautious approach ensures that a minimum near but distinct from
    the boundary isn't missed while also detecting whether or not the `xmax` is
    a minimizer when `xmax` is reached after a finite number of steps.

    See Also
    --------
    scipy.optimize.bracket
    scipy.optimize.elementwise.find_minimum

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

    `bracket_minimum` and `find_minimum` accept arrays for most arguments.
    For instance, to find the minimizers and minima for a few values of the
    parameter ``c`` at once:

    >>> import numpy as np
    >>> c = np.asarray([1, 1.5, 2])
    >>> res_bracket = elementwise.bracket_minimum(f, 0, args=(c,))
    >>> res_bracket.bracket
    (array([0. , 0.5, 0.5]), array([0.5, 1.5, 1.5]), array([1.5, 2.5, 2.5]))
    >>> res_minimum = elementwise.find_minimum(f, res_bracket.bracket, args=(c,))
    >>> res_minimum.x
    array([1.00000001, 1.5       , 2.        ])
    >>> res_minimum.f_x
    array([2., 2., 2.])

    """  # noqa: E501

    res = _bracket_minimum(f, xm0, xl0=xl0, xr0=xr0, xmin=xmin, xmax=xmax,
                           factor=factor, args=args, kwargs=kwargs, maxiter=maxiter)
    res.bracket = res.xl, res.xm, res.xr
    res.f_bracket = res.fl, res.fm, res.fr
    del res.xl
    del res.xm
    del res.xr
    del res.fl
    del res.fm
    del res.fr
    return res

