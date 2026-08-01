
def fminbound(func, x1, x2, args=(), xtol=1e-5, maxfun=500,
              full_output=0, disp=1):
    """Bounded minimization for scalar functions.

    Parameters
    ----------
    func : callable f(x,*args)
        Objective function to be minimized (must accept and return scalars).
    x1, x2 : float or array scalar
        Finite optimization bounds.
    args : tuple, optional
        Extra arguments passed to function.
    xtol : float, optional
        The convergence tolerance.
    maxfun : int, optional
        Maximum number of function evaluations allowed.
    full_output : bool, optional
        If True, return optional outputs.
    disp : int, optional
        If non-zero, print messages.

        ``0`` : no message printing.

        ``1`` : non-convergence notification messages only.

        ``2`` : print a message on convergence too.

        ``3`` : print iteration results.

    Returns
    -------
    xopt : ndarray
        Parameters (over given interval) which minimize the
        objective function.
    fval : number
        (Optional output) The function value evaluated at the minimizer.
    ierr : int
        (Optional output) An error flag (0 if converged, 1 if maximum number of
        function calls reached).
    numfunc : int
        (Optional output) The number of function calls made.

    See Also
    --------
    minimize_scalar: Interface to minimization algorithms for scalar
        univariate functions. See the 'Bounded' `method` in particular.

    Notes
    -----
    Finds a local minimizer of the scalar function `func` in the
    interval x1 < xopt < x2 using Brent's method. (See `brent`
    for auto-bracketing.)

    References
    ----------
    .. [1] Forsythe, G.E., M. A. Malcolm, and C. B. Moler. "Computer Methods
           for Mathematical Computations." Prentice-Hall Series in Automatic
           Computation 259 (1977).
    .. [2] Brent, Richard P. Algorithms for Minimization Without Derivatives.
           Courier Corporation, 2013.

    Examples
    --------
    `fminbound` finds the minimizer of the function in the given range.
    The following examples illustrate this.

    >>> from scipy import optimize
    >>> def f(x):
    ...     return (x-1)**2
    >>> minimizer = optimize.fminbound(f, -4, 4)
    >>> minimizer
    1.0
    >>> minimum = f(minimizer)
    >>> minimum
    0.0
    >>> res = optimize.fminbound(f, 3, 4, full_output=True)
    >>> minimizer, fval, ierr, numfunc = res
    >>> minimizer
    3.000005960860986
    >>> minimum = f(minimizer)
    >>> minimum, fval
    (4.000023843479476, 4.000023843479476)
    """
    options = {'xatol': xtol,
               'maxiter': maxfun,
               'disp': disp}

    res = _minimize_scalar_bounded(func, (x1, x2), args, **options)
    if full_output:
        return res['x'], res['fun'], res['status'], res['nfev']
    else:
        return res['x']

