
def minimize_scalar(fun, bracket=None, bounds=None, args=(),
                    method=None, tol=None, options=None):
    """Local minimization of scalar function of one variable.

    Parameters
    ----------
    fun : callable
        Objective function.
        Scalar function, must return a scalar.

        Suppose the callable has signature ``f0(x, *my_args, **my_kwargs)``, where
        ``my_args`` and ``my_kwargs`` are required positional and keyword arguments.
        Rather than passing ``f0`` as the callable, wrap it to accept
        only ``x``; e.g., pass ``fun=lambda x: f0(x, *my_args, **my_kwargs)`` as the
        callable, where ``my_args`` (tuple) and ``my_kwargs`` (dict) have been
        gathered before invoking this function.

    bracket : sequence, optional
        For methods 'brent' and 'golden', `bracket` defines the bracketing
        interval and is required.
        Either a triple ``(xa, xb, xc)`` satisfying ``xa < xb < xc`` and
        ``func(xb) < func(xa) and  func(xb) < func(xc)``, or a pair
        ``(xa, xb)`` to be used as initial points for a downhill bracket search
        (see `scipy.optimize.bracket`).
        The minimizer ``res.x`` will not necessarily satisfy
        ``xa <= res.x <= xb``.
    bounds : sequence, optional
        For method 'bounded', `bounds` is mandatory and must have two finite
        items corresponding to the optimization bounds.
    args : tuple, optional
        Extra arguments passed to the objective function.
    method : str or callable, optional
        Type of solver.  Should be one of:

        - :ref:`Brent <optimize.minimize_scalar-brent>`
        - :ref:`Bounded <optimize.minimize_scalar-bounded>`
        - :ref:`Golden <optimize.minimize_scalar-golden>`
        - custom - a callable object (added in version 0.14.0), see below

        Default is "Bounded" if bounds are provided and "Brent" otherwise.
        See the 'Notes' section for details of each solver.

    tol : float, optional
        Tolerance for termination. For detailed control, use solver-specific
        options.
    options : dict, optional
        A dictionary of solver options.

        maxiter : int
            Maximum number of iterations to perform.
        disp : bool
            Set to True to print convergence messages.

        See :func:`show_options()` for solver-specific options.

    Returns
    -------
    res : OptimizeResult
        The optimization result represented as a ``OptimizeResult`` object.
        Important attributes are: ``x`` the solution array, ``success`` a
        Boolean flag indicating if the optimizer exited successfully and
        ``message`` which describes the cause of the termination. See
        `OptimizeResult` for a description of other attributes.

    See Also
    --------
    minimize : Interface to minimization algorithms for scalar multivariate
        functions
    show_options : Additional options accepted by the solvers

    Notes
    -----
    This section describes the available solvers that can be selected by the
    'method' parameter. The default method is the ``"Bounded"`` Brent method if
    `bounds` are passed and unbounded ``"Brent"`` otherwise.

    Method :ref:`Brent <optimize.minimize_scalar-brent>` uses Brent's
    algorithm [1]_ to find a local minimum.  The algorithm uses inverse
    parabolic interpolation when possible to speed up convergence of
    the golden section method.

    Method :ref:`Golden <optimize.minimize_scalar-golden>` uses the
    golden section search technique [1]_. It uses analog of the bisection
    method to decrease the bracketed interval. It is usually
    preferable to use the *Brent* method.

    Method :ref:`Bounded <optimize.minimize_scalar-bounded>` can
    perform bounded minimization [2]_ [3]_. It uses the Brent method to find a
    local minimum in the interval x1 < xopt < x2.

    Note that the Brent and Golden methods do not guarantee success unless a
    valid ``bracket`` triple is provided. If a three-point bracket cannot be
    found, consider `scipy.optimize.minimize`. Also, all methods are intended
    only for local minimization. When the function of interest has more than
    one local minimum, consider :ref:`global_optimization`.

    **Custom minimizers**

    It may be useful to pass a custom minimization method, for example
    when using some library frontend to minimize_scalar. You can simply
    pass a callable as the ``method`` parameter.

    The callable is called as ``method(fun, args, **kwargs, **options)``
    where ``kwargs`` corresponds to any other parameters passed to `minimize`
    (such as `bracket`, `tol`, etc.), except the `options` dict, which has
    its contents also passed as `method` parameters pair by pair.  The method
    shall return an `OptimizeResult` object.

    The provided `method` callable must be able to accept (and possibly ignore)
    arbitrary parameters; the set of parameters accepted by `minimize` may
    expand in future versions and then these parameters will be passed to
    the method. You can find an example in the scipy.optimize tutorial.

    .. versionadded:: 0.11.0

    References
    ----------
    .. [1] Press, W., S.A. Teukolsky, W.T. Vetterling, and B.P. Flannery.
           Numerical Recipes in C. Cambridge University Press.
    .. [2] Forsythe, G.E., M. A. Malcolm, and C. B. Moler. "Computer Methods
           for Mathematical Computations." Prentice-Hall Series in Automatic
           Computation 259 (1977).
    .. [3] Brent, Richard P. Algorithms for Minimization Without Derivatives.
           Courier Corporation, 2013.

    Examples
    --------
    Consider the problem of minimizing the following function.

    >>> def f(x):
    ...     return (x - 2) * x * (x + 2)**2

    Using the *Brent* method, we find the local minimum as:

    >>> from scipy.optimize import minimize_scalar
    >>> res = minimize_scalar(f)
    >>> res.fun
    -9.9149495908

    The minimizer is:

    >>> res.x
    1.28077640403

    Using the *Bounded* method, we find a local minimum with specified
    bounds as:

    >>> res = minimize_scalar(f, bounds=(-3, -1), method='bounded')
    >>> res.fun  # minimum
    3.28365179850e-13
    >>> res.x  # minimizer
    -2.0000002026

    """
    if not isinstance(args, tuple):
        args = (args,)

    if callable(method):
        meth = "_custom"
    elif method is None:
        meth = 'brent' if bounds is None else 'bounded'
    else:
        meth = method.lower()
    if options is None:
        options = {}

    if bounds is not None and meth in {'brent', 'golden'}:
        message = f"Use of `bounds` is incompatible with 'method={method}'."
        raise ValueError(message)

    if tol is not None:
        options = dict(options)
        if meth == 'bounded' and 'xatol' not in options:
            warn("Method 'bounded' does not support relative tolerance in x; "
                 "defaulting to absolute tolerance.",
                 RuntimeWarning, stacklevel=2)
            options['xatol'] = tol
        elif meth == '_custom':
            options.setdefault('tol', tol)
        else:
            options.setdefault('xtol', tol)

    # replace boolean "disp" option, if specified, by an integer value.
    disp = options.get('disp')
    if isinstance(disp, bool):
        options['disp'] = 2 * int(disp)

    if meth == '_custom':
        res = method(fun, args=args, bracket=bracket, bounds=bounds, **options)
    elif meth == 'brent':
        res = _recover_from_bracket_error(_minimize_scalar_brent,
                                          fun, bracket, args, **options)
    elif meth == 'bounded':
        if bounds is None:
            raise ValueError('The `bounds` parameter is mandatory for '
                             'method `bounded`.')
        res = _minimize_scalar_bounded(fun, bounds, args, **options)
    elif meth == 'golden':
        res = _recover_from_bracket_error(_minimize_scalar_golden,
                                          fun, bracket, args, **options)
    else:
        raise ValueError(f'Unknown solver {method}')

    # gh-16196 reported inconsistencies in the output shape of `res.x`. While
    # fixing this, future-proof it for when the function is vectorized:
    # the shape of `res.x` should match that of `res.fun`.
    res.fun = np.asarray(res.fun)[()]
    res.x = np.reshape(res.x, res.fun.shape)[()]
    return res

