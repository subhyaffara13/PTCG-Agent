
def _curfit(x, y, k, w=None, xb=None, xe=None, s=None, nest=None, iopt=0,
            t=None, c=None, n=None, fpint=None, nrdata=None):
    """
    Wrapper for curfit that provides a simpler interface.

    iopt=0: find smoothing spline (initial call)
    iopt=1: continue with current knots (refinement)
    iopt=-1: least squares fit with fixed knots

    Returns: n, t, c, fp, ier
    For compatibility with old code, can be unpacked as:
        _data = (x, y, w, xb, xe, k, s, n, t, c, fp, None, None, ier)
    """
    x = np.asarray(x, dtype=float, order='F').ravel('F')
    y = np.asarray(y, dtype=float, order='F').ravel('F')
    m = len(x)

    if w is None:
        w = np.ones(m, dtype=float)
    else:
        w = np.asarray(w, dtype=float, order='F').ravel('F')

    if xb is None:
        xb = float(x[0])
    else:
        xb = float(xb)
    if xe is None:
        xe = float(x[-1])
    else:
        xe = float(xe)
    if s is None:
        s = float(m)

    # In iopt=1 mode, callers may pass preallocated/resized t/c; prefer that
    # size as the working `nest` to keep workspace sizing consistent.
    if nest is None and t is not None:
        nest = len(t)

    k1 = k + 1

    if iopt == -1:
        # Fixed knots mode: t is provided
        if t is None:
            raise ValueError("t must be provided for iopt=-1")
        t = np.asarray(t, dtype=float, copy=True)
        nest = len(t)
        n = nest
    else:
        # Smoothing mode (iopt=0 or iopt=1)
        if nest is None:
            nest = (m + k + 1) if (s == 0.0) else (max(m // 2, 2 * k1))

        if iopt == 0:
            # Initial call: allocate new arrays
            t = np.zeros(nest, dtype=float)
        else:
            # Continuation (iopt=1): use existing arrays
            if t is None or c is None:
                raise ValueError("t and c must be provided for iopt=1")
            t = np.asarray(t, dtype=float, copy=True)
            if n is None:
                n = nest

    # Workspace for curfit
    lwrk = m * k1 + nest * (7 + 3 * k)
    wrk = np.zeros(lwrk, dtype=float)
    iwrk = np.zeros(nest, dtype=np.int32)

    # Call curfit (nest is inferred from len(t) in C code)
    n_out, t_out, c_out, fp, ier = _fitpack.curfit(iopt, x, y, w, xb, xe, k, s,
                                                   t, wrk, iwrk)

    # Return in old format for compatibility:
    # x, y, w, xb, xe, k, s, n, t, c, fp, fpint, nrdata, ier
    return x, y, w, xb, xe, k, s, n_out, t_out, c_out, fp, fpint, nrdata, ier

