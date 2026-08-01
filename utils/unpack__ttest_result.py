
def unpack_TtestResult(res, _):
    return (res.statistic, res.pvalue, res.df, res._alternative,
            res._standard_error, res._estimate)

