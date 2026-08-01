
def test_ufuncs_binary_float(ufunc, using_nan_is_na):
    # two FloatingArrays
    a = pd.array([1, 0.2, -3, pd.NA], dtype="Float64")
    result = ufunc(a, a)
    np_res = ufunc(a.astype(float), a.astype(float))
    np_res = np_res.astype(object)
    np_res[a.isna()] = pd.NA
    expected = pd.array(np_res, dtype="Float64")
    tm.assert_extension_array_equal(result, expected)

    # FloatingArray with numpy array
    arr = np.array([1, 2, 3, 4])
    result = ufunc(a, arr)
    np_res = ufunc(a.astype(float), arr)
    np_res = np_res.astype(object)
    np_res[a.isna()] = pd.NA
    expected = pd.array(np_res, dtype="Float64")
    tm.assert_extension_array_equal(result, expected)

    result = ufunc(arr, a)
    np_res = ufunc(arr, a.astype(float))
    np_res = np_res.astype(object)
    np_res[a.isna()] = pd.NA
    expected = pd.array(np_res, dtype="Float64")
    tm.assert_extension_array_equal(result, expected)

    # FloatingArray with scalar
    result = ufunc(a, 1)
    np_res = ufunc(a.astype(float), 1)
    np_res = np_res.astype(object)
    np_res[a.isna()] = pd.NA
    expected = pd.array(np_res, dtype="Float64")
    tm.assert_extension_array_equal(result, expected)

    result = ufunc(1, a)
    np_res = ufunc(1, a.astype(float))
    np_res = np_res.astype(object)
    np_res[a.isna()] = pd.NA
    expected = pd.array(np_res, dtype="Float64")
    tm.assert_extension_array_equal(result, expected)

