
def test_maybe_promote_any_numpy_dtype_with_datetimetz(
    any_numpy_dtype, tz_aware_fixture, fill_value
):
    dtype = np.dtype(any_numpy_dtype)
    fill_dtype = DatetimeTZDtype(tz=tz_aware_fixture)

    fill_value = pd.Series([fill_value], dtype=fill_dtype)[0]

    # filling any numpy dtype with datetimetz casts to object
    expected_dtype = np.dtype(object)
    exp_val_for_scalar = fill_value

    _check_promote(dtype, fill_value, expected_dtype, exp_val_for_scalar)

