
def test_single_quantile(data, start, end, length, labels):
    # see gh-15431
    ser = Series([data] * length)
    result = qcut(ser, 1, labels=labels)

    if labels is None:
        intervals = IntervalIndex([Interval(start, end)] * length, closed="right")
        expected = Series(intervals).astype(CategoricalDtype(ordered=True))
    else:
        expected = Series([0] * length, dtype=np.intp)

    tm.assert_series_equal(result, expected)

