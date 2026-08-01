
def test_filter_out_no_groups():
    s = Series([1, 3, 20, 5, 22, 24, 7])
    grouper = s.apply(lambda x: x % 2)
    grouped = s.groupby(grouper)
    filtered = grouped.filter(lambda x: x.mean() > 0)
    tm.assert_series_equal(filtered, s)

