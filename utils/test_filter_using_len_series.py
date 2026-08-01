
def test_filter_using_len_series():
    # GH 4447
    s = Series(list("aabbbbcc"), name="B")
    grouped = s.groupby(s)
    actual = grouped.filter(lambda x: len(x) > 2)
    expected = Series(4 * ["b"], index=range(2, 6), name="B")
    tm.assert_series_equal(actual, expected)

    actual = grouped.filter(lambda x: len(x) > 4)
    expected = s[[]]
    tm.assert_series_equal(actual, expected)

