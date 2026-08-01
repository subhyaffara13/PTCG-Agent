
def call_minpack(fun, x0, jac, ftol, xtol, gtol, max_nfev, x_scale, jac_method=None):
    n = x0.size

    # Compute MINPACK's `diag`, which is inverse of our `x_scale` and
    # ``x_scale='jac'`` corresponds to ``diag=None``.

    # 1.16.0 - default x_scale changed to 'jac', with diag=None
    if x_scale is None or (isinstance(x_scale, str) and x_scale == 'jac'):
        diag = None
    else:
        # x_scale specified, so use that
        diag = 1 / x_scale

    full_output = True
    col_deriv = False
    factor = 100.0

    if max_nfev is None:
        max_nfev = 100 * n

    # lmder is typically used for systems with analytic jacobians, with lmdif being
    # used if there is only an objective fun (lmdif uses finite differences to estimate
    # jacobian). Otherwise they're very similar internally.
    # We now do all the finite differencing in VectorFunction, which means we can drop
    # lmdif and just use lmder.

    # for sending a copy of x0 into _lmder
    xp = array_namespace(x0)

    x, info, status = _minpack._lmder(
        fun, jac, xp.astype(x0, x0.dtype), (), full_output, col_deriv,
        ftol, xtol, gtol, max_nfev, factor, diag)

    f = info['fvec']
    J = jac(x)

    cost = 0.5 * np.dot(f, f)
    g = J.T.dot(f)
    g_norm = norm(g, ord=np.inf)

    nfev = info['nfev']
    if callable(jac_method):
        # user supplied a callable ("analytic") jac
        njev = info.get('njev', None)
    else:
        # If there are no analytic jacobian evaluations we need to set `njev=None`.
        njev = None

    status = FROM_MINPACK_TO_COMMON[status]
    active_mask = np.zeros_like(x0, dtype=int)

    return OptimizeResult(
        x=x, cost=cost, fun=f, jac=J, grad=g, optimality=g_norm,
        active_mask=active_mask, nfev=nfev, njev=njev, status=status)

