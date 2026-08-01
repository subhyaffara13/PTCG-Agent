
def xp_assert_less(actual, desired, *, check_namespace=True, check_dtype=True,
                   check_shape=True, check_0d=True, err_msg='', verbose=True, xp=None):
    __tracebackhide__ = True  # Hide traceback for py.test

    actual, desired, xp = _strict_check(
        actual, desired, xp, check_namespace=check_namespace,
        check_dtype=check_dtype, check_shape=check_shape,
        check_0d=check_0d
    )

    _assert_less(actual, desired, err_msg=err_msg, verbose=verbose, xp=xp)


def xp_assert_less(actual, desired, *, check_0d=False, **kwargs):
    # as for xp_assert_equal
    __tracebackhide__ = True

    if not check_0d:
        _check_scalar(actual, desired, **kwargs)
    return xp_assert_less_base(actual, desired, check_0d=check_0d, **kwargs)


def xp_assert_less(
    x: Array,
    y: Array,
    *,
    err_msg: str = "",
    check_dtype: bool = True,
    check_shape: bool = True,
    check_scalar: bool = False,
) -> None:
    """
    Array-API compatible version of `np.testing.assert_array_less`.

    Parameters
    ----------
    x, y : Array
        The arrays to compare according to ``x < y`` (elementwise).
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
    xp = _check_ns_shape_dtype(x, y, check_dtype, check_shape, check_scalar)
    if not _is_materializable(x):
        return
    x_np = as_numpy_array(x, xp=xp)
    y_np = as_numpy_array(y, xp=xp)
    np.testing.assert_array_less(x_np, y_np, err_msg=err_msg)

