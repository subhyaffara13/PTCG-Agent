
def mwu_result_object(statistic, pvalue, zstatistic=None):
    res = MannwhitneyuResult(statistic, pvalue)
    if zstatistic is not None:
        res.zstatistic = zstatistic
    return res

