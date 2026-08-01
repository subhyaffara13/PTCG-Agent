
def test_cython_agg_empty_buckets(op, targop, observed):
    df = DataFrame([11, 12, 13])
    grps = range(0, 55, 5)

    # calling _cython_agg_general directly, instead of via the user API
    # which sets different values for min_count, so do that here.
    g = df.groupby(pd.cut(df[0], grps), observed=observed)
    result = g._cython_agg_general(op, alt=None, numeric_only=True)

    g = df.groupby(pd.cut(df[0], grps), observed=observed)
    expected = g.agg(lambda x: targop(x))
    tm.assert_frame_equal(result, expected)

