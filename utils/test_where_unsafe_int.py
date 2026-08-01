
def test_where_unsafe_int(any_signed_int_numpy_dtype):
    s = Series(np.arange(10), dtype=any_signed_int_numpy_dtype)
    mask = s < 5

    s[mask] = range(2, 7)
    expected = Series(
        list(range(2, 7)) + list(range(5, 10)),
        dtype=any_signed_int_numpy_dtype,
    )

    tm.assert_series_equal(s, expected)

