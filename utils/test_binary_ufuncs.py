
def test_binary_ufuncs(ufunc, a, b):
    # can't say anything about fill value here.
    result = ufunc(a, b)
    expected = ufunc(np.asarray(a), np.asarray(b))
    assert isinstance(result, SparseArray)
    tm.assert_numpy_array_equal(np.asarray(result), expected)

