
def pack_TtestResult(statistic, pvalue, df, alternative, standard_error,
                     estimate):
    xp = array_namespace(statistic, pvalue)
    # Due to behavior of `_axis_nan_policy` decorator, `alternative` can be any number
    # of dimensions, but there is at most one unique non-NaN value.
    # `_xp_mean` with `nan_policy='omit'` is a JIT-compatible way to extract it.
    alternative = xp.asarray(alternative)
    alternative = (_xp_mean(alternative, axis=None, nan_policy='omit', warn=False)
                   if xp_size(alternative) != 0 else xp.nan)
    return TtestResult(statistic, pvalue, df=df, alternative=alternative,
                       standard_error=standard_error, estimate=estimate)

