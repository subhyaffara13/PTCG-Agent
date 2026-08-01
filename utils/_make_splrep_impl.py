
def _make_splrep_impl(x, y, w, xb, xe, k, s, t, nest, periodic, xp=np):
    """Shared infra for make_splrep and make_splprep.
    """
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
        if t is not None:
            raise ValueError("Either supply `t` or `nest`.")

    if t is None:
        gen = _generate_knots_impl(x, y, w, xb, xe, k, s, nest, periodic)
        t = list(gen)[-1]
    else:
        fpcheck(x, t, k, periodic=periodic)

    if t.shape[0] == 2 * (k + 1):
        # nothing to optimize
        _, _, c, _, _ = _lsq_solve_qr(x, y, t, k, w, periodic=periodic)
        t, c = xp.asarray(t), xp.asarray(c)
        return BSpline(t, c, k)

    ### solve ###

    # c  initial value for p.
    # https://github.com/scipy/scipy/blob/maintenance/1.11.x/scipy/interpolate/fitpack/fpcurf.f#L253
    if periodic:
        # N.B. - Check _lsq_solve_qr computation
        # of p for periodic splines
        R, A1, A2, Z, Y, _, p, _ = _lsq_solve_qr_for_root_rati_periodic(x, y, t, k, w)
    else:
        R, Y, _, _, _ = _lsq_solve_qr(x, y, t, k, w, periodic=periodic)
    nc = t.shape[0] -k -1
    if not periodic:
        p = nc / R[:, 0].sum()

    # ### bespoke solver ####
    # initial conditions
    # f(p=inf) : LSQ spline with knots t   (XXX: reuse R, c)
    # N.B. - Check _lsq_solve_qr which is called
    # via _get_residuals for logic behind
    # computation of fp for periodic splines
    _, fp = _get_residuals(x, y, t, k, w, periodic=periodic)
    fpinf = fp - s

    # f(p=0): LSQ spline without internal knots
    if not periodic:
        _, fp0 = _get_residuals(x, y, np.array([xb]*(k+1) + [xe]*(k+1)), k, w)
        fp0 = fp0 - s
    else:
        # f(p=0) is fp for constant function
        # in case of periodic splines
        per = xe - xb
        tc = np.zeros(2*(k + 1), dtype=float)
        for i in range(0, k + 1):
            tc[i] = x[0] - (k - i) * per
            tc[i + k + 1] = x[m - 1] + i * per
        _, fp0 = _get_residuals(x, y, tc, k, w, periodic=periodic)
        fp0 = fp0 - s

    # solve
    bracket = (0, fp0), (np.inf, fpinf)
    if not periodic:
        f = F(x, y, t, k=k, s=s, w=w, R=R, Y=Y)
    else:
        f = Fperiodic(x, y, t, k=k, s=s, w=w, R=R, Y=Y, A1=A1, A2=A2, Z=Z)
    _ = root_rati(f, p, bracket, acc)

    # solve ALTERNATIVE: is roughly equivalent, gives slightly different results
    # starting from scratch, that would have probably been tolerable;
    # backwards compatibility dictates that we replicate the FITPACK minimizer though.
 #   f = F(x, y, t, k=k, s=s, w=w, R=R, Y=Y)
 #   from scipy.optimize import root_scalar
 #   res_ = root_scalar(f, x0=p, rtol=acc)
 #   assert res_.converged

    # f.spl is the spline corresponding to the found `p` value
    t, c, k = f.spl.tck
    axis, extrap = f.spl.axis, f.spl.extrapolate
    t, c = xp.asarray(t), xp.asarray(c)
    spl = BSpline.construct_fast(t, c, k, axis=axis, extrapolate=extrap)
    return spl

