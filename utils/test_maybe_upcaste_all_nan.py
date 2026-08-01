
def test_maybe_upcaste_all_nan():
    # GH#36712
    dtype = np.int64
    na_value = na_values[dtype]
    arr = np.array([na_value, na_value], dtype=dtype)
    result = _maybe_upcast(arr, use_dtype_backend=True)

    expected_mask = np.array([True, True])
    expected = IntegerArray(arr, mask=expected_mask)
    tm.assert_extension_array_equal(result, expected)

