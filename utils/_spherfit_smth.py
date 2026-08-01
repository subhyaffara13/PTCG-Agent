
def _spherfit_smth(theta, phi, r, w, s, eps):
    """
    Wrapper for sphere with iopt=0 (smoothing spline on sphere).
    Returns: nt, tt, np, tp, c, fp, ier
    """
    theta = np.asarray(theta, dtype=np.float64)
    phi = np.asarray(phi, dtype=np.float64)
    r = np.asarray(r, dtype=np.float64)
    if w is None:
        w = np.ones(len(theta), dtype=np.float64)
    else:
        w = np.asarray(w, dtype=np.float64)
    m = len(theta)

    # Estimate ntest and npest
    ntest = 8 + int(np.sqrt(m / 2))
    npest = 8 + int(np.sqrt(m / 2))

    # Workspace
    # lwrk1: 185+52*v+10*u+14*u*v+8*(u-1)*v**2+8*m
    # lwrk2: 48+21*v+7*u*v+4*(u-1)*v**2
    # where u = ntest - 7, v = npest - 7
    u = ntest - 7
    v = npest - 7
    lwrk1 = 185 + 52*v + 10*u + 14*u*v + 8*(u-1)*v*v + 8*m
    lwrk2 = 48 + 21*v + 7*u*v + 4*(u-1)*v*v
    kwrk = m + (ntest - 7) * (npest - 7)
    wrk1 = np.zeros(lwrk1, dtype=np.float64)
    wrk2 = np.zeros(lwrk2, dtype=np.float64)
    iwrk = np.zeros(kwrk, dtype=np.int32)

    # Call sphere with iopt=0
    nt, tt, np_, tp, c, fp, ier = _fitpack.sphere(
        0, theta, phi, r, w, s, ntest, npest,
        np.array([0.]), np.array([0.]),  # dummy input for tt and tp, ignored
        eps, wrk1, wrk2, iwrk)

    return nt, tt, np_, tp, c, fp, ier

