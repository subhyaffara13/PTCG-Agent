
def _get_bounds(bounds, n):
    """
    Uniformize the bounds.
    """
    if bounds is None:
        return Bounds(np.full(n, -np.inf), np.full(n, np.inf))
    elif isinstance(bounds, Bounds):
        if bounds.lb.shape != (n,) or bounds.ub.shape != (n,):
            raise ValueError(f"The bounds must have {n} elements.")
        return Bounds(bounds.lb, bounds.ub)
    elif hasattr(bounds, "__len__"):
        bounds = np.asarray(bounds)
        if bounds.shape != (n, 2):
            raise ValueError(
                "The shape of the bounds is not compatible with "
                "the number of variables."
            )
        return Bounds(bounds[:, 0], bounds[:, 1])
    else:
        raise TypeError(
            "The bounds must be an instance of "
            "scipy.optimize.Bounds or an array-like object."
        )

