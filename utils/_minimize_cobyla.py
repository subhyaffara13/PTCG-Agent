
def _minimize_cobyla(fun, x0, args=(), constraints=(),
                     rhobeg=1.0, tol=1e-4, maxiter=1000,
                     disp=0, catol=None, f_target=-np.inf,
                     callback=None, bounds=None, **unknown_options):
    """
    Minimize a scalar function of one or more variables using the
    Constrained Optimization BY Linear Approximation (COBYLA) algorithm.
    This method uses the pure-python implementation of the algorithm from PRIMA.

    Options
    -------
    rhobeg : float
        Reasonable initial changes to the variables.
    tol : float
        Final accuracy in the optimization (not precisely guaranteed).
        This is a lower bound on the size of the trust region.
    disp : int
        Controls the frequency of output:
            0. (default) There will be no printing
            1. A message will be printed to the screen at the end of iteration, showing
               the best vector of variables found and its objective function value
            2. in addition to 1, each new value of RHO is printed to the screen,
               with the best vector of variables so far and its objective function
               value.
            3. in addition to 2, each function evaluation with its variables will
               be printed to the screen.
    maxiter : int
        Maximum number of function evaluations.
    catol : float
        Tolerance (absolute) for constraint violations
    f_target : float
        Stop if the objective function is less than `f_target`.

        .. versionchanged:: 1.16.0
            The original Powell implementation was replaced by a pure
            Python version from the PRIMA package, with bug fixes and
            improvements being made.


    References
    ----------
    Zhang Z. (2023), "PRIMA: Reference Implementation for Powell's Methods with
    Modernization and Amelioration", https://www.libprima.net,
    :doi:`10.5281/zenodo.8052654`
    """
    from .._external.pyprima import minimize
    from .._external.pyprima.common.infos import SMALL_TR_RADIUS, FTARGET_ACHIEVED
    from .._external.pyprima.common.message import get_info_string
    _check_unknown_options(unknown_options)
    rhoend = tol
    iprint = disp if disp is not None else 0
    if iprint != 0 and iprint != 1 and iprint != 2 and iprint != 3:
        raise ValueError(f'disp argument to minimize must be 0, 1, 2, or 3,\
                          received {iprint}')

    # create the ScalarFunction, cobyla doesn't require derivative function
    def _jac(x, *args):
        return None

    sf = _prepare_scalar_function(fun, x0, args=args, jac=_jac)

    if callback is not None:
        sig = wrapped_inspect_signature(callback)
        if set(sig.parameters) == {"intermediate_result"}:
            def wrapped_callback_intermediate(x, f, nf, tr, cstrv, nlconstrlist):
                intermediate_result = OptimizeResult(x=np.copy(x), fun=f, nfev=nf,
                                                     nit=tr, maxcv=cstrv)
                callback(intermediate_result=intermediate_result)
        else:
            def wrapped_callback_intermediate(x, f, nf, tr, cstrv, nlconstrlist):
                callback(np.copy(x))
        def wrapped_callback(x, f, nf, tr, cstrv, nlconstrlist):
            try:
                wrapped_callback_intermediate(x, f, nf, tr, cstrv, nlconstrlist)
                return False
            except StopIteration:
                return True
    else:
        wrapped_callback = None


    ctol = catol if catol is not None else np.sqrt(np.finfo(float).eps)
    options = {
        'rhobeg': rhobeg,
        'rhoend': rhoend,
        'maxfev': maxiter,
        'iprint': iprint,
        'ctol': ctol,
        'ftarget': f_target,
    }

    result = minimize(sf.fun, x0, method='cobyla', bounds=bounds,
                      constraints=constraints, callback=wrapped_callback,
                      options=options)


    if result.cstrv > ctol:
        success = False
        message = ('Did not converge to a solution satisfying the constraints. See '
                  '`maxcv` for the magnitude of the violation.')
    else:
        success = result.info == SMALL_TR_RADIUS or result.info == FTARGET_ACHIEVED
        message = get_info_string('COBYLA', result.info)

    return OptimizeResult(x=result.x,
                          status=result.info,
                          success=success,
                          message=message,
                          nfev=result.nf,
                          fun=result.f,
                          maxcv=result.cstrv)

