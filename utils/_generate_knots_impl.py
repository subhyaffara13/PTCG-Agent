
def _generate_knots_impl(x, y, w, xb, xe, k, s, nest, periodic, xp=np):

    acc = s * TOL
    m = x.size    # the number of data points

    if nest is None:
        # the max number of knots. This is set in _fitpack_impl.py line 274
        # and fitpack.pyf line 198
        # Ref: https://github.com/scipy/scipy/blob/596b586e25e34bd842b575bac134b4d6924c6556/scipy/interpolate/_fitpack_impl.py#L260-L263
        if periodic:
            nest = max(m + 2*k, 2*k + 3)
        else:
            nest = max(m + k + 1, 2*k + 3)
    else:
        if nest < 2*(k + 1):
            raise ValueError(f"`nest` too small: {nest = } < 2*(k+1) = {2*(k+1)}.")

    if not periodic:
        nmin = 2*(k + 1)    # the number of knots for an LSQ polynomial approximation
        nmax = m + k + 1  # the number of knots for the spline interpolation
    else:
        # Ref: https://github.com/scipy/scipy/blob/maintenance/1.16.x/scipy/interpolate/fitpack/fpperi.f#L54
        nmin = 2*(k + 1)    # the number of knots for an LSQ polynomial approximation
        # Ref: https://github.com/scipy/scipy/blob/maintenance/1.16.x/scipy/interpolate/fitpack/fpperi.f#L61
        nmax = m + 2*k  # the number of knots for the spline interpolation

    per = xe - xb
    # Ref: https://github.com/scipy/scipy/blob/maintenance/1.16.x/scipy/interpolate/fitpack/fpperi.f#L107-L123
    # Computes fp0 for constant function
    if periodic:
        t = np.zeros(nmin, dtype=float)
        for i in range(0, k + 1):
            t[i] = x[0] - (k - i) * per
            t[i + k + 1] = x[m - 1] + i * per
        _, fp = _get_residuals(x, y, t, k, w, periodic=periodic)
        # For periodic splines, check whether constant function
        # satisfies accuracy criterion
        # Also if maximal number of nodes is equal to the minimal
        # then constant function is the direct solution
        # Ref: https://github.com/scipy/scipy/blob/maintenance/1.16.x/scipy/interpolate/fitpack/fpperi.f#L600-L610
        if fp - s < acc or nmax == nmin:
            yield t
            return
    else:
        fp = 0.0
        fpold = 0.0

    # start from no internal knots
    if not periodic:
        t = np.asarray([xb]*(k+1) + [xe]*(k+1), dtype=float)
    else:
        # Ref: https://github.com/scipy/scipy/blob/maintenance/1.16.x/scipy/interpolate/fitpack/fpperi.f#L131
        # Initialize knot vector `t` of size (2k + 3) with zeros.
        # The central knot `t[k + 1]` is seeded with the midpoint value from `x`.
        # Note that, in the `if periodic:` block (in the main loop below),
        # the boundary knots `t[k]` and `t[n - k - 1]` are set to the endpoints `xb` and
        # `xe`. Then, the surrounding knots on both ends are updated to ensure
        # periodicity.
        # Specifically:
        # - Left-side knots are mirrored from the right end minus the period (`per`).
        # - Right-side knots are mirrored from the left end plus the period.
        # These updates ensure that the knot vector wraps around correctly for periodic
        # B-spline fitting.
        t = np.zeros(2*k + 3, dtype=float)
        t[k + 1] = x[(m + 1)//2 - 1]
        nplus = 1
    n = t.shape[0]

    # c  main loop for the different sets of knots. m is a safe upper bound
    # c  for the number of trials.
    for iter in range(m):
        # Ref: https://github.com/scipy/scipy/blob/maintenance/1.16.x/scipy/interpolate/fitpack/fpperi.f#L147-L158
        if periodic:
            n = t.shape[0]
            t[k] = xb
            t[n - k - 1] = xe
            for j in range(1, k + 1):
                t[k - j] = t[n - k - j - 1] - per
                t[n - k + j - 1] = t[k + j] + per
        yield xp.asarray(t)

        # construct the LSQ spline with this set of knots
        fpold = fp
        residuals, fp = _get_residuals(x, y, t, k, w=w,
                                        periodic=periodic)
        fpms = fp - s

        # c  test whether the approximation sinf(x) is an acceptable solution.
        # c  if f(p=inf) < s accept the choice of knots.
        if (abs(fpms) < acc) or (fpms < 0):
            return

        # ### c  increase the number of knots. ###

        # c  determine the number of knots nplus we are going to add.
        if n == nmin:
            # the first iteration
            nplus = 1
        else:
            delta = fpold - fp
            npl1 = int(nplus * fpms / delta) if delta > acc else nplus*2
            nplus = min(nplus*2, max(npl1, nplus//2, 1))

        # actually add knots
        for j in range(nplus):
            t = add_knot(x, t, k, residuals)

            # check if we have enough knots already

            n = t.shape[0]
            # c  if n = nmax, sinf(x) is an interpolating spline.
            # c  if n=nmax we locate the knots as for interpolation.
            if n >= nmax:
                if not periodic:
                    t = _not_a_knot(x, k)
                else:
                    t = _periodic_knots(x, k)
                yield xp.asarray(t)
                return

            # c  if n=nest we cannot increase the number of knots because of
            # c  the storage capacity limitation.
            if n >= nest:
                yield xp.asarray(t)
                return

            # recompute if needed
            if j < nplus - 1:
                residuals, _ = _get_residuals(x, y, t, k, w=w, periodic=periodic)

    # this should never be reached
    return

