
def _surfit_lsq(x, y, z, nx, tx, ny, ty, w, xb, xe, yb, ye, kx, ky, eps):
    """
    Wrapper for surfit with iopt=-1 (least squares fit with fixed knots).
    Returns: tx, ty, c, fp, ier
    """
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    z = np.asarray(z, dtype=np.float64)
    m = len(x)

    if w is None:
        w = np.ones(m, dtype=np.float64)
    else:
        w = np.asarray(w, dtype=np.float64, copy=True)

    tx = np.asarray(tx, dtype=np.float64, copy=True)
    ty = np.asarray(ty, dtype=np.float64, copy=True)

    nxest = nx
    nyest = ny
    nmax = max(nx, ny)
    if eps is None:
        eps = 1e-16
    else:
        if not (0.0 < eps < 1.0):
            raise ValueError("eps must be in the range (0.0, 1.0)")

    # Call surfit with iopt=-1, tx/ty are modified in-place.
    c, fp, ier = _fitpack.surfit_lsq(
        x, y, z, w, xb, xe, yb, ye, kx, ky, 0.0, nxest, nyest, nmax, eps, tx, ty)

    return tx, ty, c, fp, ier

