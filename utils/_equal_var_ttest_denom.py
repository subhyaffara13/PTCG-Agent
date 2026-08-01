
def _equal_var_ttest_denom(v1, n1, v2, n2, xp=None):
    xp = array_namespace(v1, v2) if xp is None else xp

    # If there is a single observation in one sample, this formula for pooled
    # variance breaks down because the variance of that sample is undefined.
    # The pooled variance is still defined, though, because the (n-1) in the
    # numerator should cancel with the (n-1) in the denominator, leaving only
    # the sum of squared differences from the mean: zero.
    v1 = xp.where(xp.asarray(n1 == 1), 0., v1)
    v2 = xp.where(xp.asarray(n2 == 1), 0., v2)

    df = n1 + n2 - 2.0
    svar = ((n1 - 1) * v1 + (n2 - 1) * v2) / df
    denom = xp.sqrt(svar * (1.0 / n1 + 1.0 / n2))
    df = xp.asarray(df, dtype=denom.dtype)
    return df, denom

