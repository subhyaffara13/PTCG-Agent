
def _conditional_oddsratio(table):
    """
    Conditional MLE of the odds ratio for the 2x2 contingency table.
    """
    x, M, n, N = _hypergeom_params_from_table(table)
    # Get the bounds of the support.  The support of the noncentral
    # hypergeometric distribution with parameters M, n, and N is the same
    # for all values of the noncentrality parameter, so we can use 1 here.
    lo, hi = nchypergeom_fisher.support(M, n, N, 1)

    # Check if x is at one of the extremes of the support.  If so, we know
    # the odds ratio is either 0 or inf.
    if x == lo:
        # x is at the low end of the support.
        return 0
    if x == hi:
        # x is at the high end of the support.
        return np.inf

    nc = _nc_hypergeom_mean_inverse(x, M, n, N)
    return nc

