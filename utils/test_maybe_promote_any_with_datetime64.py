
def test_maybe_promote_any_with_datetime64(any_numpy_dtype, fill_value):
    dtype = np.dtype(any_numpy_dtype)

    # filling datetime with anything but datetime casts to object
    if dtype.kind == "M":
        expected_dtype = dtype
        # for datetime dtypes, scalar values get cast to pd.Timestamp.value
        exp_val_for_scalar = pd.Timestamp(fill_value).to_datetime64()
    else:
        expected_dtype = np.dtype(object)
        exp_val_for_scalar = fill_value

    if type(fill_value) is datetime.date and dtype.kind == "M":
        # Casting date to dt64 is deprecated, in 2.0 enforced to cast to object
        expected_dtype = np.dtype(object)
        exp_val_for_scalar = fill_value

    _check_promote(dtype, fill_value, expected_dtype, exp_val_for_scalar)

