
def _regrid_smth(x, y, z, xb, xe, yb, ye, kx, ky, s, maxit):
    """
    Wrapper for regrid with iopt=0 (smoothing spline on rectangular grid).
    Returns: nx, tx, ny, ty, c, fp, ier
    """
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    z = np.asarray(z, dtype=np.float64)
    mx = len(x)
    my = len(y)

    # Handle None values for bbox
    if xb is None:
        xb = np.min(x)
    if xe is None:
        xe = np.max(x)
    if yb is None:
        yb = np.min(y)
    if ye is None:
        ye = np.max(y)

    # Estimate nxest and nyest
    nxest = mx + kx + 1
    nyest = my + ky + 1

    # Workspace
    lwrk = 4 + mx + my + nxest * (my + 2 * kx + 5) \
           + nyest * (2 * ky + 5) + mx * (kx + 1) \
           + my * (ky + 1) + \
           max((nxest - kx - 1) * (nyest - ky - 1), my)

    wrk = np.zeros(lwrk, dtype=np.float64)
    kwrk = 3 + mx + my + nxest + nyest
    iwrk = np.zeros(kwrk, dtype=np.int32)

    # Call regrid with iopt=0
    nx, tx, ny, ty, c, fp, ier = _fitpack.regrid(
        0, x, y, z, xb, xe, yb, ye, kx, ky, s, nxest, nyest, maxit, wrk, iwrk)

    return nx, tx, ny, ty, c, fp, ier

