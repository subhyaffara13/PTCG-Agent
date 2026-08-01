
def _chi2_permutation_method(observed, expected, method):
    x, y = _untabulate(observed)
    # `permutation_test` with `permutation_type='pairings' permutes the order of `x`,
    # which pairs observations in `x` with different observations in `y`.
    def statistic(x):
        # crosstab the resample and compute the statistic
        table = crosstab(x, y)[1]
        return np.sum((table - expected)**2/expected)

    return stats.permutation_test((x,), statistic, permutation_type='pairings',
                                  alternative='greater', **method._asdict())

