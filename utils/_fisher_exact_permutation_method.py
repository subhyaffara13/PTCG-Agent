
def _fisher_exact_permutation_method(table, method):
    x, y = _untabulate(table)
    colsums = np.sum(table, axis=0)
    rowsums = np.sum(table, axis=1)
    X = stats.random_table(rowsums, colsums)

    # `permutation_test` with `permutation_type='pairings' permutes the order of `x`,
    # which pairs observations in `x` with different observations in `y`.
    def statistic(x):
        # crosstab the resample and compute the statistic
        table = stats.contingency.crosstab(x, y)[1]
        return X.pmf(table)

    # tables with *smaller* probability mass are considered to be more extreme
    return stats.permutation_test((x,), statistic, permutation_type='pairings',
                                  alternative='less', **method._asdict())

