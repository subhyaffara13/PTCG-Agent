
def golden(func, args=(), brack=None, tol=_epsilon,
           full_output=0, maxiter=5000):
    """
    Return the minimizer of a function of one variable using the golden section
    method.

    Given a function of one variable and a possible bracketing interval,
    return a minimizer of the function isolated to a fractional precision of
    tol.

    Parameters
    ----------
    func : callable func(x,*args)
        Objective function to minimize.
    args : tuple, optional
        Additional arguments (if present), passed to func.
    brack : tuple, optional
        Either a triple ``(xa, xb, xc)`` where ``xa < xb < xc`` and
        ``func(xb) < func(xa) and  func(xb) < func(xc)``, or a pair (xa, xb)
        to be used as initial points for a downhill bracket search (see
        `scipy.optimize.bracket`).
        The minimizer ``x`` will not necessarily satisfy ``xa <= x <= xb``.
    tol : float, optional
        x tolerance stop criterion
    full_output : bool, optional
        If True, return optional outputs.
    maxiter : int
        Maximum number of iterations to perform.

    Returns
    -------
    xmin : ndarray
        Optimum point.
    fval : float
        (Optional output) Optimum function value.
    funcalls : int
        (Optional output) Number of objective function evaluations made.

    See Also
    --------
    minimize_scalar: Interface to minimization algorithms for scalar
        univariate functions. See the 'Golden' `method` in particular.

    Notes
    -----
    Uses analog of bisection method to decrease the bracketed
    interval.

    Examples
    --------
    We illustrate the behaviour of the function when `brack` is of
    size 2 and 3, respectively. In the case where `brack` is of the
    form (xa,xb), we can see for the given values, the output need
    not necessarily lie in the range ``(xa, xb)``.

    >>> def f(x):
    ...     return (x-1)**2

    >>> from scipy import optimize

    >>> minimizer = optimize.golden(f, brack=(1, 2))
    >>> minimizer
    1
    >>> res = optimize.golden(f, brack=(-1, 0.5, 2), full_output=True)
    >>> xmin, fval, funcalls = res
    >>> f(xmin), fval
    (9.925165290385052e-18, 9.925165290385052e-18)

    """
    options = {'xtol': tol, 'maxiter': maxiter}
    res = _minimize_scalar_golden(func, brack, args, **options)
    if full_output:
        return res['x'], res['fun'], res['nfev']
    else:
        return res['x']

