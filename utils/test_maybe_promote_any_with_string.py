
def test_maybe_promote_any_with_string(any_numpy_dtype):
    dtype = np.dtype(any_numpy_dtype)

    # create array of given dtype
    fill_value = "abc"

    # filling anything with a string casts to object
    expected_dtype = np.dtype(object)
    exp_val_for_scalar = fill_value

    _check_promote(dtype, fill_value, expected_dtype, exp_val_for_scalar)

