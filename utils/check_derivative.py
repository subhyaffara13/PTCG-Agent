
def check_derivative(fun, jac, x0, bounds=(-np.inf, np.inf), args=(),
                     kwargs=None):
    """Check correctness of a function computing derivatives (Jacobian or
    gradient) by comparison with a finite difference approximation.

    Parameters
    ----------
    fun : callable
        Function of which to estimate the derivatives. The argument x
        passed to this function is ndarray of shape (n,) (never a scalar
        even if n=1). It must return 1-D array_like of shape (m,) or a scalar.
    jac : callable
        Function which computes Jacobian matrix of `fun`. It must work with
        argument x the same way as `fun`. The return value must be array_like
        or sparse array with an appropriate shape.
    x0 : array_like of shape (n,) or float
        Point at which to estimate the derivatives. Float will be converted
        to 1-D array.
    bounds : 2-tuple of array_like, optional
        Lower and upper bounds on independent variables. Defaults to no bounds.
        Each bound must match the size of `x0` or be a scalar, in the latter
        case the bound will be the same for all variables. Use it to limit the
        range of function evaluation.
    args, kwargs : tuple and dict, optional
        Additional arguments passed to `fun` and `jac`. Both empty by default.
        The calling signature is ``fun(x, *args, **kwargs)`` and the same
        for `jac`.

    Returns
    -------
    accuracy : float
        The maximum among all relative errors for elements with absolute values
        higher than 1 and absolute errors for elements with absolute values
        less or equal than 1. If `accuracy` is on the order of 1e-6 or lower,
        then it is likely that your `jac` implementation is correct.

    See Also
    --------
    approx_derivative : Compute finite difference approximation of derivative.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.optimize._numdiff import check_derivative
    >>>
    >>>
    >>> def f(x, c1, c2):
    ...     return np.array([x[0] * np.sin(c1 * x[1]),
    ...                      x[0] * np.cos(c2 * x[1])])
    ...
    >>> def jac(x, c1, c2):
    ...     return np.array([
    ...         [np.sin(c1 * x[1]),  c1 * x[0] * np.cos(c1 * x[1])],
    ...         [np.cos(c2 * x[1]), -c2 * x[0] * np.sin(c2 * x[1])]
    ...     ])
    ...
    >>>
    >>> x0 = np.array([1.0, 0.5 * np.pi])
    >>> check_derivative(f, jac, x0, args=(1, 2))
    2.4492935982947064e-16
    """
    if kwargs is None:
        kwargs = {}
    J_to_test = jac(x0, *args, **kwargs)
    if issparse(J_to_test):
        J_diff = approx_derivative(fun, x0, bounds=bounds, sparsity=J_to_test,
                                   args=args, kwargs=kwargs)
        J_to_test = csr_array(J_to_test)
        abs_err = J_to_test - J_diff
        i, j, abs_err_data = find(abs_err)
        J_diff_data = np.asarray(J_diff[i, j]).ravel()
        return np.max(np.abs(abs_err_data) /
                      np.maximum(1, np.abs(J_diff_data)))
    else:
        J_diff = approx_derivative(fun, x0, bounds=bounds,
                                   args=args, kwargs=kwargs)
        abs_err = np.abs(J_to_test - J_diff)
        return np.max(abs_err / np.maximum(1, np.abs(J_diff)))

