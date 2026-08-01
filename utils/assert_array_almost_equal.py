
def assert_array_almost_equal(x, y, decimal=6, err_msg="", verbose=True):
    """
    Raises an AssertionError if two objects are not equal up to desired
    precision.

    .. note:: It is recommended to use one of `assert_allclose`,
              `assert_array_almost_equal_nulp` or `assert_array_max_ulp`
              instead of this function for more consistent floating point
              comparisons.

    The test verifies identical shapes and that the elements of ``actual`` and
    ``desired`` satisfy.

        ``abs(desired-actual) < 1.5 * 10**(-decimal)``

    That is a looser test than originally documented, but agrees with what the
    actual implementation did up to rounding vagaries. An exception is raised
    at shape mismatch or conflicting values. In contrast to the standard usage
    in numpy, NaNs are compared like numbers, no assertion is raised if both
    objects have NaNs in the same positions.

    Parameters
    ----------
    x : array_like
        The actual object to check.
    y : array_like
        The desired, expected object.
    decimal : int, optional
        Desired precision, default is 6.
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
    the first assert does not raise an exception

    >>> np.testing.assert_array_almost_equal([1.0, 2.333, np.nan], [1.0, 2.333, np.nan])

    >>> np.testing.assert_array_almost_equal(
    ...     [1.0, 2.33333, np.nan], [1.0, 2.33339, np.nan], decimal=5
    ... )
    Traceback (most recent call last):
        ...
    AssertionError:
    Arrays are not almost equal to 5 decimals
    <BLANKLINE>
    Mismatched elements: 1 / 3 (33.3%)
    Max absolute difference: 5.999999999994898e-05
    Max relative difference: 2.5713661239633743e-05
     x: torch.ndarray([1.0000, 2.3333,    nan], dtype=float64)
     y: torch.ndarray([1.0000, 2.3334,    nan], dtype=float64)

    >>> np.testing.assert_array_almost_equal(
    ...     [1.0, 2.33333, np.nan], [1.0, 2.33333, 5], decimal=5
    ... )
    Traceback (most recent call last):
        ...
    AssertionError:
    Arrays are not almost equal to 5 decimals
    <BLANKLINE>
    x and y nan location mismatch:
     x: torch.ndarray([1.0000, 2.3333,    nan], dtype=float64)
     y: torch.ndarray([1.0000, 2.3333, 5.0000], dtype=float64)

    """
    __tracebackhide__ = True  # Hide traceback for py.test
    from torch._numpy import any as npany, float_, issubdtype, number, result_type

    def compare(x, y):
        try:
            if npany(gisinf(x)) or npany(gisinf(y)):
                xinfid = gisinf(x)
                yinfid = gisinf(y)
                if not (xinfid == yinfid).all():
                    return False
                # if one item, x and y is +- inf
                if x.size == y.size == 1:
                    return x == y
                x = x[~xinfid]
                y = y[~yinfid]
        except (TypeError, NotImplementedError):
            pass

        # make sure y is an inexact type to avoid abs(MIN_INT); will cause
        # casting of x later.
        dtype = result_type(y, 1.0)
        y = asanyarray(y, dtype)
        z = abs(x - y)

        if not issubdtype(z.dtype, number):
            z = z.astype(float_)  # handle object arrays

        return z < 1.5 * 10.0 ** (-decimal)

    assert_array_compare(
        compare,
        x,
        y,
        err_msg=err_msg,
        verbose=verbose,
        header=f"Arrays are not almost equal to {decimal:d} decimals",
        precision=decimal,
    )


def assert_array_almost_equal(actual, desired, decimal=6, *args, **kwds):
    """Backwards compatible replacement. In new code, use xp_assert_close instead.
    """
    rtol, atol = 0, 1.5*10**(-decimal)
    return xp_assert_close(actual, desired,
                           atol=atol, rtol=rtol, check_dtype=False, check_shape=False,
                           *args, **kwds)


def assert_array_almost_equal(actual, desired, decimal=6, **kwds):
    """Backwards compatible replacement. In new code, use xp_assert_close instead.
    """
    rtol, atol = 0, 1.5*10**(-decimal)
    return xp_assert_close(actual, desired,
                           atol=atol, rtol=rtol, check_dtype=False, check_shape=False,
                           **kwds)


def assert_array_almost_equal(x, y, decimal=6, err_msg='', verbose=True):
    """
    Checks the equality of two masked arrays, up to given number odecimals.

    The equality is checked elementwise.

    """
    def compare(x, y):
        "Returns the result of the loose comparison between x and y)."
        return almost(x, y, decimal)
    assert_array_compare(compare, x, y, err_msg=err_msg, verbose=verbose,
                         header='Arrays are not almost equal')


def assert_array_almost_equal(actual, desired, decimal=6, err_msg='',
                              verbose=True):
    """
    Raises an AssertionError if two objects are not equal up to desired
    precision.

    .. note:: It is recommended to use one of `assert_allclose`,
              `assert_array_almost_equal_nulp` or `assert_array_max_ulp`
              instead of this function for more consistent floating point
              comparisons.

    The test verifies identical shapes and that the elements of ``actual`` and
    ``desired`` satisfy::

        abs(desired-actual) < 1.5 * 10**(-decimal)

    That is a looser test than originally documented, but agrees with what the
    actual implementation did up to rounding vagaries. An exception is raised
    at shape mismatch or conflicting values. In contrast to the standard usage
    in numpy, NaNs are compared like numbers, no assertion is raised if both
    objects have NaNs in the same positions.

    Parameters
    ----------
    actual : array_like
        The actual object to check.
    desired : array_like
        The desired, expected object.
    decimal : int, optional
        Desired precision, default is 6.
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
    the first assert does not raise an exception

    >>> np.testing.assert_array_almost_equal([1.0,2.333,np.nan],
    ...                                      [1.0,2.333,np.nan])

    >>> np.testing.assert_array_almost_equal([1.0,2.33333,np.nan],
    ...                                      [1.0,2.33339,np.nan], decimal=5)
    Traceback (most recent call last):
        ...
    AssertionError:
    Arrays are not almost equal to 5 decimals
    <BLANKLINE>
    Mismatched elements: 1 / 3 (33.3%)
    Mismatch at index:
     [1]: 2.33333 (ACTUAL), 2.33339 (DESIRED)
    Max absolute difference among violations: 6.e-05
    Max relative difference among violations: 2.57136612e-05
     ACTUAL: array([1.     , 2.33333,     nan])
     DESIRED: array([1.     , 2.33339,     nan])

    >>> np.testing.assert_array_almost_equal([1.0,2.33333,np.nan],
    ...                                      [1.0,2.33333, 5], decimal=5)
    Traceback (most recent call last):
        ...
    AssertionError:
    Arrays are not almost equal to 5 decimals
    <BLANKLINE>
    nan location mismatch:
     ACTUAL: array([1.     , 2.33333,     nan])
     DESIRED: array([1.     , 2.33333, 5.     ])

    """
    __tracebackhide__ = True  # Hide traceback for py.test
    from numpy._core import number, result_type
    from numpy._core.numerictypes import issubdtype

    def compare(x, y):
        # make sure y is an inexact type to avoid abs(MIN_INT); will cause
        # casting of x later.
        dtype = result_type(y, 1.)
        y = np.asanyarray(y, dtype)
        z = abs(x - y)

        if not issubdtype(z.dtype, number):
            z = z.astype(np.float64)  # handle object arrays

        return z < 1.5 * 10.0**(-decimal)

    assert_array_compare(compare, actual, desired, err_msg=err_msg, verbose=verbose,
             header=f'Arrays are not almost equal to {decimal} decimals',
             precision=decimal)

