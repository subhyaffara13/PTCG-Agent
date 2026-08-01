
def _chi2_resampling_methods(observed, expected, correction, lambda_, method):

    if observed.ndim != 2:
        message = 'Use of `method` is only compatible with two-way tables.'
        raise ValueError(message)

    if correction:
        message = f'`{correction=}` is not compatible with `{method=}.`'
        raise ValueError(message)

    if lambda_ is not None:
        message = f'`{lambda_=}` is not compatible with `{method=}.`'
        raise ValueError(message)

    if isinstance(method, stats.PermutationMethod):
        res = _chi2_permutation_method(observed, expected, method)
    elif isinstance(method, stats.MonteCarloMethod):
        res = _chi2_monte_carlo_method(observed, expected, method)
    else:
        message = (f'`{method=}` not recognized; if provided, `method` must be an '
                   'instance of `PermutationMethod` or `MonteCarloMethod`.')
        raise ValueError(message)

    return Chi2ContingencyResult(res.statistic, res.pvalue, np.nan, expected)

