
def test_series_from_string_array(dtype):
    arr = pa.array("the quick brown fox".split())
    ser = pd.Series(arr, dtype=dtype)
    expected = pd.Series(ArrowExtensionArray(arr), dtype=dtype)
    tm.assert_series_equal(ser, expected)

