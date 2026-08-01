
def _pearsonr_bootstrap_ci(confidence_level, method, x, y, alternative, axis):
    """
    Compute the confidence interval for Pearson's R using the bootstrap.
    """
    def statistic(x, y, axis):
        statistic, _ = pearsonr(x, y, axis=axis)
        return statistic

    res = bootstrap((x, y), statistic, confidence_level=confidence_level, axis=axis,
                    paired=True, alternative=alternative, **method._asdict())
    # for one-sided confidence intervals, bootstrap gives +/- inf on one side
    res.confidence_interval = np.clip(res.confidence_interval, -1, 1)

    return ConfidenceInterval(*res.confidence_interval)

