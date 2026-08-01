
def _value_and_jac_angle(func, xs, ys, xlim, ylim):
    """
    Parameters
    ----------
    func : callable
        A function that transforms the coordinates of a point (x, y) to a new coordinate
        system (u, v), and which can also take x and y as arrays of shape *shape* and
        returns (u, v) as a ``(2, shape)`` array.
    xs, ys : array-likes
        Points where *func* and its derivatives will be evaluated.
    xlim, ylim : pairs of floats
        (min, max) beyond which *func* should not be evaluated.

    Returns
    -------
    val
        Value of *func* at each point of ``(xs, ys)``.
    thetas_dx
        Angles (in radians) defined by the (u, v) components of the numerically
        differentiated df/dx vector, at each point of ``(xs, ys)``.  If needed, the
        differentiation step size is increased until at least one component of df/dx
        is nonzero, under the constraint of not going out of the *xlims*, *ylims*
        bounds.  If the gridline at a point is actually null (and the angle is thus not
        well defined), the derivatives are evaluated after taking a small step along y;
        this ensures e.g. that the tick at r=0 on a radial axis of a polar plot is
        parallel with the ticks at r!=0.
    thetas_dy
        Like *thetas_dx*, but for df/dy.
    """

    shape = np.broadcast_shapes(np.shape(xs), np.shape(ys))
    val = func(xs, ys)

    # Take finite difference steps towards the furthest bound; the step size will be the
    # min of epsilon and the distance to that bound.
    eps0 = np.finfo(float).eps ** (1/2)  # cf. scipy.optimize.approx_fprime

    def calc_eps(vals, lim):
        lo, hi = sorted(lim)
        dlo = vals - lo
        dhi = hi - vals
        eps_max = np.maximum(dlo, dhi)
        eps = np.where(dhi >= dlo, 1, -1) * np.minimum(eps0, eps_max)
        return eps, eps_max

    xeps, xeps_max = calc_eps(xs, xlim)
    yeps, yeps_max = calc_eps(ys, ylim)

    def calc_thetas(dfunc, ps, eps_p0, eps_max, eps_q):
        thetas_dp = np.full(shape, np.nan)
        missing = np.full(shape, True)
        eps_p = eps_p0
        for it, eps_q in enumerate([0, eps_q]):
            while missing.any() and (abs(eps_p) < eps_max).any():
                if it == 0 and (eps_p > 1).any():
                    break  # Degenerate derivative, move a bit along the other coord.
                eps_p = np.minimum(eps_p, eps_max)
                df_x, df_y = (dfunc(eps_p, eps_q) - dfunc(0, eps_q)) / eps_p
                good = missing & ((df_x != 0) | (df_y != 0))
                thetas_dp[good] = np.arctan2(df_y, df_x)[good]
                missing &= ~good
                eps_p *= 2
        return thetas_dp

    thetas_dx = calc_thetas(lambda eps_p, eps_q: func(xs + eps_p, ys + eps_q),
                            xs, xeps, xeps_max, yeps)
    thetas_dy = calc_thetas(lambda eps_p, eps_q: func(xs + eps_q, ys + eps_p),
                            ys, yeps, yeps_max, xeps)
    return (val, thetas_dx, thetas_dy)

