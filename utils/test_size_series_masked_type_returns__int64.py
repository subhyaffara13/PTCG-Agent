
def test_size_series_masked_type_returns_Int64(dtype):
    # GH 54132
    ser = Series([1, 1, 1], index=["a", "a", "b"], dtype=dtype)
    result = ser.groupby(level=0).size()
    expected = Series([2, 1], dtype="Int64", index=["a", "b"])
    tm.assert_series_equal(result, expected)

