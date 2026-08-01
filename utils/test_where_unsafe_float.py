
def test_where_unsafe_float(float_numpy_dtype):
    s = Series(np.arange(10), dtype=float_numpy_dtype)
    mask = s < 5

    s[mask] = range(2, 7)
    data = list(range(2, 7)) + list(range(5, 10))
    expected = Series(data, dtype=float_numpy_dtype)

    tm.assert_series_equal(s, expected)

