
def test_single_bin(data, length):
    # see gh-14652, gh-15428
    ser = Series([data] * length)
    result = cut(ser, 1, labels=False)

    expected = Series([0] * length, dtype=np.intp)
    tm.assert_series_equal(result, expected)

