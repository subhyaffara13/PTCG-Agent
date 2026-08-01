
def test_mode_nullable_dtype_edge_case(any_numeric_ea_dtype):
    # GH##58926
    ser = Series([1, 2, 3, 1], dtype=any_numeric_ea_dtype)
    result = ser.mode(dropna=False)
    expected = Series([1], dtype=any_numeric_ea_dtype)
    tm.assert_series_equal(result, expected)

    ser2 = Series([1, 1, 2, 3, pd.NA], dtype=any_numeric_ea_dtype)
    result = ser2.mode(dropna=False)
    expected = Series([1], dtype=any_numeric_ea_dtype)
    tm.assert_series_equal(result, expected)

    ser3 = Series([1, pd.NA, pd.NA], dtype=any_numeric_ea_dtype)
    result = ser3.mode(dropna=False)
    expected = Series([pd.NA], dtype=any_numeric_ea_dtype)
    tm.assert_series_equal(result, expected)

    ser4 = Series([1, 1, pd.NA, pd.NA], dtype=any_numeric_ea_dtype)
    result = ser4.mode(dropna=False)
    expected = Series([1, pd.NA], dtype=any_numeric_ea_dtype)
    tm.assert_series_equal(result, expected)

