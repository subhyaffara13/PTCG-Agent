
def test_searchsorted_different_argument_classes(listlike_box):
    # https://github.com/pandas-dev/pandas/issues/32762
    values = IntervalIndex([Interval(0, 1), Interval(1, 2)])
    result = values.searchsorted(listlike_box(values))
    expected = np.array([0, 1], dtype=result.dtype)
    tm.assert_numpy_array_equal(result, expected)

    result = values._data.searchsorted(listlike_box(values))
    tm.assert_numpy_array_equal(result, expected)

