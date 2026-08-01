
def xp_assert_equal(actual, desired, *, check_namespace=True, check_dtype=True,
                    check_shape=True, check_0d=True, err_msg='', xp=None):
    __tracebackhide__ = True  # Hide traceback for py.test

    actual, desired, xp = _strict_check(
        actual, desired, xp, check_namespace=check_namespace,
        check_dtype=check_dtype, check_shape=check_shape,
        check_0d=check_0d
    )

    if is_cupy(xp):
        return xp.testing.assert_array_equal(actual, desired, err_msg=err_msg)
    elif is_torch(xp):
        # PyTorch recommends using `rtol=0, atol=0` like this
        # to test for exact equality
        err_msg = None if err_msg == '' else err_msg
        return xp.testing.assert_close(actual, desired, rtol=0, atol=0, equal_nan=True,
                                       check_dtype=False, msg=err_msg)
    # JAX uses `np.testing`
    return np.testing.assert_array_equal(actual, desired, err_msg=err_msg)


def xp_assert_equal(actual, desired, *, check_0d=False, **kwargs):
    # in contrast to xp_assert_equal_base, this defaults to check_0d=False,
    # but will do an extra check in that case, which forbids 0d-arrays for `actual`
    __tracebackhide__ = True  # Hide traceback for py.test

    # array-ness (check_0d == True) is taken care of by the *_base functions
    if not check_0d:
        _check_scalar(actual, desired, **kwargs)
    return xp_assert_equal_base(actual, desired, check_0d=check_0d, **kwargs)


def xp_assert_equal(
    actual: Array,
    desired: Array,
    *,
    err_msg: str = "",
    check_dtype: bool = True,
    check_shape: bool = True,
    check_scalar: bool = False,
) -> None:
    """
    Array-API compatible version of `np.testing.assert_array_equal`.

    Parameters
    ----------
    actual : Array
        The array produced by the tested function.
    desired : Array
        The expected array (typically hardcoded).
    err_msg : str, optional
        Error message to display on failure.
    check_dtype, check_shape : bool, default: True
        Whether to check agreement between actual and desired dtypes and shapes
    check_scalar : bool, default: False
        NumPy only: whether to check agreement between actual and desired types -
        0d array vs scalar.

    See Also
    --------
    xp_assert_close : Similar function for inexact equality checks.
    numpy.testing.assert_array_equal : Similar function for NumPy arrays.
    """
    xp = _check_ns_shape_dtype(actual, desired, check_dtype, check_shape, check_scalar)
    if not _is_materializable(actual):
        return
    actual_np = as_numpy_array(actual, xp=xp)
    desired_np = as_numpy_array(desired, xp=xp)
    np.testing.assert_array_equal(actual_np, desired_np, err_msg=err_msg)

