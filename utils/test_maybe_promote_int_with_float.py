
def test_maybe_promote_int_with_float(any_int_numpy_dtype, float_numpy_dtype):
    dtype = np.dtype(any_int_numpy_dtype)
    fill_dtype = np.dtype(float_numpy_dtype)

    # create array of given dtype; casts "1" to correct dtype
    fill_value = np.array([1], dtype=fill_dtype)[0]

    # filling int with float always upcasts to float64
    expected_dtype = np.float64
    # fill_value can be different float type
    exp_val_for_scalar = np.float64(fill_value)

    _check_promote(dtype, fill_value, expected_dtype, exp_val_for_scalar)

