
def quantile_test_reference(x, q, p, alternative):
    res = stats.quantile_test(x, q=q, p=p, alternative=alternative)
    return res.statistic, res.pvalue, *res.confidence_interval()

