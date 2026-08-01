
def test_getitem_assignment_series_alignment():
    # https://github.com/pandas-dev/pandas/issues/37427
    # with getitem, when assigning with a Series, it is not first aligned
    ser = Series(range(10))
    idx = np.array([2, 4, 9])
    ser[idx] = Series([10, 11, 12])
    expected = Series([0, 1, 10, 3, 11, 5, 6, 7, 8, 12])
    tm.assert_series_equal(ser, expected)

