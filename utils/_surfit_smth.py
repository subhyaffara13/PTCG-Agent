
def _surfit_smth(x, y, z, w, xb, xe, yb, ye, kx, ky, s, eps):
    """
    Wrapper for surfit with iopt=0 (smoothing spline).
    Returns: nx, tx, ny, ty, c, fp, ier
    """
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    z = np.asarray(z, dtype=np.float64)
    m = len(x)

    # Handle None w value (default equal weights)
    if w is None:
        w = np.ones(m, dtype=np.float64)
    else:
        w = np.asarray(w, dtype=np.float64)

    # Handle None bbox values (matching f2py behavior: xb=dmin(x,m), etc.)
    if xb is None:
        xb = np.min(x)
    if xe is None:
        xe = np.max(x)
    if yb is None:
        yb = np.min(y)
    if ye is None:
        ye = np.max(y)

    # Estimate nxest and nyest
    nxest = max(kx + 1 + int(np.sqrt(m / 2)), 2 * (kx + 1))
    nyest = max(ky + 1 + int(np.sqrt(m / 2)), 2 * (ky + 1))
    nmax = max(nxest, nyest)

    # Handle None s value (default smoothing factor)
    if s is None:
        s = float(m)

    # Call surfit with iopt=0
    # Note: The C wrapper allocates tx, ty, and workspace arrays internally for iopt=1
    # We just need to pass dummy wrk here
    nx, tx, ny, ty, c, fp, ier = _fitpack.surfit_smth(
        x, y, z, w, xb, xe, yb, ye, kx, ky, s, nxest, nyest, nmax, eps)

    return nx, tx, ny, ty, c, fp, ier

