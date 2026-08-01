
def _hypergeom_params_from_table(table):
    # The notation M, n and N is consistent with stats.hypergeom and
    # stats.nchypergeom_fisher.
    x = table[0, 0]
    M = table.sum()
    n = table[0].sum()
    N = table[:, 0].sum()
    return x, M, n, N

