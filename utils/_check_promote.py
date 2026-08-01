
def _check_promote(dtype, fill_value, expected_dtype, exp_val_for_scalar=None):
    """
    Auxiliary function to unify testing of scalar/array promotion.

    Parameters
    ----------
    dtype : dtype
        The value to pass on as the first argument to maybe_promote.
    fill_value : scalar
        The value to pass on as the second argument to maybe_promote as
        a scalar.
    expected_dtype : dtype
        The expected dtype returned by maybe_promote (by design this is the
        same regardless of whether fill_value was passed as a scalar or in an
        array!).
    exp_val_for_scalar : scalar
        The expected value for the (potentially upcast) fill_value returned by
        maybe_promote.
    """
    assert is_scalar(fill_value)

    # here, we pass on fill_value as a scalar directly; the expected value
    # returned from maybe_promote is fill_value, potentially upcast to the
    # returned dtype.
    result_dtype, result_fill_value = maybe_promote(dtype, fill_value)
    expected_fill_value = exp_val_for_scalar

    assert result_dtype == expected_dtype
    _assert_match(result_fill_value, expected_fill_value)

