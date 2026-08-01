
def _minimize_trust_region(fun, x0, args=(), jac=None, hess=None, hessp=None,
                           subproblem=None, initial_trust_radius=1.0,
                           max_trust_radius=1000.0, eta=0.15, gtol=1e-4,
                           maxiter=None, disp=False, return_all=False,
                           callback=None, inexact=True, workers=None,
                           subproblem_maxiter=None, **unknown_options):
    """
    Minimization of scalar function of one or more variables using a
    trust-region algorithm.

    Options for the trust-region algorithm are:
        initial_trust_radius : float
            Initial trust radius.
        max_trust_radius : float
            Never propose steps that are longer than this value.
        eta : float
            Trust region related acceptance stringency for proposed steps.
        gtol : float
            Gradient norm must be less than `gtol`
            before successful termination.
        maxiter : int
            Maximum number of iterations to perform.
        disp : bool
            If True, print convergence message.
        inexact : bool
            Accuracy to solve subproblems. If True requires less nonlinear
            iterations, but more vector products. Only effective for method
            trust-krylov.
        workers : int, map-like callable, optional
            A map-like callable, such as `multiprocessing.Pool.map` for evaluating
            any numerical differentiation in parallel.
            This evaluation is carried out as ``workers(fun, iterable)``.
            Only for 'trust-krylov', 'trust-ncg'.

            .. versionadded:: 1.16.0
        subproblem_maxiter : int, optional
            Maximum number of iterations to perform per subproblem. Only affects
            trust-exact. Default is 25.

            .. versionadded:: 1.17.0


    This function is called by the `minimize` function.
    It is not supposed to be called directly.
    """
    _check_unknown_options(unknown_options)

    if jac is None:
        raise ValueError('Jacobian is currently required for trust-region '
                         'methods')
    if hess is None and hessp is None:
        raise ValueError('Either the Hessian or the Hessian-vector product '
                         'is currently required for trust-region methods')
    if subproblem is None:
        raise ValueError('A subproblem solving strategy is required for '
                         'trust-region methods')
    if not (0 <= eta < 0.25):
        raise Exception('invalid acceptance stringency')
    if max_trust_radius <= 0:
        raise Exception('the max trust radius must be positive')
    if initial_trust_radius <= 0:
        raise ValueError('the initial trust radius must be positive')
    if initial_trust_radius >= max_trust_radius:
        raise ValueError('the initial trust radius must be less than the '
                         'max trust radius')

    # force the initial guess into a nice format
    x0 = np.asarray(x0).flatten()

    # A ScalarFunction representing the problem. This caches calls to fun, jac,
    # hess.
    # the workers kwd only has an effect for trust-ncg, trust-krylov when
    # estimating the Hessian with finite-differences. It's never used
    # during calculation of jacobian, because callables are required for all
    # methods.
    sf = _prepare_scalar_function(
        fun, x0, jac=jac, hess=hess, args=args, workers=workers
    )
    fun = sf.fun
    jac = sf.grad
    if callable(hess):
        hess = sf.hess
    elif callable(hessp):
        # this elif statement must come before examining whether hess
        # is estimated by FD methods or a HessianUpdateStrategy
        pass
    elif (hess in FD_METHODS or isinstance(hess, HessianUpdateStrategy)):
        # If the Hessian is being estimated by finite differences or a
        # Hessian update strategy then ScalarFunction.hess returns a
        # LinearOperator or a HessianUpdateStrategy. This enables the
        # calculation/creation of a hessp. BUT you only want to do this
        # if the user *hasn't* provided a callable(hessp) function.
        hess = None

        def hessp(x, p, *args):
            return sf.hess(x).dot(p)
    else:
        raise ValueError('Either the Hessian or the Hessian-vector product '
                         'is currently required for trust-region methods')

    # ScalarFunction doesn't represent hessp
    nhessp, hessp = _wrap_function(hessp, args)

    # limit the number of iterations
    if maxiter is None:
        maxiter = len(x0)*200

    # init the search status
    warnflag = 0

    # initialize the search
    trust_radius = initial_trust_radius
    x = x0
    if return_all:
        allvecs = [x]

    subproblem_init_kw = {}
    if hasattr(subproblem, 'MAXITER_DEFAULT'):
        subproblem_init_kw['maxiter'] = subproblem_maxiter

    m = subproblem(x, fun, jac, hess, hessp, **subproblem_init_kw)
    k = 0

    # search for the function min
    # do not even start if the gradient is small enough
    while m.jac_mag >= gtol:

        # Solve the sub-problem.
        # This gives us the proposed step relative to the current position
        # and it tells us whether the proposed step
        # has reached the trust region boundary or not.
        try:
            p, hits_boundary = m.solve(trust_radius)
        except np.linalg.LinAlgError:
            warnflag = 3
            break

        # calculate the predicted value at the proposed point
        predicted_value = m(p)

        # define the local approximation at the proposed point
        x_proposed = x + p
        m_proposed = subproblem(x_proposed, fun, jac, hess, hessp, **subproblem_init_kw)

        # evaluate the ratio defined in equation (4.4)
        actual_reduction = m.fun - m_proposed.fun
        predicted_reduction = m.fun - predicted_value
        if predicted_reduction <= 0:
            warnflag = 2
            break
        rho = actual_reduction / predicted_reduction

        # update the trust radius according to the actual/predicted ratio
        if rho < 0.25:
            trust_radius *= 0.25
        elif rho > 0.75 and hits_boundary:
            trust_radius = min(2*trust_radius, max_trust_radius)

        # if the ratio is high enough then accept the proposed step
        if rho > eta:
            x = x_proposed
            m = m_proposed

        # append the best guess, call back, increment the iteration count
        if return_all:
            allvecs.append(np.copy(x))
        k += 1

        intermediate_result = OptimizeResult(x=x, fun=m.fun)
        if _call_callback_maybe_halt(callback, intermediate_result):
            break

        # check if the gradient is small enough to stop
        if m.jac_mag < gtol:
            warnflag = 0
            break

        # check if we have looked at enough iterations
        if k >= maxiter:
            warnflag = 1
            break

    # print some stuff if requested
    status_messages = (
            _status_message['success'],
            _status_message['maxiter'],
            'A bad approximation caused failure to predict improvement.',
            'A linalg error occurred, such as a non-psd Hessian.',
            )
    if disp:
        if warnflag == 0:
            print(status_messages[warnflag])
        else:
            warnings.warn(status_messages[warnflag], RuntimeWarning, stacklevel=3)
        print(f"         Current function value: {m.fun:f}")
        print(f"         Iterations: {k:d}")
        print(f"         Function evaluations: {sf.nfev:d}")
        print(f"         Gradient evaluations: {sf.ngev:d}")
        print(f"         Hessian evaluations: {sf.nhev + nhessp[0]:d}")

    result = OptimizeResult(x=x, success=(warnflag == 0), status=warnflag,
                            fun=m.fun, jac=m.jac, nfev=sf.nfev, njev=sf.ngev,
                            nhev=sf.nhev + nhessp[0], nit=k,
                            message=status_messages[warnflag])

    if hess is not None:
        result['hess'] = m.hess

    if return_all:
        result['allvecs'] = allvecs

    return result

