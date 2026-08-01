
def _regrid_fitpack(
    x, y, Z, *, kx=3, ky=3, s=0.0,
    maxit=50, nestx=None, nesty=None,
    bbox=None):
    """
    Core adaptive bivariate spline fitter using the 1/p-penalty convention.

    Parameters
    ----------
    x, y : array_like
        Strictly increasing coordinate vectors.
    Z : array_like, shape (len(x), len(y))
        Data grid.
    kx, ky : int, optional
        Spline degrees along x and y, default 3 (cubic).
    s : float, optional
        Target residual (`fp` target). `s = 0` requests an interpolatory
        surface; `s > 0` triggers smoothing with penalty weight **1/p**.
    maxit : int, optional
        Maximum iterations for the `p`-search when smoothing, default 50.
    nestx, nesty : int or None
        Max coefficient counts per axis (nesting limits).
    bbox : sequence of 4 scalars
        Optional domain limits `(xb, xe, yb, ye)`. Use `None` entries to skip.

    Returns
    -------
    NdBSpline
        Fitted 2-D spline surface.

    Notes
    -----
    The internal smoothing parameter `p` follows the **inverse**-penalty
    rule: penalty term is 1/p.  Hence, larger `p` -> weaker smoothing
    (approaching interpolation), while smaller `p` -> stronger smoothing.
    A sentinel value `p == -1` is interpreted as *p = inf*, corresponding to
    an exact (interpolatory) fit.

    The iterative process adaptively grows knot vectors based on residual
    energy and optionally performs a 1-D search over `p` to satisfy `fp ~ s`.
    """
    x_fit, y_fit, Z_fit, _, _ = _apply_bbox_grid(x, y, Z, bbox)

    if x_fit.size < (kx + 1) or y_fit.size < (ky + 1):
        raise ValueError(
            f"Not enough samples inside bbox for degrees (kx={kx}, ky={ky}). "
            f"Need at least k+1 per axis: ({kx+1}, {ky+1}). "
            f"Got ({x_fit.size}, {y_fit.size})."
        )

    xb = float(x_fit[0] if bbox[0] is None else bbox[0])
    xe = float(x_fit[-1] if bbox[1] is None else bbox[1])
    yb = float(y_fit[0] if bbox[2] is None else bbox[2])
    ye = float(y_fit[-1] if bbox[3] is None else bbox[3])

    p = -1

    if s == 0.0:
        if nestx is not None or nesty is not None:
            raise ValueError("s == 0 is interpolation only")
        # For special-case k=1 (e.g., Lyche and Morken, Eq.(2.16)),
        # _not_a_knot produces desired knot vector
        tx = _not_a_knot(x_fit, kx)
        ty = _not_a_knot(y_fit, ky)
        (Ax, Ay, Q) = _build_design_matrices(
             x_fit, y_fit, Z, tx, ty, kx, ky)
        C0, fp, _ = _solve_2d_fitpack(Ax, Ay, Q, p,
                                     kx, tx, x_fit, ky, ty,
                                     y_fit, Z_fit)
        return return_NdBSpline(fp, (tx, ty, C0), (kx, ky))

    tx, nestx, nminx, nmaxx = _initialise_knots(x_fit.size, xb, xe, kx, nest=nestx)
    ty, nesty, nminy, nmaxy = _initialise_knots(y_fit.size, yb, ye, ky, nest=nesty)

    fpold = None
    last_axis = "y"
    mpm = len(x) + len(y)
    fp0 = None
    nplusx = None
    nplusy = None

    # https://github.com/scipy/scipy/blob/v1.16.2/scipy/interpolate/fitpack/fpregr.f#L51-L300
    for _ in range(mpm):

        (Ax, Ay, Q) = _build_design_matrices(
             x_fit, y_fit, Z, tx, ty, kx, ky)
        # _solve_2d_fitpack now returns R = Z_fit - zhat alongside C0 and fp,
        # so we can reuse it directly for knot placement instead of
        # recomputing zhat a second time via tocsr + dense matmul.
        C0, fp, R = _solve_2d_fitpack(Ax, Ay, Q, p,
                                      kx, tx, x_fit,
                                      ky, ty, y_fit,
                                      Z_fit)

        # https://github.com/scipy/scipy/blob/v1.16.2/scipy/interpolate/fitpack/fpregr.f#L190
        # https://github.com/scipy/scipy/blob/v1.16.2/scipy/interpolate/fitpack/fpregr.f#L224
        if len(tx) == nminx and len(ty) == nminy:
            fp0 = fp

        if fp < s:
            break

        # https://github.com/scipy/scipy/blob/v1.16.2/scipy/interpolate/fitpack/fpregr.f#L265-L295
        if last_axis == "y":
            tx, nplusx = _add_knots(
                x_fit, kx, s, tx, nmin=nminx, nmax=nmaxx,
                nest=nestx, fp=fp, fpold=fpold,
                residuals=np.sum(R**2, axis=1),
                nplus=nplusx)
            last_axis = "x"
        else:
            ty, nplusy = _add_knots(
                y_fit, ky, s, ty, nmin=nminy, nmax=nmaxy,
                nest=nesty, fp=fp, fpold=fpold,
                residuals=np.sum(R**2, axis=0),
                nplus=nplusy)
            last_axis = "y"

        # When both knot vectors have reached their maximum size no further
        # growth is possible; break to avoid redundant loop iterations.
        if len(tx) >= nmaxx and len(ty) >= nmaxy:
            break

        fpold = fp

    if len(tx) == nminx and len(ty) == nminy:
        return return_NdBSpline(fp, (tx, ty, C0), (kx, ky))

    p = 1
    Drx, offset_dx, nc_dx = disc(tx, kx)
    Dry, offset_dy, nc_dy = disc(ty, ky)
    Drx = PackedMatrix(Drx, offset_dx, nc_dx)
    Dry = PackedMatrix(Dry, offset_dy, nc_dy)
    (Ax, Ay, Q) = _build_design_matrices(
        x_fit, y_fit, Z, tx, ty, kx, ky)
    _, C_sm, fp_sm = _p_search_hit_s(Ax, Drx, Ay, Dry, Q,
                                     kx, tx, x_fit, ky,
                                     ty, y_fit, Z_fit, s,
                                     fp0, maxit=maxit, p_init=p)
    return return_NdBSpline(fp_sm, (tx, ty, C_sm), (kx, ky))

