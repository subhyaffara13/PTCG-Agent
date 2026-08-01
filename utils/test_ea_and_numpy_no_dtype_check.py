
def test_ea_and_numpy_no_dtype_check(val, check_exact, dtype):
    # GH#56651
    left = Series([1, 2, val], dtype=dtype)
    right = Series(pd.array([1, 2, val]))
    tm.assert_series_equal(left, right, check_dtype=False, check_exact=check_exact)

