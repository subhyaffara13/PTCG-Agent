
def _remove_from_bounds(bounds, i_fixed):
    """Removes fixed variables from a `Bounds` instance"""
    lb = bounds.lb[~i_fixed]
    ub = bounds.ub[~i_fixed]
    return Bounds(lb, ub)  # don't mutate original Bounds object

