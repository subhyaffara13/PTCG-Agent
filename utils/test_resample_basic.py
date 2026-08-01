
def test_resample_basic(closed, expected, unit):
    index = date_range("1/1/2000 00:00:00", "1/1/2000 00:13:00", freq="Min")
    s = Series(range(len(index)), index=index)
    s.index.name = "index"
    s.index = s.index.as_unit(unit)
    expected = expected(s)
    expected.index = expected.index.as_unit(unit)
    result = s.resample("5min", closed=closed, label="right").mean()
    tm.assert_series_equal(result, expected)

