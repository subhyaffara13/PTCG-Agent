
def _fisher_exact_monte_carlo_method(table, method):
    method = method._asdict()

    if method.pop('rvs', None) is not None:
        message = ('If the `method` argument of `fisher_exact` is an '
                   'instance of `MonteCarloMethod`, its `rvs` attribute '
                   'must be unspecified. Use the `MonteCarloMethod` `rng` argument '
                   'to control the random state.')
        raise ValueError(message)
    rng = np.random.default_rng(method.pop('rng', None))

    # `random_table.rvs` produces random contingency tables with the given marginals
    # under the null hypothesis of independence
    shape = table.shape
    colsums = np.sum(table, axis=0)
    rowsums = np.sum(table, axis=1)
    totsum = np.sum(table)
    X = stats.random_table(rowsums, colsums, seed=rng)

    def rvs(size):
        n_resamples = size[0]
        return X.rvs(size=n_resamples).reshape(size)

    # axis signals to `monte_carlo_test` that statistic is vectorized, but we know
    # how it will pass the table(s), so we don't need to use `axis` explicitly.
    def statistic(table, axis):
        shape_ = (-1,) + shape if table.size > totsum else shape
        return X.pmf(table.reshape(shape_))

    # tables with *smaller* probability mass are considered to be more extreme
    return stats.monte_carlo_test(table.ravel(), rvs, statistic,
                                  alternative='less', **method)

