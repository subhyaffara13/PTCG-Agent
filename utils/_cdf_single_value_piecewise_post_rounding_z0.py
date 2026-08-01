
def _cdf_single_value_piecewise_post_rounding_Z0(x0, alpha, beta, quad_eps,
                                                 x_tol_near_zeta):
    """Calculate cdf using Nolan's methods as detailed in [NO]."""
    _nolan = Nolan(alpha, beta, x0)
    zeta = _nolan.zeta
    xi = _nolan.xi
    c1 = _nolan.c1
    # c2 = _nolan.c2
    c3 = _nolan.c3
    g = _nolan.g
    # round x0 to zeta again if needed. zeta was recomputed and may have
    # changed due to floating point differences.
    # See https://github.com/scipy/scipy/pull/18133
    x0 = _nolan_round_x_near_zeta(x0, alpha, zeta, x_tol_near_zeta)
    # handle Nolan's initial case logic
    if (alpha == 1 and beta < 0) or x0 < zeta:
        # NOTE: Nolan's paper has a typo here!
        # He states F(x) = 1 - F(x, alpha, -beta), but this is clearly
        # incorrect since F(-infty) would be 1.0 in this case
        # Indeed, the alpha != 1, x0 < zeta case is correct here.
        return 1 - _cdf_single_value_piecewise_post_rounding_Z0(
            -x0, alpha, -beta, quad_eps, x_tol_near_zeta
        )
    elif x0 == zeta:
        return 0.5 - xi / np.pi

    # following Nolan, we may now assume
    #   x0 > zeta when alpha != 1
    #   beta > 0 when alpha == 1

    # spare calculating integral on null set
    # use isclose as macos has fp differences
    if np.isclose(-xi, np.pi / 2, rtol=1e-014, atol=1e-014):
        return c1

    def integrand(theta):
        g_1 = g(theta)
        return np.exp(-g_1)

    with np.errstate(all="ignore"):
        # shrink supports where required
        left_support = -xi
        right_support = np.pi / 2
        if alpha > 1:
            # integrand(t) monotonic 0 to 1
            if integrand(-xi) != 0.0:
                res = optimize.minimize(
                    integrand,
                    (-xi,),
                    method="L-BFGS-B",
                    bounds=[(-xi, np.pi / 2)],
                )
                left_support = res.x[0]
        else:
            # integrand(t) monotonic 1 to 0
            if integrand(np.pi / 2) != 0.0:
                res = optimize.minimize(
                    integrand,
                    (np.pi / 2,),
                    method="L-BFGS-B",
                    bounds=[(-xi, np.pi / 2)],
                )
                right_support = res.x[0]

        intg, *ret = integrate.quad(
            integrand,
            left_support,
            right_support,
            points=[left_support, right_support],
            limit=100,
            epsrel=quad_eps,
            epsabs=0,
            full_output=1,
        )

    return c1 + c3 * intg

