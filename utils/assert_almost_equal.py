
def assert_almost_equal(actual, desired, decimal=7, err_msg="", verbose=True):
    """
    Raises an AssertionError if two items are not equal up to desired
    precision.

    .. note:: It is recommended to use one of `assert_allclose`,
              `assert_array_almost_equal_nulp` or `assert_array_max_ulp`
              instead of this function for more consistent floating point
              comparisons.

    The test verifies that the elements of `actual` and `desired` satisfy.

        ``abs(desired-actual) < float64(1.5 * 10**(-decimal))``

    That is a looser test than originally documented, but agrees with what the
    actual implementation in `assert_array_almost_equal` did up to rounding
    vagaries. An exception is raised at conflicting values. For ndarrays this
    delegates to assert_array_almost_equal

    Parameters
    ----------
    actual : array_like
        The object to check.
    desired : array_like
        The expected object.
    decimal : int, optional
        Desired precision, default is 7.
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
    assert_allclose: Compare two array_like objects for equality with desired
                     relative and/or absolute precision.
    assert_array_almost_equal_nulp, assert_array_max_ulp, assert_equal

    Examples
    --------
    >>> from torch._numpy.testing import assert_almost_equal
    >>> assert_almost_equal(2.3333333333333, 2.33333334)
    >>> assert_almost_equal(2.3333333333333, 2.33333334, decimal=10)
    Traceback (most recent call last):
        ...
    AssertionError:
    Arrays are not almost equal to 10 decimals
     ACTUAL: 2.3333333333333
     DESIRED: 2.33333334

    >>> assert_almost_equal(
    ...     np.array([1.0, 2.3333333333333]), np.array([1.0, 2.33333334]), decimal=9
    ... )
    Traceback (most recent call last):
        ...
    AssertionError:
    Arrays are not almost equal to 9 decimals
    <BLANKLINE>
    Mismatched elements: 1 / 2 (50%)
    Max absolute difference: 6.666699636781459e-09
    Max relative difference: 2.8571569790287484e-09
     x: torch.ndarray([1.0000, 2.3333], dtype=float64)
     y: torch.ndarray([1.0000, 2.3333], dtype=float64)

    """
    __tracebackhide__ = True  # Hide traceback for py.test
    from torch._numpy import imag, iscomplexobj, ndarray, real

    # Handle complex numbers: separate into real/imag to handle
    # nan/inf/negative zero correctly
    # XXX: catch ValueError for subclasses of ndarray where iscomplex fail
    try:
        usecomplex = iscomplexobj(actual) or iscomplexobj(desired)
    except ValueError:
        usecomplex = False

    def _build_err_msg():
        header = f"Arrays are not almost equal to {decimal:d} decimals"
        return build_err_msg([actual, desired], err_msg, verbose=verbose, header=header)

    if usecomplex:
        if iscomplexobj(actual):
            actualr = real(actual)
            actuali = imag(actual)
        else:
            actualr = actual
            actuali = 0
        if iscomplexobj(desired):
            desiredr = real(desired)
            desiredi = imag(desired)
        else:
            desiredr = desired
            desiredi = 0
        try:
            assert_almost_equal(actualr, desiredr, decimal=decimal)
            assert_almost_equal(actuali, desiredi, decimal=decimal)
        except AssertionError:
            raise AssertionError(_build_err_msg())  # noqa: B904

    if isinstance(actual, (ndarray, tuple, list)) or isinstance(
        desired, (ndarray, tuple, list)
    ):
        return assert_array_almost_equal(actual, desired, decimal, err_msg)
    try:
        # If one of desired/actual is not finite, handle it specially here:
        # check that both are nan if any is a nan, and test for equality
        # otherwise
        if not (gisfinite(desired) and gisfinite(actual)):
            if gisnan(desired) or gisnan(actual):
                if not (gisnan(desired) and gisnan(actual)):
                    raise AssertionError(_build_err_msg())
            else:
                if not desired == actual:
                    raise AssertionError(_build_err_msg())
            return
    except (NotImplementedError, TypeError):
        pass
    if abs(desired - actual) >= np.float64(1.5 * 10.0 ** (-decimal)):
        raise AssertionError(_build_err_msg())


def assert_almost_equal(actual, desired, decimal=7, *args, **kwds):
    """Backwards compatible replacement. In new code, use xp_assert_close instead.
    """
    rtol, atol = 0, 1.5*10**(-decimal)
    return xp_assert_close(actual, desired,
                           atol=atol, rtol=rtol, check_dtype=False, check_shape=False,
                           *args, **kwds)


def assert_almost_equal(actual, desired, decimal=7, **kwds):
    """Backwards compatible replacement. In new code, use xp_assert_close instead.
    """
    rtol, atol = 0, 1.5*10**(-decimal)
    return xp_assert_close(actual, desired,
                           atol=atol, rtol=rtol, check_dtype=False, check_shape=False,
                           **kwds)


def assert_almost_equal(
    left,
    right,
    check_dtype: bool | Literal["equiv"] = "equiv",
    rtol: float = 1.0e-5,
    atol: float = 1.0e-8,
    **kwargs,
) -> None:
    """
    Check that the left and right objects are approximately equal.

    By approximately equal, we refer to objects that are numbers or that
    contain numbers which may be equivalent to specific levels of precision.

    Parameters
    ----------
    left : object
    right : object
    check_dtype : bool or {'equiv'}, default 'equiv'
        Check dtype if both a and b are the same type. If 'equiv' is passed in,
        then `RangeIndex` and `Index` with int64 dtype are also considered
        equivalent when doing type checking.
    rtol : float, default 1e-5
        Relative tolerance.
    atol : float, default 1e-8
        Absolute tolerance.
    """
    if isinstance(left, Index):
        assert_index_equal(
            left,
            right,
            check_exact=False,
            exact=check_dtype,
            rtol=rtol,
            atol=atol,
            **kwargs,
        )

    elif isinstance(left, Series):
        assert_series_equal(
            left,
            right,
            check_exact=False,
            check_dtype=check_dtype,
            rtol=rtol,
            atol=atol,
            **kwargs,
        )

    elif isinstance(left, DataFrame):
        assert_frame_equal(
            left,
            right,
            check_exact=False,
            check_dtype=check_dtype,
            rtol=rtol,
            atol=atol,
            **kwargs,
        )

    else:
        # Other sequences.
        if check_dtype:
            if is_number(left) and is_number(right):
                # Do not compare numeric classes, like np.float64 and float.
                pass
            elif is_bool(left) and is_bool(right):
                # Do not compare bool classes, like np.bool_ and bool.
                pass
            else:
                if isinstance(left, np.ndarray) or isinstance(right, np.ndarray):
                    obj = "numpy array"
                else:
                    obj = "Input"
                assert_class_equal(left, right, obj=obj)

        # if we have "equiv", this becomes True
        _testing.assert_almost_equal(
            left, right, check_dtype=bool(check_dtype), rtol=rtol, atol=atol, **kwargs
        )


def assert_almost_equal(actual, desired, decimal=7, err_msg='', verbose=True):
    """
    Asserts that two items are almost equal.

    The test is equivalent to abs(desired-actual) < 0.5 * 10**(-decimal).

    """
    if isinstance(actual, np.ndarray) or isinstance(desired, np.ndarray):
        return assert_array_almost_equal(actual, desired, decimal=decimal,
                                         err_msg=err_msg, verbose=verbose)
    msg = build_err_msg([actual, desired],
                        err_msg=err_msg, verbose=verbose)
    if not round(abs(desired - actual), decimal) == 0:
        raise AssertionError(msg)


def assert_almost_equal(actual, desired, decimal=7, err_msg='', verbose=True):
    """
    Raises an AssertionError if two items are not equal up to desired
    precision.

    .. note:: It is recommended to use one of `assert_allclose`,
              `assert_array_almost_equal_nulp` or `assert_array_max_ulp`
              instead of this function for more consistent floating point
              comparisons.

    The test verifies that the elements of `actual` and `desired` satisfy::

        abs(desired-actual) < float64(1.5 * 10**(-decimal))

    That is a looser test than originally documented, but agrees with what the
    actual implementation in `assert_array_almost_equal` did up to rounding
    vagaries. An exception is raised at conflicting values. For ndarrays this
    delegates to assert_array_almost_equal

    Parameters
    ----------
    actual : array_like
        The object to check.
    desired : array_like
        The expected object.
    decimal : int, optional
        Desired precision, default is 7.
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
    assert_allclose: Compare two array_like objects for equality with desired
                     relative and/or absolute precision.
    assert_array_almost_equal_nulp, assert_array_max_ulp, assert_equal

    Examples
    --------
    >>> from numpy.testing import assert_almost_equal
    >>> assert_almost_equal(2.3333333333333, 2.33333334)
    >>> assert_almost_equal(2.3333333333333, 2.33333334, decimal=10)
    Traceback (most recent call last):
        ...
    AssertionError:
    Arrays are not almost equal to 10 decimals
     ACTUAL: 2.3333333333333
     DESIRED: 2.33333334

    >>> assert_almost_equal(np.array([1.0,2.3333333333333]),
    ...                     np.array([1.0,2.33333334]), decimal=9)
    Traceback (most recent call last):
        ...
    AssertionError:
    Arrays are not almost equal to 9 decimals
    <BLANKLINE>
    Mismatched elements: 1 / 2 (50%)
    Mismatch at index:
     [1]: 2.3333333333333 (ACTUAL), 2.33333334 (DESIRED)
    Max absolute difference among violations: 6.66669964e-09
    Max relative difference among violations: 2.85715698e-09
     ACTUAL: array([1.         , 2.333333333])
     DESIRED: array([1.        , 2.33333334])

    """
    __tracebackhide__ = True  # Hide traceback for py.test
    from numpy import imag, iscomplexobj, real
    from numpy._core import ndarray

    # Handle complex numbers: separate into real/imag to handle
    # nan/inf/negative zero correctly
    # XXX: catch ValueError for subclasses of ndarray where iscomplex fail
    try:
        usecomplex = iscomplexobj(actual) or iscomplexobj(desired)
    except ValueError:
        usecomplex = False

    def _build_err_msg():
        header = (f'Arrays are not almost equal to {decimal} decimals')
        return build_err_msg([actual, desired], err_msg, verbose=verbose,
                             header=header)

    if usecomplex:
        if iscomplexobj(actual):
            actualr = real(actual)
            actuali = imag(actual)
        else:
            actualr = actual
            actuali = 0
        if iscomplexobj(desired):
            desiredr = real(desired)
            desiredi = imag(desired)
        else:
            desiredr = desired
            desiredi = 0
        try:
            assert_almost_equal(actualr, desiredr, decimal=decimal)
            assert_almost_equal(actuali, desiredi, decimal=decimal)
        except AssertionError:
            raise AssertionError(_build_err_msg())

    if isinstance(actual, (ndarray, tuple, list)) \
            or isinstance(desired, (ndarray, tuple, list)):
        return assert_array_almost_equal(actual, desired, decimal, err_msg)
    try:
        # If one of desired/actual is not finite, handle it specially here:
        # check that both are nan if any is a nan, and test for equality
        # otherwise
        if not (isfinite(desired) and isfinite(actual)):
            if isnan(desired) or isnan(actual):
                if not (isnan(desired) and isnan(actual)):
                    raise AssertionError(_build_err_msg())
            elif not desired == actual:
                raise AssertionError(_build_err_msg())
            return
    except (NotImplementedError, TypeError):
        pass
    if abs(desired - actual) >= np.float64(1.5 * 10.0**(-decimal)):
        raise AssertionError(_build_err_msg())


def assert_almost_equal(a, b, single_decimal=6, double_decimal=12, **kw):
    if asarray(a).dtype.type in (single, csingle):
        decimal = single_decimal
    else:
        decimal = double_decimal
    old_assert_almost_equal(a, b, decimal=decimal, **kw)

