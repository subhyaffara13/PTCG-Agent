
def _ci_lower(table, alpha):
    """
    Compute the lower end of the confidence interval.
    """
    if _sample_odds_ratio(table) == 0:
        return 0

    x, M, n, N = _hypergeom_params_from_table(table)

    nc = _solve(lambda nc: nchypergeom_fisher.sf(x - 1, M, n, N, nc) - alpha)
    return nc

