
def unpack_ttest_result(res):
    low, high = res.confidence_interval()
    return (res.statistic, res.pvalue, res.df, res._standard_error,
            res._estimate, low, high)

