
def test_as_unit(dtype):
    # GH 52284
    ser = pd.Series([1000, None], dtype=dtype)
    result = ser.dt.as_unit("ns")
    expected = ser.astype(dtype.replace("ms", "ns"))
    tm.assert_series_equal(result, expected)

