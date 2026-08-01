
def test_apply_without_aggregation(func, _test_series):
    # both resample and groupby should work w/o aggregation
    t = func(_test_series)
    result = t.apply(lambda x: x)
    tm.assert_series_equal(result, _test_series)

