
def _cdf_single_value_piecewise_Z0(x0, alpha, beta, **kwds):

    quad_eps = kwds.get("quad_eps", _QUAD_EPS)
    x_tol_near_zeta = kwds.get("piecewise_x_tol_near_zeta", 0.005)
    alpha_tol_near_one = kwds.get("piecewise_alpha_tol_near_one", 0.005)

    zeta = -beta * np.tan(np.pi * alpha / 2.0)
    x0, alpha, beta = _nolan_round_difficult_input(
        x0, alpha, beta, zeta, x_tol_near_zeta, alpha_tol_near_one
    )

    # some other known distribution cdfs / analytical cases
    # TODO: add more where possible with test coverage,
    # eg https://en.wikipedia.org/wiki/Stable_distribution#Other_analytic_cases
    if alpha == 2.0:
        # normal
        return _norm_cdf(x0 / np.sqrt(2))
    elif alpha == 0.5 and beta == 1.0:
        # levy
        # since S(1/2, 1, gamma, delta; <x>) ==
        # S(1/2, 1, gamma, gamma + delta; <x0>).
        _x = x0 + 1
        if _x <= 0:
            return 0

        return sc.erfc(np.sqrt(0.5 / _x))
    elif alpha == 1.0 and beta == 0.0:
        # cauchy
        return 0.5 + np.arctan(x0) / np.pi

    return _cdf_single_value_piecewise_post_rounding_Z0(
        x0, alpha, beta, quad_eps, x_tol_near_zeta
    )

