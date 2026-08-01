
def test_ufuncs_single_int(ufunc, using_nan_is_na):
    a = pd.array([1, 2, -3, pd.NA], dtype="Int64")
    result = ufunc(a)
    np_res = ufunc(a.astype(float))
    np_res = np_res.astype(object)
    np_res[-1] = pd.NA
    expected = pd.array(np_res, dtype="Int64")
    tm.assert_extension_array_equal(result, expected)

    s = pd.Series(a)
    result = ufunc(s)
    np_res = ufunc(a.astype(float))
    np_res = np_res.astype(object)
    np_res[-1] = pd.NA
    expected = pd.Series(pd.array(np_res, dtype="Int64"))
    tm.assert_series_equal(result, expected)

