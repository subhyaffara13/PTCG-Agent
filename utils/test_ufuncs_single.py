
def test_ufuncs_single(ufunc, using_nan_is_na):
    a = pd.array([1, 2, -3, pd.NA], dtype="Float64")
    result = ufunc(a)
    np_res = ufunc(a.astype(float))
    np_res = np_res.astype(object)
    np_res[a.isna()] = pd.NA
    expected = pd.array(np_res, dtype="Float64")
    tm.assert_extension_array_equal(result, expected)

    s = pd.Series(a)
    result = ufunc(s)
    expected = pd.Series(expected)
    tm.assert_series_equal(result, expected)

