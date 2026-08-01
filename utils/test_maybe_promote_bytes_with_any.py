
def test_maybe_promote_bytes_with_any(bytes_dtype, any_numpy_dtype):
    dtype = np.dtype(bytes_dtype)
    fill_dtype = np.dtype(any_numpy_dtype)

    # create array of given dtype; casts "1" to correct dtype
    fill_value = np.array([1], dtype=fill_dtype)[0]

    # we never use bytes dtype internally, always promote to object
    expected_dtype = np.dtype(np.object_)
    exp_val_for_scalar = fill_value

    _check_promote(dtype, fill_value, expected_dtype, exp_val_for_scalar)

