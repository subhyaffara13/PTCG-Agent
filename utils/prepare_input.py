
def prepare_input(x, y, axis, dydx=None, xp=None):
    """Prepare input for cubic spline interpolators.

    All data are converted to numpy arrays and checked for correctness.
    Axes equal to `axis` of arrays `y` and `dydx` are moved to be the 0th
    axis. The value of `axis` is converted to lie in
    [0, number of dimensions of `y`).
    """

    x, y = map(xp.asarray, (x, y))
    if xp.isdtype(x.dtype, "complex floating"):
        raise ValueError("`x` must contain real values.")
    x = xp.astype(x, xp.float64)

    if xp.isdtype(y.dtype, "complex floating"):
        dtype = xp.complex128
    else:
        dtype = xp.float64

    if dydx is not None:
        dydx = xp.asarray(dydx)
        if y.shape != dydx.shape:
            raise ValueError("The shapes of `y` and `dydx` must be identical.")
        if xp.isdtype(dydx.dtype, "complex floating"):
            dtype = xp.complex128
        dydx = xp.astype(dydx, dtype, copy=False)

    y = xp.astype(y, dtype, copy=False)
    axis = axis % y.ndim
    if x.ndim != 1:
        raise ValueError("`x` must be 1-dimensional.")
    if x.shape[0] < 2:
        raise ValueError("`x` must contain at least 2 elements.")
    if x.shape[0] != y.shape[axis]:
        raise ValueError(f"The length of `y` along `axis`={axis} doesn't "
                         "match the length of `x`")

    if not xp.all(xp.isfinite(x)):
        raise ValueError("`x` must contain only finite values.")
    if not xp.all(xp.isfinite(y)):
        raise ValueError("`y` must contain only finite values.")

    if dydx is not None and not xp.all(xp.isfinite(dydx)):
        raise ValueError("`dydx` must contain only finite values.")

    dx = xp.diff(x)
    if xp.any(dx <= 0):
        raise ValueError("`x` must be strictly increasing sequence.")

    y = xp.moveaxis(y, axis, 0)
    if dydx is not None:
        dydx = xp.moveaxis(dydx, axis, 0)

    return x, dx, y, axis, dydx

