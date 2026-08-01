
def _pvalue_dunnett(
    rho: np.ndarray, df: int, statistic: np.ndarray,
    alternative: Literal['two-sided', 'less', 'greater'],
    rng: SeedType = None
) -> np.ndarray:
    """pvalue from the multivariate t-distribution.

    Critical values come from the multivariate student-t distribution.
    """
    statistic = statistic.reshape(-1, 1)

    mvt = stats.multivariate_t(shape=rho, df=df, seed=rng)
    if alternative == "two-sided":
        statistic = abs(statistic)
        pvalue = 1 - mvt.cdf(statistic, lower_limit=-statistic)
    elif alternative == "greater":
        pvalue = 1 - mvt.cdf(statistic, lower_limit=-np.inf)
    else:
        pvalue = 1 - mvt.cdf(np.inf, lower_limit=statistic)

    return np.atleast_1d(pvalue)

