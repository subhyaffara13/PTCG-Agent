
def _ci_upper(table, alpha):
    """
    Compute the upper end of the confidence interval.
    """
    if _sample_odds_ratio(table) == np.inf:
        return np.inf

    x, M, n, N = _hypergeom_params_from_table(table)

    # nchypergeom_fisher.cdf is a decreasing function of nc, so we negate
    # it in the lambda expression.
    nc = _solve(lambda nc: -nchypergeom_fisher.cdf(x, M, n, N, nc) + alpha)
    return nc

