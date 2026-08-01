
def approx_fprime(xk, f, epsilon=_epsilon, *args):
    """Finite difference approximation of the derivatives of a
    scalar or vector-valued function.

    If a function maps from :math:`R^n` to :math:`R^m`, its derivatives form
    an m-by-n matrix
    called the Jacobian, where an element :math:`(i, j)` is a partial
    derivative of f[i] with respect to ``xk[j]``.

    Parameters
    ----------
    xk : array_like
        The coordinate vector at which to determine the gradient of `f`.
    f : callable
        Function of which to estimate the derivatives of. Has the signature
        ``f(xk, *args)`` where `xk` is the argument in the form of a 1-D array
        and `args` is a tuple of any additional fixed parameters needed to
        completely specify the function. The argument `xk` passed to this
        function is an ndarray of shape (n,) (never a scalar even if n=1).
        It must return a 1-D array_like of shape (m,) or a scalar.

        Suppose the callable has signature ``f0(x, *my_args, **my_kwargs)``, where
        ``my_args`` and ``my_kwargs`` are required positional and keyword arguments.
        Rather than passing ``f0`` as the callable, wrap it to accept
        only ``x``; e.g., pass ``fun=lambda x: f0(x, *my_args, **my_kwargs)`` as the
        callable, where ``my_args`` (tuple) and ``my_kwargs`` (dict) have been
        gathered before invoking this function.

        .. versionchanged:: 1.9.0
            `f` is now able to return a 1-D array-like, with the :math:`(m, n)`
            Jacobian being estimated.

    epsilon : {float, array_like}, optional
        Increment to `xk` to use for determining the function gradient.
        If a scalar, uses the same finite difference delta for all partial
        derivatives. If an array, should contain one value per element of
        `xk`. Defaults to ``sqrt(np.finfo(float).eps)``, which is approximately
        1.49e-08.
    \\*args : args, optional
        Any other arguments that are to be passed to `f`.

    Returns
    -------
    jac : ndarray
        The partial derivatives of `f` to `xk`.

    See Also
    --------
    check_grad : Check correctness of gradient function against approx_fprime.

    Notes
    -----
    The function gradient is determined by the forward finite difference
    formula::

                 f(xk[i] + epsilon[i]) - f(xk[i])
        f'[i] = ---------------------------------
                            epsilon[i]

    Examples
    --------
    >>> import numpy as np
    >>> from scipy import optimize
    >>> def func(x, c0, c1):
    ...     "Coordinate vector `x` should be an array of size two."
    ...     return c0 * x[0]**2 + c1*x[1]**2

    >>> x = np.ones(2)
    >>> c0, c1 = (1, 200)
    >>> eps = np.sqrt(np.finfo(float).eps)
    >>> optimize.approx_fprime(x, func, [eps, np.sqrt(200) * eps], c0, c1)
    array([   2.        ,  400.00004208])

    """
    xk = np.asarray(xk, float)
    f0 = f(xk, *args)

    return approx_derivative(f, xk, method='2-point', abs_step=epsilon,
                             args=args, f0=f0)

