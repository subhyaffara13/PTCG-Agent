
def test_maybe_promote_any_with_bytes(any_numpy_dtype):
    dtype = np.dtype(any_numpy_dtype)

    # create array of given dtype
    fill_value = b"abc"

    # we never use bytes dtype internally, always promote to object
    expected_dtype = np.dtype(np.object_)
    # output is not a generic bytes, but corresponds to expected_dtype
    exp_val_for_scalar = np.array([fill_value], dtype=expected_dtype)[0]

    _check_promote(dtype, fill_value, expected_dtype, exp_val_for_scalar)

