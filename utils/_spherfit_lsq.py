
def _spherfit_lsq(theta, phi, r, nt, tt, np_, tp, w, eps):
    """
    Wrapper for sphere with iopt=-1 (least squares fit with fixed knots on sphere).
    Returns: tt, tp, c, fp, ier
    """
    theta = np.asarray(theta, dtype=np.float64)
    phi = np.asarray(phi, dtype=np.float64)
    r = np.asarray(r, dtype=np.float64)
    tt = np.asarray(tt, dtype=np.float64, copy=True)
    tp = np.asarray(tp, dtype=np.float64, copy=True)
    if w is None:
        w = np.ones(len(theta), dtype=np.float64)
    else:
        w = np.asarray(w, dtype=np.float64)
    m = len(theta)

    ntest = nt
    npest = np_

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

    # Call sphere with iopt=-1
    nt_out, tt_out, np_out, tp_out, c, fp, ier = _fitpack.sphere(
        -1, theta, phi, r, w, 0.0, ntest, npest, tt, tp, eps, wrk1, wrk2, iwrk)

    return tt_out, tp_out, c, fp, ier

