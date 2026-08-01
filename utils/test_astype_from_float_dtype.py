
def test_astype_from_float_dtype(float_dtype, dtype):
    # https://github.com/pandas-dev/pandas/issues/36451
    ser = pd.Series([0.1], dtype=float_dtype)
    result = ser.astype(dtype)
    expected = pd.Series(["0.1"], dtype=dtype)
    tm.assert_series_equal(result, expected)

