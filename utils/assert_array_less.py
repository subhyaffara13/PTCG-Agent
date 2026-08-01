
def assert_array_less(x, y, err_msg="", verbose=True):
    """
    Raises an AssertionError if two array_like objects are not ordered by less
    than.

    Given two array_like objects, check that the shape is equal and all
    elements of the first object are strictly smaller than those of the
    second object. An exception is raised at shape mismatch or incorrectly
    ordered values. Shape mismatch does not raise if an object has zero
    dimension. In contrast to the standard usage in numpy, NaNs are
    compared, no assertion is raised if both objects have NaNs in the same
    positions.



    Parameters
    ----------
    x : array_like
      The smaller object to check.
    y : array_like
      The larger object to compare.
    err_msg : string
      The error message to be printed in case of failure.
    verbose : bool
        If True, the conflicting values are appended to the error message.

    Raises
    ------
    AssertionError
      If actual and desired objects are not equal.

    See Also
    --------
    assert_array_equal: tests objects for equality
    assert_array_almost_equal: test objects for equality up to precision



    Examples
    --------
    >>> np.testing.assert_array_less([1.0, 1.0, np.nan], [1.1, 2.0, np.nan])
    >>> np.testing.assert_array_less([1.0, 1.0, np.nan], [1, 2.0, np.nan])
    Traceback (most recent call last):
        ...
    AssertionError:
    Arrays are not less-ordered
    <BLANKLINE>
    Mismatched elements: 1 / 3 (33.3%)
    Max absolute difference: 1.0
    Max relative difference: 0.5
     x: torch.ndarray([1.,  1., nan], dtype=float64)
     y: torch.ndarray([1.,  2., nan], dtype=float64)

    >>> np.testing.assert_array_less([1.0, 4.0], 3)
    Traceback (most recent call last):
        ...
    AssertionError:
    Arrays are not less-ordered
    <BLANKLINE>
    Mismatched elements: 1 / 2 (50%)
    Max absolute difference: 2.0
    Max relative difference: 0.6666666666666666
     x: torch.ndarray([1., 4.], dtype=float64)
     y: torch.ndarray(3)

    >>> np.testing.assert_array_less([1.0, 2.0, 3.0], [4])
    Traceback (most recent call last):
        ...
    AssertionError:
    Arrays are not less-ordered
    <BLANKLINE>
    (shapes (3,), (1,) mismatch)
     x: torch.ndarray([1., 2., 3.], dtype=float64)
     y: torch.ndarray([4])

    """
    __tracebackhide__ = True  # Hide traceback for py.test
    assert_array_compare(
        operator.__lt__,
        x,
        y,
        err_msg=err_msg,
        verbose=verbose,
        header="Arrays are not less-ordered",
        equal_inf=False,
    )


def assert_array_less(x, y, err_msg='', verbose=True):
    """
    Checks that x is smaller than y elementwise.

    """
    assert_array_compare(operator.__lt__, x, y,
                         err_msg=err_msg, verbose=verbose,
                         header='Arrays are not less-ordered')


def assert_array_less(x, y, err_msg='', verbose=True, *, strict=False):
    """
    Raises an AssertionError if two array_like objects are not ordered by less
    than.

    Given two array_like objects `x` and `y`, check that the shape is equal and
    all elements of `x` are strictly less than the corresponding elements of
    `y` (but see the Notes for the special handling of a scalar). An exception
    is raised at shape mismatch or values that are not correctly ordered. In
    contrast to the  standard usage in NumPy, no assertion is raised if both
    objects have NaNs in the same positions.

    Parameters
    ----------
    x : array_like
      The smaller object to check.
    y : array_like
      The larger object to compare.
    err_msg : string
      The error message to be printed in case of failure.
    verbose : bool
        If True, the conflicting values are appended to the error message.
    strict : bool, optional
        If True, raise an AssertionError when either the shape or the data
        type of the array_like objects does not match. The special
        handling for scalars mentioned in the Notes section is disabled.

        .. versionadded:: 2.0.0

    Raises
    ------
    AssertionError
      If x is not strictly smaller than y, element-wise.

    See Also
    --------
    assert_array_equal: tests objects for equality
    assert_array_almost_equal: test objects for equality up to precision

    Notes
    -----
    When one of `x` and `y` is a scalar and the other is array_like, the
    function performs the comparison as though the scalar were broadcasted
    to the shape of the array. This behaviour can be disabled with the `strict`
    parameter.

    Examples
    --------
    The following assertion passes because each finite element of `x` is
    strictly less than the corresponding element of `y`, and the NaNs are in
    corresponding locations.

    >>> x = [1.0, 1.0, np.nan]
    >>> y = [1.1, 2.0, np.nan]
    >>> np.testing.assert_array_less(x, y)

    The following assertion fails because the zeroth element of `x` is no
    longer strictly less than the zeroth element of `y`.

    >>> y[0] = 1
    >>> np.testing.assert_array_less(x, y)
    Traceback (most recent call last):
        ...
    AssertionError:
    Arrays are not strictly ordered `x < y`
    <BLANKLINE>
    Mismatched elements: 1 / 3 (33.3%)
    Mismatch at index:
     [0]: 1.0 (x), 1.0 (y)
    Max absolute difference among violations: 0.
    Max relative difference among violations: 0.
     x: array([ 1.,  1., nan])
     y: array([ 1.,  2., nan])

    Here, `y` is a scalar, so each element of `x` is compared to `y`, and
    the assertion passes.

    >>> x = [1.0, 4.0]
    >>> y = 5.0
    >>> np.testing.assert_array_less(x, y)

    However, with ``strict=True``, the assertion will fail because the shapes
    do not match.

    >>> np.testing.assert_array_less(x, y, strict=True)
    Traceback (most recent call last):
        ...
    AssertionError:
    Arrays are not strictly ordered `x < y`
    <BLANKLINE>
    (shapes (2,), () mismatch)
     x: array([1., 4.])
     y: array(5.)

    With ``strict=True``, the assertion also fails if the dtypes of the two
    arrays do not match.

    >>> y = [5, 5]
    >>> np.testing.assert_array_less(x, y, strict=True)
    Traceback (most recent call last):
        ...
    AssertionError:
    Arrays are not strictly ordered `x < y`
    <BLANKLINE>
    (dtypes float64, int64 mismatch)
     x: array([1., 4.])
     y: array([5, 5])
    """
    __tracebackhide__ = True  # Hide traceback for py.test
    assert_array_compare(operator.__lt__, x, y, err_msg=err_msg,
                         verbose=verbose,
                         header='Arrays are not strictly ordered `x < y`',
                         equal_inf=False,
                         strict=strict,
                         names=('x', 'y'))

