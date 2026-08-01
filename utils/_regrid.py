
def _regrid(x, y, z, *, bbox=None, kx=3, ky=3, s=0.0, maxit=50):
    """
    Interface for 2-D smoothing B-spline fitting (1/p penalty form).

    Parameters
    ----------
    x, y : array_like
        Strictly increasing 1-D coordinate vectors.
    z : array_like, shape (len(x), len(y))
        Data grid.
    bbox : sequence of 4 scalars
        Optional bounding box ``(xb, xe, yb, ye)``; use ``None`` entries to disable.
    kx, ky : int, optional
        Spline degrees along `x` and `y`, default cubic (3).
    s : float, optional
        Target smoothing residual (`fp` target). Must satisfy ``s >= 0``.
        The underlying formulation uses a **1/p** penalty, meaning:
        - small `p` -> heavy smoothing,
        - large `p` -> light smoothing (approaching interpolation).
        Setting `p == -1` internally denotes *p = inf*, i.e. a pure interpolant.
    maxit : int, optional
        Maximum iterations for `p`-search if invoked.

    Returns
    -------
    NdBSpline
        Fitted bivariate spline surface.
    """
    if bbox is None:
        bbox = [None]*4

    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    z = np.asarray(z, dtype=float)
    bbox = np.ravel(bbox)
    s = float(s)

    if not np.all(np.diff(x) > 0.0):
        raise ValueError("x must be strictly increasing")
    if not np.all(np.diff(y) > 0.0):
        raise ValueError("y must be strictly increasing")
    if x.size != z.shape[0]:
        raise ValueError("x dimension of z must have same number of elements as x")
    if y.size != z.shape[1]:
        raise ValueError("y dimension of z must have same number of elements as y")
    if (s < 0.0):
        raise ValueError("s should be s >= 0.0")
    if not bbox.shape == (4,):
        raise ValueError(f"bbox shape should be (4,), found: {bbox.shape}")

    return _regrid_fitpack(
        x, y, z, kx=kx, ky=ky, s=s, maxit=maxit,
        nestx=None, nesty=None, bbox=bbox)

