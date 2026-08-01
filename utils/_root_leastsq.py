
def _root_leastsq(fun, x0, args=(), jac=None,
                  col_deriv=0, xtol=1.49012e-08, ftol=1.49012e-08,
                  gtol=0.0, maxiter=0, eps=0.0, factor=100, diag=None,
                  **unknown_options):
    """
    Solve for least squares with Levenberg-Marquardt

    Options
    -------
    col_deriv : bool
        non-zero to specify that the Jacobian function computes derivatives
        down the columns (faster, because there is no transpose operation).
    ftol : float
        Relative error desired in the sum of squares.
    xtol : float
        Relative error desired in the approximate solution.
    gtol : float
        Orthogonality desired between the function vector and the columns
        of the Jacobian.
    maxiter : int
        The maximum number of calls to the function. If zero, then
        100*(N+1) is the maximum where N is the number of elements in x0.
    eps : float
        A suitable step length for the forward-difference approximation of
        the Jacobian (for Dfun=None). If `eps` is less than the machine
        precision, it is assumed that the relative errors in the functions
        are of the order of the machine precision.
    factor : float
        A parameter determining the initial step bound
        (``factor * || diag * x||``). Should be in interval ``(0.1, 100)``.
    diag : sequence
        N positive entries that serve as a scale factors for the variables.
    """
    nfev = 0
    def _wrapped_fun(*fargs):
        """
        Wrapped `func` to track the number of times
        the function has been called.
        """
        nonlocal nfev
        nfev += 1
        return fun(*fargs)

    _check_unknown_options(unknown_options)
    x, cov_x, info, msg, ier = leastsq(_wrapped_fun, x0, args=args,
                                       Dfun=jac, full_output=True,
                                       col_deriv=col_deriv, xtol=xtol,
                                       ftol=ftol, gtol=gtol,
                                       maxfev=maxiter, epsfcn=eps,
                                       factor=factor, diag=diag)
    sol = OptimizeResult(x=x, message=msg, status=ier,
                         success=ier in (1, 2, 3, 4), cov_x=cov_x,
                         fun=info.pop('fvec'), method="lm")
    sol.update(info)
    sol.nfev = nfev
    return sol

