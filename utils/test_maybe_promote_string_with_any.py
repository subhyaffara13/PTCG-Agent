
def test_maybe_promote_string_with_any(string_dtype, any_numpy_dtype):
    dtype = np.dtype(string_dtype)
    fill_dtype = np.dtype(any_numpy_dtype)

    # create array of given dtype; casts "1" to correct dtype
    fill_value = np.array([1], dtype=fill_dtype)[0]

    # filling string with anything casts to object
    expected_dtype = np.dtype(object)
    exp_val_for_scalar = fill_value

    _check_promote(dtype, fill_value, expected_dtype, exp_val_for_scalar)

