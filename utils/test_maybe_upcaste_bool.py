
def test_maybe_upcaste_bool():
    # GH#36712
    dtype = np.bool_
    na_value = na_values[dtype]
    arr = np.array([True, False, na_value], dtype="uint8").view(dtype)
    result = _maybe_upcast(arr, use_dtype_backend=True)

    expected_mask = np.array([False, False, True])
    expected = BooleanArray(arr, mask=expected_mask)
    tm.assert_extension_array_equal(result, expected)

