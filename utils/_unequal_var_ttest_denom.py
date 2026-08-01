
def _unequal_var_ttest_denom(v1, n1, v2, n2, xp=None):
    xp = array_namespace(v1, v2) if xp is None else xp
    vn1 = v1 / n1
    vn2 = v2 / n2
    with np.errstate(divide='ignore', invalid='ignore'):
        df = (vn1 + vn2)**2 / (vn1**2 / (n1 - 1) + vn2**2 / (n2 - 1))

    # If df is undefined, variances are zero (assumes n1 > 0 & n2 > 0).
    # Hence it doesn't matter what df is as long as it's not NaN.
    df = xp.where(xp.isnan(df), 1., df)
    denom = xp.sqrt(vn1 + vn2)
    return df, denom

