
def trf(fun, jac, x0, f0, J0, lb, ub, ftol, xtol, gtol, max_nfev, x_scale,
        loss_function, tr_solver, tr_options, verbose, callback=None):
    # For efficiency, it makes sense to run the simplified version of the
    # algorithm when no bounds are imposed. We decided to write the two
    # separate functions. It violates the DRY principle, but the individual
    # functions are kept the most readable.
    if np.all(lb == -np.inf) and np.all(ub == np.inf):
        return trf_no_bounds(
            fun, jac, x0, f0, J0, ftol, xtol, gtol, max_nfev, x_scale,
            loss_function, tr_solver, tr_options, verbose, callback=callback)
    else:
        return trf_bounds(
            fun, jac, x0, f0, J0, lb, ub, ftol, xtol, gtol, max_nfev, x_scale,
            loss_function, tr_solver, tr_options, verbose, callback=callback)

