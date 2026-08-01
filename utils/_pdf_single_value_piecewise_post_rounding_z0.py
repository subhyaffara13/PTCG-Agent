
def _pdf_single_value_piecewise_post_rounding_Z0(x0, alpha, beta, quad_eps,
                                                 x_tol_near_zeta):
    """Calculate pdf using Nolan's methods as detailed in [NO]."""

    _nolan = Nolan(alpha, beta, x0)
    zeta = _nolan.zeta
    xi = _nolan.xi
    c2 = _nolan.c2
    g = _nolan.g

    # round x0 to zeta again if needed. zeta was recomputed and may have
    # changed due to floating point differences.
    # See https://github.com/scipy/scipy/pull/18133
    x0 = _nolan_round_x_near_zeta(x0, alpha, zeta, x_tol_near_zeta)
    # handle Nolan's initial case logic
    if x0 == zeta:
        return (
            sc.gamma(1 + 1 / alpha)
            * np.cos(xi)
            / np.pi
            / ((1 + zeta ** 2) ** (1 / alpha / 2))
        )
    elif x0 < zeta:
        return _pdf_single_value_piecewise_post_rounding_Z0(
            -x0, alpha, -beta, quad_eps, x_tol_near_zeta
        )

    # following Nolan, we may now assume
    #   x0 > zeta when alpha != 1
    #   beta != 0 when alpha == 1

    # spare calculating integral on null set
    # use isclose as macos has fp differences
    if np.isclose(-xi, np.pi / 2, rtol=1e-014, atol=1e-014):
        return 0.0

    def integrand(theta):
        # limit any numerical issues leading to g_1 < 0 near theta limits
        g_1 = g(theta)
        if not np.isfinite(g_1) or g_1 < 0:
            g_1 = 0
        return g_1 * np.exp(-g_1)

    with np.errstate(all="ignore"):
        peak = optimize.bisect(
            lambda t: g(t) - 1, -xi, np.pi / 2, xtol=quad_eps
        )

        # this integrand can be very peaked, so we need to force
        # QUADPACK to evaluate the function inside its support
        #

        # lastly, we add additional samples at
        #   ~exp(-100), ~exp(-10), ~exp(-5), ~exp(-1)
        # to improve QUADPACK's detection of rapidly descending tail behavior
        # (this choice is fairly ad hoc)
        tail_points = [
            optimize.bisect(lambda t: g(t) - exp_height, -xi, np.pi / 2)
            for exp_height in [100, 10, 5]
            # exp_height = 1 is handled by peak
        ]
        # Symmetry is used to ensure x > zeta as above. Integration 
        # becomes numerically unstable so let `quad` handle 
        # integration points
        if beta != -1:
            intg_points = [0, peak] + tail_points
        else:
            intg_points = None

        intg, *ret = integrate.quad(
            integrand,
            -xi,
            np.pi / 2,
            points=intg_points,
            limit=100,
            epsrel=quad_eps,
            epsabs=0,
            full_output=1,
        )

    return c2 * intg

