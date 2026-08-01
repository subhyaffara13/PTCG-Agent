
def check_grad(func, grad, x0, *args, epsilon=_epsilon, direction='all', rng=None):
    r"""Check the correctness of a gradient function by comparing it against a
    (forward) finite-difference approximation of the gradient.

    Parameters
    ----------
    func : callable ``func(x0, *args)``
        Function whose derivative is to be checked.
    grad : callable ``grad(x0, *args)``
        Jacobian of `func`.
    x0 : ndarray
        Points to check `grad` against forward difference approximation of grad
        using `func`.
    *args : optional
        Extra arguments passed to `func` and `grad`.
    epsilon : float, optional
        Step size used for the finite difference approximation. It defaults to
        ``sqrt(np.finfo(float).eps)``, which is approximately 1.49e-08.
    direction : str, optional
        If set to ``'random'``, then gradients along a random vector
        are used to check `grad` against forward difference approximation
        using `func`. By default it is ``'all'``, in which case, all
        the one hot direction vectors are considered to check `grad`.
        If `func` is a vector valued function then only ``'all'`` can be used.
    rng : `numpy.random.Generator`, optional
        Pseudorandom number generator state. When `rng` is None, a new
        `numpy.random.Generator` is created using entropy from the
        operating system. Types other than `numpy.random.Generator` are
        passed to `numpy.random.default_rng` to instantiate a ``Generator``.

        The random numbers generated affect the random vector along which gradients
        are computed to check ``grad``. Note that `rng` is only used when `direction`
        argument is set to `'random'`.

    Returns
    -------
    err : float
        The square root of the sum of squares (i.e., the 2-norm) of the
        difference between ``grad(x0, *args)`` and the finite difference
        approximation of `grad` using func at the points `x0`.

    See Also
    --------
    approx_fprime

    Examples
    --------
    >>> import numpy as np
    >>> def func(x):
    ...     return x[0]**2 - 0.5 * x[1]**3
    >>> def grad(x):
    ...     return [2 * x[0], -1.5 * x[1]**2]
    >>> from scipy.optimize import check_grad
    >>> check_grad(func, grad, [1.5, -1.5])
    2.9802322387695312e-08  # may vary
    >>> rng = np.random.default_rng()
    >>> check_grad(func, grad, [1.5, -1.5],
    ...             direction='random', seed=rng)
    2.9802322387695312e-08

    """
    step = epsilon
    x0 = np.asarray(x0)

    def g(w, func, x0, v, *args):
        return func(x0 + w*v, *args)

    if direction == 'random':
        _grad = np.asanyarray(grad(x0, *args))
        if _grad.ndim > 1:
            raise ValueError("'random' can only be used with scalar valued"
                             " func")
        rng_gen = check_random_state(rng)
        v = rng_gen.standard_normal(size=(x0.shape))
        _args = (func, x0, v) + args
        _func = g
        vars = np.zeros((1,))
        analytical_grad = np.dot(_grad, v)
    elif direction == 'all':
        _args = args
        _func = func
        vars = x0
        analytical_grad = grad(x0, *args)
    else:
        raise ValueError(f"{direction} is not a valid string for "
                         "``direction`` argument")

    return np.sqrt(np.sum(np.abs(
        (analytical_grad - approx_fprime(vars, _func, step, *_args))**2
    )))

