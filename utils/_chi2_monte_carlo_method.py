
def _chi2_monte_carlo_method(observed, expected, method):
    method = method._asdict()

    if method.pop('rvs', None) is not None:
        message = ('If the `method` argument of `chi2_contingency` is an '
                   'instance of `MonteCarloMethod`, its `rvs` attribute '
                   'must be unspecified. Use the `MonteCarloMethod` `rng` argument '
                   'to control the random state.')
        raise ValueError(message)
    rng = np.random.default_rng(method.pop('rng', None))

    # `random_table.rvs` produces random contingency tables with the given marginals
    # under the null hypothesis of independence
    rowsums, colsums = stats.contingency.margins(observed)
    X = stats.random_table(rowsums.ravel(), colsums.ravel(), seed=rng)
    def rvs(size):
        n_resamples = size[0]
        return X.rvs(size=n_resamples).reshape(size)

    expected = expected.ravel()
    def statistic(table, axis):
        return np.sum((table - expected)**2/expected, axis=axis)

    return stats.monte_carlo_test(observed.ravel(), rvs, statistic,
                                  alternative='greater', **method)

