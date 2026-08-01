
def test_apply_without_aggregation2(_test_series):
    grouped = _test_series.to_frame(name="foo").resample("20min", group_keys=False)
    result = grouped["foo"].apply(lambda x: x)
    tm.assert_series_equal(result, _test_series.rename("foo"))

