
def _minimize_scalar_golden(func, brack=None, args=(),
                            xtol=_epsilon, maxiter=5000, disp=0,
                            **unknown_options):
    """
    Options
    -------
    xtol : float
        Relative error in solution `xopt` acceptable for convergence.
    maxiter : int
        Maximum number of iterations to perform.
    disp: int, optional
        If non-zero, print messages.

        ``0`` : no message printing.

        ``1`` : non-convergence notification messages only.

        ``2`` : print a message on convergence too.

        ``3`` : print iteration results.
    """
    _check_unknown_options(unknown_options)
    tol = xtol
    if brack is None:
        xa, xb, xc, fa, fb, fc, funcalls = bracket(func, args=args)
    elif len(brack) == 2:
        xa, xb, xc, fa, fb, fc, funcalls = bracket(func, xa=brack[0],
                                                   xb=brack[1], args=args)
    elif len(brack) == 3:
        xa, xb, xc = brack
        if (xa > xc):  # swap so xa < xc can be assumed
            xc, xa = xa, xc
        if not ((xa < xb) and (xb < xc)):
            raise ValueError(
                "Bracketing values (xa, xb, xc) do not"
                " fulfill this requirement: (xa < xb) and (xb < xc)"
            )
        fa = func(*((xa,) + args))
        fb = func(*((xb,) + args))
        fc = func(*((xc,) + args))
        if not ((fb < fa) and (fb < fc)):
            raise ValueError(
                "Bracketing values (xa, xb, xc) do not fulfill"
                " this requirement: (f(xb) < f(xa)) and (f(xb) < f(xc))"
            )
        funcalls = 3
    else:
        raise ValueError("Bracketing interval must be length 2 or 3 sequence.")

    _gR = 0.61803399  # golden ratio conjugate: 2.0/(1.0+sqrt(5.0))
    _gC = 1.0 - _gR
    x3 = xc
    x0 = xa
    if (np.abs(xc - xb) > np.abs(xb - xa)):
        x1 = xb
        x2 = xb + _gC * (xc - xb)
    else:
        x2 = xb
        x1 = xb - _gC * (xb - xa)
    f1 = func(*((x1,) + args))
    f2 = func(*((x2,) + args))
    funcalls += 2
    nit = 0

    if disp > 2:
        print(" ")
        print(f"{'Func-count':^12} {'x':^12} {'f(x)': ^12}")

    for i in range(maxiter):
        if np.abs(x3 - x0) <= tol * (np.abs(x1) + np.abs(x2)):
            break
        if (f2 < f1):
            x0 = x1
            x1 = x2
            x2 = _gR * x1 + _gC * x3
            f1 = f2
            f2 = func(*((x2,) + args))
        else:
            x3 = x2
            x2 = x1
            x1 = _gR * x2 + _gC * x0
            f2 = f1
            f1 = func(*((x1,) + args))
        funcalls += 1
        if disp > 2:
            if (f1 < f2):
                xmin, fval = x1, f1
            else:
                xmin, fval = x2, f2
            print(f"{funcalls:^12g} {xmin:^12.6g} {fval:^12.6g}")

        nit += 1
    # end of iteration loop

    if (f1 < f2):
        xmin = x1
        fval = f1
    else:
        xmin = x2
        fval = f2

    success = nit < maxiter and not (np.isnan(fval) or np.isnan(xmin))

    if success:
        message = ("\nOptimization terminated successfully;\n"
                   "The returned value satisfies the termination criteria\n"
                   f"(using xtol = {xtol} )")
    else:
        if nit >= maxiter:
            message = "\nMaximum number of iterations exceeded"
        if np.isnan(xmin) or np.isnan(fval):
            message = f"{_status_message['nan']}"

    if disp:
        _print_success_message_or_warn(not success, message)

    return OptimizeResult(fun=fval, nfev=funcalls, x=xmin, nit=nit,
                          success=success, message=message)

