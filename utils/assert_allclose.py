
def assert_allclose(
    actual: Any,
    expected: Any,
    rtol: float | None = None,
    atol: float | None = None,
    equal_nan: bool = True,
    msg: str = "",
) -> None:
    """
    .. warning::

       :func:`torch.testing.assert_allclose` is deprecated since ``1.12`` and will be removed in a future release.
       Please use :func:`torch.testing.assert_close` instead. You can find detailed upgrade instructions
       `here <https://github.com/pytorch/pytorch/issues/61844>`_.
    """
    if not isinstance(actual, torch.Tensor):
        actual = torch.tensor(actual)
    if not isinstance(expected, torch.Tensor):
        expected = torch.tensor(expected, dtype=actual.dtype)

    if rtol is None and atol is None:
        rtol, atol = default_tolerances(
            actual,
            expected,
            dtype_precisions={
                torch.float16: (1e-3, 1e-3),
                torch.float32: (1e-4, 1e-5),
                torch.float64: (1e-5, 1e-8),
            },
        )

    torch.testing.assert_close(
        actual,
        expected,
        rtol=rtol,
        atol=atol,
        equal_nan=equal_nan,
        check_device=True,
        check_dtype=False,
        check_stride=False,
        msg=msg or None,
    )


def assert_allclose(
    actual,
    desired,
    rtol=1e-7,
    atol=0,
    equal_nan=True,
    err_msg="",
    verbose=True,
    check_dtype=False,
):
    """
    Raises an AssertionError if two objects are not equal up to desired
    tolerance.

    Given two array_like objects, check that their shapes and all elements
    are equal (but see the Notes for the special handling of a scalar). An
    exception is raised if the shapes mismatch or any values conflict. In
    contrast to the standard usage in numpy, NaNs are compared like numbers,
    no assertion is raised if both objects have NaNs in the same positions.

    The test is equivalent to ``allclose(actual, desired, rtol, atol)`` (note
    that ``allclose`` has different default values). It compares the difference
    between `actual` and `desired` to ``atol + rtol * abs(desired)``.

    .. versionadded:: 1.5.0

    Parameters
    ----------
    actual : array_like
        Array obtained.
    desired : array_like
        Array desired.
    rtol : float, optional
        Relative tolerance.
    atol : float, optional
        Absolute tolerance.
    equal_nan : bool, optional.
        If True, NaNs will compare equal.
    err_msg : str, optional
        The error message to be printed in case of failure.
    verbose : bool, optional
        If True, the conflicting values are appended to the error message.

    Raises
    ------
    AssertionError
        If actual and desired are not equal up to specified precision.

    See Also
    --------
    assert_array_almost_equal_nulp, assert_array_max_ulp

    Notes
    -----
    When one of `actual` and `desired` is a scalar and the other is
    array_like, the function checks that each element of the array_like
    object is equal to the scalar.

    Examples
    --------
    >>> x = [1e-5, 1e-3, 1e-1]
    >>> y = np.arccos(np.cos(x))
    >>> np.testing.assert_allclose(x, y, rtol=1e-5, atol=0)

    """
    __tracebackhide__ = True  # Hide traceback for py.test

    def compare(x, y):
        return np.isclose(x, y, rtol=rtol, atol=atol, equal_nan=equal_nan)

    actual, desired = asanyarray(actual), asanyarray(desired)
    header = f"Not equal to tolerance rtol={rtol:g}, atol={atol:g}"

    if check_dtype:
        if actual.dtype != desired.dtype:
            raise AssertionError(f"dtype mismatch: {actual.dtype} != {desired.dtype}")

    assert_array_compare(
        compare,
        actual,
        desired,
        err_msg=str(err_msg),
        verbose=verbose,
        header=header,
        equal_nan=equal_nan,
    )


def assert_allclose(actual, desired, rtol=1e-7, atol=0, equal_nan=True,
                    err_msg='', verbose=True, *, strict=False):
    """
    Raises an AssertionError if two objects are not equal up to desired
    tolerance.

    Given two array_like objects, check that their shapes and all elements
    are equal (but see the Notes for the special handling of a scalar). An
    exception is raised if the shapes mismatch or any values conflict. In
    contrast to the standard usage in numpy, NaNs are compared like numbers,
    no assertion is raised if both objects have NaNs in the same positions.

    The test is equivalent to ``allclose(actual, desired, rtol, atol)``,
    except that it is stricter: it doesn't broadcast its operands, and has
    tighter default tolerance values. It compares the difference between
    `actual` and `desired` to ``atol + rtol * abs(desired)``.

    Parameters
    ----------
    actual : array_like
        Array obtained.
    desired : array_like
        Array desired.
    rtol : float, optional
        Relative tolerance.
    atol : float | np.timedelta64, optional
        Absolute tolerance.
    equal_nan : bool, optional.
        If True, NaNs will compare equal.
    err_msg : str, optional
        The error message to be printed in case of failure.
    verbose : bool, optional
        If True, the conflicting values are appended to the error message.
    strict : bool, optional
        If True, raise an ``AssertionError`` when either the shape or the data
        type of the arguments does not match. The special handling of scalars
        mentioned in the Notes section is disabled.

        .. versionadded:: 2.0.0

    Raises
    ------
    AssertionError
        If actual and desired are not equal up to specified precision.

    See Also
    --------
    assert_array_almost_equal_nulp, assert_array_max_ulp

    Notes
    -----
    When one of `actual` and `desired` is a scalar and the other is array_like, the
    function performs the comparison as if the scalar were broadcasted to the shape
    of the array. Note that empty arrays are therefore considered equal to scalars.
    This behaviour can be disabled by setting ``strict==True``.

    Examples
    --------
    >>> x = [1e-5, 1e-3, 1e-1]
    >>> y = np.arccos(np.cos(x))
    >>> np.testing.assert_allclose(x, y, rtol=1e-5, atol=0)

    As mentioned in the Notes section, `assert_allclose` has special
    handling for scalars. Here, the test checks that the value of `numpy.sin`
    is nearly zero at integer multiples of π.

    >>> x = np.arange(3) * np.pi
    >>> np.testing.assert_allclose(np.sin(x), 0, atol=1e-15)

    Use `strict` to raise an ``AssertionError`` when comparing an array
    with one or more dimensions against a scalar.

    >>> np.testing.assert_allclose(np.sin(x), 0, atol=1e-15, strict=True)
    Traceback (most recent call last):
        ...
    AssertionError:
    Not equal to tolerance rtol=1e-07, atol=1e-15
    <BLANKLINE>
    (shapes (3,), () mismatch)
     ACTUAL: array([ 0.000000e+00,  1.224647e-16, -2.449294e-16])
     DESIRED: array(0)

    The `strict` parameter also ensures that the array data types match:

    >>> y = np.zeros(3, dtype=np.float32)
    >>> np.testing.assert_allclose(np.sin(x), y, atol=1e-15, strict=True)
    Traceback (most recent call last):
        ...
    AssertionError:
    Not equal to tolerance rtol=1e-07, atol=1e-15
    <BLANKLINE>
    (dtypes float64, float32 mismatch)
     ACTUAL: array([ 0.000000e+00,  1.224647e-16, -2.449294e-16])
     DESIRED: array([0., 0., 0.], dtype=float32)

    """
    __tracebackhide__ = True  # Hide traceback for py.test
    import numpy as np

    def compare(x, y):
        return np._core.numeric.isclose(x, y, rtol=rtol, atol=atol,
                                       equal_nan=equal_nan)

    actual, desired = np.asanyarray(actual), np.asanyarray(desired)
    if isinstance(atol, np.timedelta64):
        atol_str = str(atol)
    else:
        atol_str = f"{atol:g}"
    header = f'Not equal to tolerance rtol={rtol:g}, atol={atol_str}'
    assert_array_compare(compare, actual, desired, err_msg=str(err_msg),
                         verbose=verbose, header=header, equal_nan=equal_nan,
                         strict=strict)

