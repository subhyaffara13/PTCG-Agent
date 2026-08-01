
def _nolan_round_difficult_input(
    x0, alpha, beta, zeta, x_tol_near_zeta, alpha_tol_near_one
):
    """Round difficult input values for Nolan's method in [NO]."""

    # following Nolan's STABLE,
    #   "1. When 0 < |alpha-1| < 0.005, the program has numerical problems
    #   evaluating the pdf and cdf.  The current version of the program sets
    #   alpha=1 in these cases. This approximation is not bad in the S0
    #   parameterization."
    if np.abs(alpha - 1) < alpha_tol_near_one:
        alpha = 1.0

    #   "2. When alpha=1 and |beta| < 0.005, the program has numerical
    #   problems.  The current version sets beta=0."
    # We seem to have addressed this through re-expression of g(theta) here

    x0 = _nolan_round_x_near_zeta(x0, alpha, zeta, x_tol_near_zeta)
    return x0, alpha, beta

