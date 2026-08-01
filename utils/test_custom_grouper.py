
def test_custom_grouper(unit):
    index = date_range(datetime(2005, 1, 1), datetime(2005, 1, 10), freq="Min")
    dti = index.as_unit(unit)
    s = Series(np.array([1] * len(dti)), index=dti, dtype="int64")

    b = Grouper(freq=Minute(5))
    g = s.groupby(b)

    # check all cython functions work
    g.ohlc()  # doesn't use _cython_agg_general
    funcs = ["sum", "mean", "prod", "min", "max", "var"]
    for f in funcs:
        g._cython_agg_general(f, alt=None, numeric_only=True)

    b = Grouper(freq=Minute(5), closed="right", label="right")
    g = s.groupby(b)
    # check all cython functions work
    g.ohlc()  # doesn't use _cython_agg_general
    funcs = ["sum", "mean", "prod", "min", "max", "var"]
    for f in funcs:
        g._cython_agg_general(f, alt=None, numeric_only=True)

    assert g.ngroups == 2593
    assert notna(g.mean()).all()

    # construct expected val
    arr = [1] + [5] * 2592
    idx = dti[0:-1:5]
    idx = idx.append(dti[-1:])
    idx = DatetimeIndex(idx, freq="5min").as_unit(unit)
    expect = Series(arr, index=idx)

    # GH2763 - return input dtype if we can
    result = g.agg("sum")
    tm.assert_series_equal(result, expect)

