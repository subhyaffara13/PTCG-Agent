
def prepare_bounds(bounds, n):
    lb, ub = (np.asarray(b, dtype=float) for b in bounds)
    if lb.ndim == 0:
        lb = np.resize(lb, n)

    if ub.ndim == 0:
        ub = np.resize(ub, n)

    return lb, ub


def prepare_bounds(bounds, n):
    if len(bounds) != 2:
        raise ValueError("`bounds` must contain 2 elements.")
    lb, ub = (np.asarray(b, dtype=float) for b in bounds)

    if lb.ndim == 0:
        lb = np.resize(lb, n)

    if ub.ndim == 0:
        ub = np.resize(ub, n)

    return lb, ub

