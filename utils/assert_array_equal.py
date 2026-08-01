
def assert_array_equal(x, y, err_msg="", verbose=True, *, strict=False):
    """
    Raises an AssertionError if two array_like objects are not equal.

    Given two array_like objects, check that the shape is equal and all
    elements of these objects are equal (but see the Notes for the special
    handling of a scalar). An exception is raised at shape mismatch or
    conflicting values. In contrast to the standard usage in numpy, NaNs
    are compared like numbers, no assertion is raised if both objects have
    NaNs in the same positions.

    The usual caution for verifying equality with floating point numbers is
    advised.

    Parameters
    ----------
    x : array_like
        The actual object to check.
    y : array_like
        The desired, expected object.
    err_msg : str, optional
        The error message to be printed in case of failure.
    verbose : bool, optional
        If True, the conflicting values are appended to the error message.
    strict : bool, optional
        If True, raise an AssertionError when either the shape or the data
        type of the array_like objects does not match. The special
        handling for scalars mentioned in the Notes section is disabled.

    Raises
    ------
    AssertionError
        If actual and desired objects are not equal.

    See Also
    --------
    assert_allclose: Compare two array_like objects for equality with desired
                     relative and/or absolute precision.
    assert_array_almost_equal_nulp, assert_array_max_ulp, assert_equal

    Notes
    -----
    When one of `x` and `y` is a scalar and the other is array_like, the
    function checks that each element of the array_like object is equal to
    the scalar. This behaviour can be disabled with the `strict` parameter.

    Examples
    --------
    The first assert does not raise an exception:

    >>> np.testing.assert_array_equal(
    ...     [1.0, 2.33333, np.nan], [np.exp(0), 2.33333, np.nan]
    ... )

    Use `assert_allclose` or one of the nulp (number of floating point values)
    functions for these cases instead:

    >>> np.testing.assert_allclose(
    ...     [1.0, np.pi, np.nan], [1, np.sqrt(np.pi) ** 2, np.nan], rtol=1e-10, atol=0
    ... )

    As mentioned in the Notes section, `assert_array_equal` has special
    handling for scalars. Here the test checks that each value in `x` is 3:

    >>> x = np.full((2, 5), fill_value=3)
    >>> np.testing.assert_array_equal(x, 3)

    Use `strict` to raise an AssertionError when comparing a scalar with an
    array:

    >>> np.testing.assert_array_equal(x, 3, strict=True)
    Traceback (most recent call last):
        ...
    AssertionError:
    Arrays are not equal
    <BLANKLINE>
    (shapes (2, 5), () mismatch)
     x: torch.ndarray([[3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3]])
     y: torch.ndarray(3)

    The `strict` parameter also ensures that the array data types match:

    >>> x = np.array([2, 2, 2])
    >>> y = np.array([2.0, 2.0, 2.0], dtype=np.float32)
    >>> np.testing.assert_array_equal(x, y, strict=True)
    Traceback (most recent call last):
        ...
    AssertionError:
    Arrays are not equal
    <BLANKLINE>
    (dtypes dtype("int64"), dtype("float32") mismatch)
     x: torch.ndarray([2, 2, 2])
     y: torch.ndarray([2., 2., 2.])
    """
    __tracebackhide__ = True  # Hide traceback for py.test
    assert_array_compare(
        operator.__eq__,
        x,
        y,
        err_msg=err_msg,
        verbose=verbose,
        header="Arrays are not equal",
        strict=strict,
    )


def assert_array_equal(testclass, v_expected, v_actual):
  """Asserts that two arrays are equal."""
  if hasattr(v_expected, 'dtype'):
    testclass.assertEqual(v_expected.dtype, v_actual.dtype)
  testclass.assertIsInstance(v_actual, type(v_expected))
  if isinstance(v_expected, jax.Array):
    if jax.dtypes.issubdtype(v_expected.dtype, jax.dtypes.prng_key):
      # random key
      testclass.assertTrue(
          jax.dtypes.issubdtype(v_actual.dtype, jax.dtypes.prng_key)
      )
      expected_array = jax.random.key_data(v_expected)
      actual_array = jax.random.key_data(v_actual)
      assert_array_equal(testclass, expected_array, actual_array)
      testclass.assertEqual(
          str(jax.random.key_impl(v_expected)),
          str(jax.random.key_impl(v_actual)),
      )
    else:
      # regular array
      testclass.assertEqual(
          len(v_expected.addressable_shards), len(v_actual.addressable_shards)
      )
      for shard_expected, shard_actual in zip(
          v_expected.addressable_shards, v_actual.addressable_shards
      ):
        np.testing.assert_array_equal(shard_actual.data, shard_expected.data)
  elif isinstance(v_expected, (np.ndarray, jnp.ndarray)):
    np.testing.assert_array_equal(v_actual, v_expected)
  else:
    testclass.assertEqual(v_expected, v_actual)


def assert_array_equal(x, y, err_msg='', verbose=True):
    """
    Checks the elementwise equality of two masked arrays.

    """
    assert_array_compare(operator.__eq__, x, y,
                         err_msg=err_msg, verbose=verbose,
                         header='Arrays are not equal')


def assert_array_equal(actual, desired, err_msg='', verbose=True, *,
                       strict=False):
    """
    Raises an AssertionError if two array_like objects are not equal.

    Given two array_like objects, check that the shape is equal and all
    elements of these objects are equal (but see the Notes for the special
    handling of a scalar). An exception is raised at shape mismatch or
    conflicting values. In contrast to the standard usage in numpy, NaNs
    are compared like numbers, no assertion is raised if both objects have
    NaNs in the same positions.

    The usual caution for verifying equality with floating point numbers is
    advised.

    .. note:: When either `actual` or `desired` is already an instance of
        `numpy.ndarray` and `desired` is not a ``dict``, the behavior of
        ``assert_equal(actual, desired)`` is identical to the behavior of this
        function. Otherwise, this function performs `np.asanyarray` on the
        inputs before comparison, whereas `assert_equal` defines special
        comparison rules for common Python types. For example, only
        `assert_equal` can be used to compare nested Python lists. In new code,
        consider using only `assert_equal`, explicitly converting either
        `actual` or `desired` to arrays if the behavior of `assert_array_equal`
        is desired.

    Parameters
    ----------
    actual : array_like
        The actual object to check.
    desired : array_like
        The desired, expected object.
    err_msg : str, optional
        The error message to be printed in case of failure.
    verbose : bool, optional
        If True, the conflicting values are appended to the error message.
    strict : bool, optional
        If True, raise an AssertionError when either the shape or the data
        type of the array_like objects does not match. The special
        handling for scalars mentioned in the Notes section is disabled.

        .. versionadded:: 1.24.0

    Raises
    ------
    AssertionError
        If actual and desired objects are not equal.

    See Also
    --------
    assert_allclose: Compare two array_like objects for equality with desired
                     relative and/or absolute precision.
    assert_array_almost_equal_nulp, assert_array_max_ulp, assert_equal

    Notes
    -----
    When one of `actual` and `desired` is a scalar and the other is array_like, the
    function checks that each element of the array_like is equal to the scalar.
    Note that empty arrays are therefore considered equal to scalars.
    This behaviour can be disabled by setting ``strict==True``.

    Examples
    --------
    >>> import numpy as np

    The first assert does not raise an exception:

    >>> np.testing.assert_array_equal([1.0,2.33333,np.nan],
    ...                               [np.exp(0),2.33333, np.nan])

    Assert fails with numerical imprecision with floats:

    >>> np.testing.assert_array_equal([1.0,np.pi,np.nan],
    ...                               [1, np.sqrt(np.pi)**2, np.nan])
    Traceback (most recent call last):
        ...
    AssertionError:
    Arrays are not equal
    <BLANKLINE>
    Mismatched elements: 1 / 3 (33.3%)
    Mismatch at index:
     [1]: 3.141592653589793 (ACTUAL), 3.1415926535897927 (DESIRED)
    Max absolute difference among violations: 4.4408921e-16
    Max relative difference among violations: 1.41357986e-16
     ACTUAL: array([1.      , 3.141593,      nan])
     DESIRED: array([1.      , 3.141593,      nan])

    Use `assert_allclose` or one of the nulp (number of floating point values)
    functions for these cases instead:

    >>> np.testing.assert_allclose([1.0,np.pi,np.nan],
    ...                            [1, np.sqrt(np.pi)**2, np.nan],
    ...                            rtol=1e-10, atol=0)

    As mentioned in the Notes section, `assert_array_equal` has special
    handling for scalars. Here the test checks that each value in `x` is 3:

    >>> x = np.full((2, 5), fill_value=3)
    >>> np.testing.assert_array_equal(x, 3)

    Use `strict` to raise an AssertionError when comparing a scalar with an
    array:

    >>> np.testing.assert_array_equal(x, 3, strict=True)
    Traceback (most recent call last):
        ...
    AssertionError:
    Arrays are not equal
    <BLANKLINE>
    (shapes (2, 5), () mismatch)
     ACTUAL: array([[3, 3, 3, 3, 3],
           [3, 3, 3, 3, 3]])
     DESIRED: array(3)

    The `strict` parameter also ensures that the array data types match:

    >>> x = np.array([2, 2, 2])
    >>> y = np.array([2., 2., 2.], dtype=np.float32)
    >>> np.testing.assert_array_equal(x, y, strict=True)
    Traceback (most recent call last):
        ...
    AssertionError:
    Arrays are not equal
    <BLANKLINE>
    (dtypes int64, float32 mismatch)
     ACTUAL: array([2, 2, 2])
     DESIRED: array([2., 2., 2.], dtype=float32)
    """
    __tracebackhide__ = True  # Hide traceback for py.test
    assert_array_compare(operator.__eq__, actual, desired, err_msg=err_msg,
                         verbose=verbose, header='Arrays are not equal',
                         strict=strict)

