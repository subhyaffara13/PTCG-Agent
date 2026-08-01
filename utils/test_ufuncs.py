
def test_ufuncs(ufunc, arr):
    result = ufunc(arr)
    fill_value = ufunc(arr.fill_value)
    expected = SparseArray(ufunc(np.asarray(arr)), fill_value=fill_value)
    tm.assert_sp_array_equal(result, expected)

