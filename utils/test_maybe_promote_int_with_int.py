
def test_maybe_promote_int_with_int(dtype, fill_value, expected_dtype):
    dtype = np.dtype(dtype)
    expected_dtype = np.dtype(expected_dtype)

    # output is not a generic int, but corresponds to expected_dtype
    exp_val_for_scalar = np.array([fill_value], dtype=expected_dtype)[0]

    _check_promote(dtype, fill_value, expected_dtype, exp_val_for_scalar)

