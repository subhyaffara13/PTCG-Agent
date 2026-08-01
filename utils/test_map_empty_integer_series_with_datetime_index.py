
def test_map_empty_integer_series_with_datetime_index():
    # GH 21245
    s = Series([], index=date_range(start="2018-01-01", periods=0), dtype=int)
    result = s.map(lambda x: x)
    tm.assert_series_equal(result, s)

