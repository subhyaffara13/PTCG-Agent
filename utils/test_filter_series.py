
def test_filter_series():
    s = Series([1, 3, 20, 5, 22, 24, 7])
    expected_odd = Series([1, 3, 5, 7], index=[0, 1, 3, 6])
    expected_even = Series([20, 22, 24], index=[2, 4, 5])
    grouper = s.apply(lambda x: x % 2)
    grouped = s.groupby(grouper)
    tm.assert_series_equal(grouped.filter(lambda x: x.mean() < 10), expected_odd)
    tm.assert_series_equal(grouped.filter(lambda x: x.mean() > 10), expected_even)
    # Test dropna=False.
    tm.assert_series_equal(
        grouped.filter(lambda x: x.mean() < 10, dropna=False),
        expected_odd.reindex(s.index),
    )
    tm.assert_series_equal(
        grouped.filter(lambda x: x.mean() > 10, dropna=False),
        expected_even.reindex(s.index),
    )

