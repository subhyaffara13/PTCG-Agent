
def xp_assert_close(actual, desired, *, rtol=None, atol=0, check_namespace=True,
                    check_dtype=True, check_shape=True, check_0d=True,
                    err_msg='', xp=None):
    __tracebackhide__ = True  # Hide traceback for py.test

    actual, desired, xp = _strict_check(
        actual, desired, xp,
        check_namespace=check_namespace, check_dtype=check_dtype,
        check_shape=check_shape, check_0d=check_0d
    )

    floating = xp.isdtype(actual.dtype, ('real floating', 'complex floating'))
    if rtol is None and floating:
        # multiplier of 4 is used as for `np.float64` this puts the default `rtol`
        # roughly half way between sqrt(eps) and the default for
        # `numpy.testing.assert_allclose`, 1e-7
        rtol = xp.finfo(actual.dtype).eps**0.5 * 4
    elif rtol is None:
        rtol = 1e-7

    if is_cupy(xp):
        return xp.testing.assert_allclose(actual, desired, rtol=rtol,
                                          atol=atol, err_msg=err_msg)
    elif is_torch(xp):
        err_msg = None if err_msg == '' else err_msg
        return xp.testing.assert_close(actual, desired, rtol=rtol, atol=atol,
                                       equal_nan=True, check_dtype=False, msg=err_msg)
    # JAX uses `np.testing`
    return np.testing.assert_allclose(actual, desired, rtol=rtol,
                                      atol=atol, err_msg=err_msg)


def xp_assert_close(actual, desired, *, check_0d=False, **kwargs):
    # as for xp_assert_equal
    __tracebackhide__ = True

    if not check_0d:
        _check_scalar(actual, desired, **kwargs)
    return xp_assert_close_base(actual, desired, check_0d=check_0d, **kwargs)


def xp_assert_close(
    actual: Array,
    desired: Array,
    *,
    rtol: float | None = None,
    atol: float = 0,
    err_msg: str = "",
    check_dtype: bool = True,
    check_shape: bool = True,
    check_scalar: bool = False,
) -> None:
    """
    Array-API compatible version of `np.testing.assert_allclose`.

    Parameters
    ----------
    actual : Array
        The array produced by the tested function.
    desired : Array
        The expected array (typically hardcoded).
    rtol : float, optional
        Relative tolerance. Default: dtype-dependent.
    atol : float, optional
        Absolute tolerance. Default: 0.
    err_msg : str, optional
        Error message to display on failure.
    check_dtype, check_shape : bool, default: True
        Whether to check agreement between actual and desired dtypes and shapes
    check_scalar : bool, default: False
        NumPy only: whether to check agreement between actual and desired types -
        0d array vs scalar.

    See Also
    --------
    xp_assert_equal : Similar function for exact equality checks.
    isclose : Public function for checking closeness.
    numpy.testing.assert_allclose : Similar function for NumPy arrays.

    Notes
    -----
    The default `atol` and `rtol` differ from `xp.all(xpx.isclose(a, b))`.
    """
    xp = _check_ns_shape_dtype(actual, desired, check_dtype, check_shape, check_scalar)
    if not _is_materializable(actual):
        return

    if rtol is None:
        if xp.isdtype(actual.dtype, ("real floating", "complex floating")):
            # multiplier of 4 is used as for `np.float64` this puts the default `rtol`
            # roughly half way between sqrt(eps) and the default for
            # `numpy.testing.assert_allclose`, 1e-7
            rtol = xp.finfo(actual.dtype).eps ** 0.5 * 4
        else:
            rtol = 1e-7

    actual_np = as_numpy_array(actual, xp=xp)
    desired_np = as_numpy_array(desired, xp=xp)
    np.testing.assert_allclose(  # pyright: ignore[reportCallIssue]
        actual_np,
        desired_np,
        rtol=rtol,  # pyright: ignore[reportArgumentType]
        atol=atol,
        err_msg=err_msg,
    )

