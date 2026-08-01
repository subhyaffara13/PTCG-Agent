
def _pack_CorrelationResult(statistic, pvalue, correlation):
    res = SignificanceResult(statistic, pvalue)
    res.correlation = correlation
    return res

