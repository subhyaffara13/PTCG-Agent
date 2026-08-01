
def standardize_bounds(bounds, x0, meth):
    """Converts bounds to the form required by the solver."""
    if meth in {'trust-constr', 'powell', 'nelder-mead', 'cobyla', 'cobyqa',
                'new'}:
        if not isinstance(bounds, Bounds):
            lb, ub = old_bound_to_new(bounds)
            bounds = Bounds(lb, ub)
    elif meth in ('l-bfgs-b', 'tnc', 'slsqp', 'old'):
        if isinstance(bounds, Bounds):
            bounds = new_bounds_to_old(bounds.lb, bounds.ub, x0.shape[0])
    return bounds

