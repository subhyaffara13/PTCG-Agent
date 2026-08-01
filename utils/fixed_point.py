
def fixed_point(func, x0, args=(), xtol=1e-8, maxiter=500, method='del2'):
    """
    Find a fixed point of the function.

    Given a function of one or more variables and a starting point, find a
    fixed point of the function: i.e., where ``func(xf) == xf``.

    Parameters
    ----------
    func : function
        Function to evaluate.
    x0 : array_like
        Guess of fixed point of function.
    args : tuple, optional
        Extra arguments to `func`.
    xtol : float, optional
        Convergence tolerance, defaults to 1e-08.
    maxiter : int, optional
        Maximum number of iterations, defaults to 500.
    method : {"del2", "iteration"}, optional
        Method of finding the fixed-point, defaults to "del2",
        which uses Steffensen's Method with Aitken's ``Del^2``
        convergence acceleration [1]_. The "iteration" method simply iterates
        the function until convergence is detected, without attempting to
        accelerate the convergence.

    Returns
    -------
    xf : array
        Fixed point of function.

    References
    ----------
    .. [1] Burden, Faires, "Numerical Analysis", 5th edition, pg. 80

    Examples
    --------
    >>> import numpy as np
    >>> from scipy import optimize
    >>> def func(x, c1, c2):
    ...    return np.sqrt(c1/(x+c2))
    >>> c1 = np.array([10,12.])
    >>> c2 = np.array([3, 5.])
    >>> optimize.fixed_point(func, [1.2, 1.3], args=(c1,c2))
    array([ 1.4920333 ,  1.37228132])

    """
    use_accel = {'del2': True, 'iteration': False}[method]
    x0 = _asarray_validated(x0, as_inexact=True)
    return _fixed_point_helper(func, x0, args, xtol, maxiter, use_accel)

