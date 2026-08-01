
def test_ignore_error():
    ser = Series([1, -3.14, "apple"])
    result = to_numeric(ser, errors="coerce")

    expected = Series([1, -3.14, np.nan])
    tm.assert_series_equal(result, expected)

