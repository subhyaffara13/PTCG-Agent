
def test_ufuncs_single_float(ufunc, using_nan_is_na):
    a = pd.array([1.0, 0.2, 3.0, pd.NA], dtype="Float64")
    with np.errstate(invalid="ignore"):
        result = ufunc(a)
        np_res = ufunc(a.astype(float))
        np_res = np_res.astype(object)
        np_res[a.isna()] = pd.NA
        expected = pd.array(np_res, dtype="Float64")
    tm.assert_extension_array_equal(result, expected)

    s = pd.Series(a)
    with np.errstate(invalid="ignore"):
        result = ufunc(s)
        np_res = ufunc(s.astype(float))
        np_res = np_res.astype(object)
        np_res[a.isna()] = pd.NA
        expected = pd.Series(np_res, dtype="Float64")
    tm.assert_series_equal(result, expected)


def test_ufuncs_single_float(ufunc, using_nan_is_na):
    a = pd.array([1, 2, -3, pd.NA], dtype="Int64")
    with np.errstate(invalid="ignore"):
        result = ufunc(a)
        if using_nan_is_na:
            expected = pd.array(ufunc(a.astype(float)), dtype="Float64")
        else:
            expected = FloatingArray(ufunc(a.astype(float)), mask=a._mask)
    tm.assert_extension_array_equal(result, expected)

    s = pd.Series(a)
    with np.errstate(invalid="ignore"):
        result = ufunc(s)
    expected = pd.Series(expected)
    tm.assert_series_equal(result, expected)

