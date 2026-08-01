
def _minimize_scalar_brent(func, brack=None, args=(), xtol=1.48e-8,
                           maxiter=500, disp=0,
                           **unknown_options):
    """
    Options
    -------
    maxiter : int
        Maximum number of iterations to perform.
    xtol : float
        Relative error in solution `xopt` acceptable for convergence.
    disp : int, optional
        If non-zero, print messages.

        ``0`` : no message printing.

        ``1`` : non-convergence notification messages only.

        ``2`` : print a message on convergence too.

        ``3`` : print iteration results.

    Notes
    -----
    Uses inverse parabolic interpolation when possible to speed up
    convergence of golden section method.

    """
    _check_unknown_options(unknown_options)
    tol = xtol
    if tol < 0:
        raise ValueError(f'tolerance should be >= 0, got {tol!r}')

    brent = Brent(func=func, args=args, tol=tol,
                  full_output=True, maxiter=maxiter, disp=disp)
    brent.set_bracket(brack)
    brent.optimize()
    x, fval, nit, nfev = brent.get_result(full_output=True)

    success = nit < maxiter and not (np.isnan(x) or np.isnan(fval))

    if success:
        message = ("\nOptimization terminated successfully;\n"
                   "The returned value satisfies the termination criteria\n"
                   f"(using xtol = {xtol} )")
    else:
        if nit >= maxiter:
            message = "\nMaximum number of iterations exceeded"
        if np.isnan(x) or np.isnan(fval):
            message = f"{_status_message['nan']}"

    if disp:
        _print_success_message_or_warn(not success, message)

    return OptimizeResult(fun=fval, x=x, nit=nit, nfev=nfev,
                          success=success, message=message)

