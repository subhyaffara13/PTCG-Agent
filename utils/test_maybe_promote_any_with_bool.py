
def test_maybe_promote_any_with_bool(any_numpy_dtype):
    dtype = np.dtype(any_numpy_dtype)
    fill_value = True

    # filling anything but bool with bool casts to object
    expected_dtype = np.dtype(object) if dtype != bool else dtype
    # output is not a generic bool, but corresponds to expected_dtype
    exp_val_for_scalar = np.array([fill_value], dtype=expected_dtype)[0]

    _check_promote(dtype, fill_value, expected_dtype, exp_val_for_scalar)

