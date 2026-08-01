
def _ttest_finish(df, t, alternative):
    """Common code between all 3 t-test functions."""
    # We use ``stdtr`` directly here to preserve masked arrays

    if alternative == 'less':
        pval = special._ufuncs.stdtr(df, t)
    elif alternative == 'greater':
        pval = special._ufuncs.stdtr(df, -t)
    elif alternative == 'two-sided':
        pval = special._ufuncs.stdtr(df, -np.abs(t))*2
    else:
        raise ValueError("alternative must be "
                         "'less', 'greater' or 'two-sided'")

    if t.ndim == 0:
        t = t[()]
    if pval.ndim == 0:
        pval = pval[()]

    return t, pval

