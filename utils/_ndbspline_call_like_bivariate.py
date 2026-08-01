
def _ndbspline_call_like_bivariate(ndbs, x, y, dx=0, dy=0, grid=True):
    """
    Evaluate a 2D `NdBSpline` like a classical bivariate API.

    Parameters
    ----------
    ndbs : NdBSpline
        A 2D spline object (``len(ndbs.t) == 2``).
    x, y : array_like
        Sample locations. If ``grid=True``, these must be 1-D strictly
        increasing vectors. If ``grid=False``, they can be broadcastable
        arrays of the same shape.
    dx, dy : int, optional
        Derivative orders along `x` and `y` respectively, by default 0.
    grid : bool, optional
        If True, evaluate on the cartesian product of `x` and `y`;
        otherwise treat `(x, y)` as paired coordinates, by default True.

    Returns
    -------
    ndarray or (ndarray, dict)
        Evaluated values with shape:
        - ``(len(x), len(y), ...)`` if ``grid=True``.
        - ``x.shape + ...`` if ``grid=False``.

    Raises
    ------
    ValueError
        If `ndbs` is not 2D, derivatives are negative, or monotonicity checks fail.

    Notes
    -----
    This is a thin convenience wrapper around ``NdBSpline.__call__`` with input
    validation and optional profiling.
    """
    if len(ndbs.t) != 2:
        raise ValueError("ndbs must be a 2D NdBSpline (len(t) == 2).")

    dx = _validate_int(dx, 'dx')
    dy = _validate_int(dy, 'dy')
    if dx < 0 or dy < 0:
        raise ValueError("order of derivative must be positive or zero")

    trailing = ndbs.c.shape[2:]
    x = np.asarray(x)
    y = np.asarray(y)

    if grid:
        if x.size == 0 or y.size == 0:
            vals = np.zeros((x.size, y.size) + trailing, dtype=ndbs.c.dtype)
            return vals

        if (x.size >= 2) and (not np.all(np.diff(x) >= 0.0)):
            raise ValueError("x must be strictly increasing when `grid` is True")
        if (y.size >= 2) and (not np.all(np.diff(y) >= 0.0)):
            raise ValueError("y must be strictly increasing when `grid` is True")

        X, Y = np.meshgrid(x, y, indexing="ij")
        xi = np.stack((X, Y), axis=-1)  # (len(x), len(y), 2)

        vals = ndbs(xi, nu=(dx, dy), extrapolate=ndbs.extrapolate)

        return vals
    else:
        if x.shape != y.shape:
            x, y = np.broadcast_arrays(x, y)

        if x.size == 0:
            return np.zeros(x.shape + trailing, dtype=ndbs.c.dtype)
        xi = np.stack((x.ravel(), y.ravel()), axis=-1)
        vals = ndbs(xi, nu=(dx, dy), extrapolate=ndbs.extrapolate)
        return vals.reshape(x.shape + trailing)

