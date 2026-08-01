
def test_astype_nansafe_copy_false(any_int_numpy_dtype):
    # GH#34457 use astype, not view
    arr = np.array([1, 2, 3], dtype=any_int_numpy_dtype)

    dtype = np.dtype("float64")
    result = astype_array(arr, dtype, copy=False)

    expected = np.array([1.0, 2.0, 3.0], dtype=dtype)
    tm.assert_numpy_array_equal(result, expected)

