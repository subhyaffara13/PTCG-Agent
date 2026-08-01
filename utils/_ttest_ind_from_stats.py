
def _ttest_ind_from_stats(mean1, mean2, denom, df, alternative, xp=None):
    xp = array_namespace(mean1, mean2, denom) if xp is None else xp

    d = mean1 - mean2
    with np.errstate(divide='ignore', invalid='ignore'):
        t = xp.divide(d, denom)

    dist = _SimpleStudentT(xp.asarray(df, dtype=t.dtype, device=xp_device(t)))
    prob = _get_pvalue(t, dist, alternative, xp=xp)
    prob = prob[()] if prob.ndim == 0 else prob

    t = t[()] if t.ndim == 0 else t
    prob = prob[()] if prob.ndim == 0 else prob
    return t, prob

