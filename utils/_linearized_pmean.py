
def _linearized_pmean(a, p, *, axis=None, weights=None, xp=None):
    # pmean linearized as a function of p about p = 0; see gh-23407
    M0 = gmean(a, axis=axis, weights=weights)

    loga = xp.log(a)

    ln_avg = _xp_mean(loga, axis=axis, weights=weights)
    ln2_avg = _xp_mean(loga * loga, axis=axis, weights=weights)

    return M0 * (1 + 0.5 * p * (ln2_avg - ln_avg * ln_avg))

