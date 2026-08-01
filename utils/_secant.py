
def _secant(xvals, fvals):
    """Perform a secant step, taking a little care"""
    # Secant has many "mathematically" equivalent formulations
    # x2 = x0 - (x1 - x0)/(f1 - f0) * f0
    #    = x1 - (x1 - x0)/(f1 - f0) * f1
    #    = (-x1 * f0 + x0 * f1) / (f1 - f0)
    #    = (-f0 / f1 * x1 + x0) / (1 - f0 / f1)
    #    = (-f1 / f0 * x0 + x1) / (1 - f1 / f0)
    x0, x1 = xvals[:2]
    f0, f1 = fvals[:2]
    if f0 == f1:
        return np.nan
    if np.abs(f1) > np.abs(f0):
        x2 = (-f0 / f1 * x1 + x0) / (1 - f0 / f1)
    else:
        x2 = (-f1 / f0 * x0 + x1) / (1 - f1 / f0)
    return x2

