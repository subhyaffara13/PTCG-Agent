
def test_astype_specific_casting(dtype):
    s = pd.Series([1, 2, 3], dtype="Int64")
    result = s.astype(dtype)
    expected = pd.Series([1, 2, 3], dtype=dtype)
    tm.assert_series_equal(result, expected)

    s = pd.Series([1, 2, 3, None], dtype="Int64")
    result = s.astype(dtype)
    expected = pd.Series([1, 2, 3, None], dtype=dtype)
    tm.assert_series_equal(result, expected)

