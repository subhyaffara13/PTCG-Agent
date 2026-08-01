
def test_floordiv_by_int_zero_no_mask(any_int_ea_dtype):
    # GH 48223: Aligns with non-masked floordiv
    # but differs from numpy
    # https://github.com/pandas-dev/pandas/issues/30188#issuecomment-564452740
    ser = pd.Series([0, 1], dtype=any_int_ea_dtype)
    result = 1 // ser
    expected = pd.Series([np.inf, 1.0], dtype="Float64")
    tm.assert_series_equal(result, expected)

    ser_non_nullable = ser.astype(ser.dtype.numpy_dtype)
    result = 1 // ser_non_nullable
    expected = expected.astype(np.float64)
    tm.assert_series_equal(result, expected)

