
def wilcoxon_result_object(statistic, pvalue, zstatistic=None):
    res = WilcoxonResult(statistic, pvalue)
    if zstatistic is not None:
        res.zstatistic = zstatistic
    return res

