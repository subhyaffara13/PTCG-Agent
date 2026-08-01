
def _fisher_exact_rxc(table, alternative, method):
    if alternative is not None:
        message = ('`alternative` must be the default (None) unless '
                  '`table` has shape `(2, 2)` and `method is None`.')
        raise ValueError(message)

    if table.size == 0:
        raise ValueError("`table` must have at least one row and one column.")

    if table.shape[0] == 1 or table.shape[1] == 1 or np.all(table == 0):
        # Only one such table with those marginals
        return SignificanceResult(1.0, 1.0)

    if method is None:
        method = stats.MonteCarloMethod()

    if isinstance(method, stats.PermutationMethod):
        res = _fisher_exact_permutation_method(table, method)
    elif isinstance(method, stats.MonteCarloMethod):
        res = _fisher_exact_monte_carlo_method(table, method)
    else:
        message = (f'`{method=}` not recognized; if provided, `method` must be an '
                   'instance of `PermutationMethod` or `MonteCarloMethod`.')
        raise ValueError(message)

    return SignificanceResult(np.clip(res.statistic, None, 1.0), res.pvalue)

