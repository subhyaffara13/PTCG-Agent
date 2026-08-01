
def wilcoxon_result_unpacker(res, _):
    if hasattr(res, 'zstatistic'):
        return res.statistic, res.pvalue, res.zstatistic
    else:
        return res.statistic, res.pvalue

