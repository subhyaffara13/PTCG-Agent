
def test_maybe_promote_any_with_timedelta64(any_numpy_dtype, fill_value):
    dtype = np.dtype(any_numpy_dtype)

    # filling anything but timedelta with timedelta casts to object
    if dtype.kind == "m":
        expected_dtype = dtype
        # for timedelta dtypes, scalar values get cast to pd.Timedelta.value
        exp_val_for_scalar = pd.Timedelta(fill_value).to_timedelta64()
    else:
        expected_dtype = np.dtype(object)
        exp_val_for_scalar = fill_value

    _check_promote(dtype, fill_value, expected_dtype, exp_val_for_scalar)

