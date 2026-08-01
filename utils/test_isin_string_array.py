
def test_isin_string_array(dtype, dtype2):
    s = pd.Series(["a", "b", None], dtype=dtype)

    result = s.isin(pd.array(["a", "c"], dtype=dtype2))
    expected = pd.Series([True, False, False])
    tm.assert_series_equal(result, expected)

    result = s.isin(pd.array(["a", None], dtype=dtype2))
    expected = pd.Series([True, False, True])
    tm.assert_series_equal(result, expected)

