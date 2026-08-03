from typing import Any

def assert_equal(actual, expected_data, expected_dtype):
    np.testing.assert_equal(actual, np.array(expected_data, dtype=expected_dtype))


def assert_equal(actual, desired, err_msg="", verbose=True):
    """
    Raises an AssertionError if two objects are not equal.

    Given two objects (scalars, lists, tuples, dictionaries or numpy arrays),
    check that all elements of these objects are equal. An exception is raised
    at the first conflicting values.

    When one of `actual` and `desired` is a scalar and the other is array_like,
    the function checks that each element of the array_like object is equal to
    the scalar.

    This function handles NaN comparisons as if NaN was a "normal" number.
    That is, AssertionError is not raised if both objects have NaNs in the same
    positions.  This is in contrast to the IEEE standard on NaNs, which says
    that NaN compared to anything must return False.

    Parameters
    ----------
    actual : array_like
        The object to check.
    desired : array_like
        The expected object.
    err_msg : str, optional
        The error message to be printed in case of failure.
    verbose : bool, optional
        If True, the conflicting values are appended to the error message.

    Raises
    ------
    AssertionError
        If actual and desired are not equal.

    Examples
    --------
    >>> np.testing.assert_equal([4, 5], [4, 6])
    Traceback (most recent call last):
        ...
    AssertionError:
    Items are not equal:
    item=1
     ACTUAL: 5
     DESIRED: 6

    The following comparison does not raise an exception.  There are NaNs
    in the inputs, but they are in the same positions.

    >>> np.testing.assert_equal(np.array([1.0, 2.0, np.nan]), [1, 2, np.nan])

    """
    __tracebackhide__ = True  # Hide traceback for py.test

    num_nones = sum([actual is None, desired is None])
    if num_nones == 1:
        raise AssertionError(f"Not equal: {actual} != {desired}")
    elif num_nones == 2:
        return True
    # else, carry on

    if isinstance(actual, np.DType) or isinstance(desired, np.DType):
        result = actual == desired
        if not result:
            raise AssertionError(f"Not equal: {actual} != {desired}")
        else:
            return True

    if isinstance(desired, str) and isinstance(actual, str):
        if actual != desired:
            raise AssertionError(f"Strings not equal: {actual!r} != {desired!r}")
        return

    if isinstance(desired, dict):
        if not isinstance(actual, dict):
            raise AssertionError(repr(type(actual)))
        assert_equal(len(actual), len(desired), err_msg, verbose)
        for k in desired:
            if k not in actual:
                raise AssertionError(repr(k))
            assert_equal(actual[k], desired[k], f"key={k!r}\n{err_msg}", verbose)
        return
    if isinstance(desired, (list, tuple)) and isinstance(actual, (list, tuple)):
        assert_equal(len(actual), len(desired), err_msg, verbose)
        for k in range(len(desired)):
            assert_equal(actual[k], desired[k], f"item={k!r}\n{err_msg}", verbose)
        return

    from torch._numpy import imag, iscomplexobj, isscalar, ndarray, real, signbit

    if isinstance(actual, ndarray) or isinstance(desired, ndarray):
        return assert_array_equal(actual, desired, err_msg, verbose)
    msg = build_err_msg([actual, desired], err_msg, verbose=verbose)

    # Handle complex numbers: separate into real/imag to handle
    # nan/inf/negative zero correctly
    # XXX: catch ValueError for subclasses of ndarray where iscomplex fail
    try:
        usecomplex = iscomplexobj(actual) or iscomplexobj(desired)
    except (ValueError, TypeError):
        usecomplex = False

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
            assert_equal(actualr, desiredr)
            assert_equal(actuali, desiredi)
        except AssertionError:
            raise AssertionError(msg)  # noqa: B904

    # isscalar test to check cases such as [np.nan] != np.nan
    if isscalar(desired) != isscalar(actual):
        raise AssertionError(msg)

    # Inf/nan/negative zero handling
    try:
        isdesnan = gisnan(desired)
        isactnan = gisnan(actual)
        if isdesnan and isactnan:
            return  # both nan, so equal

        if desired == 0 and actual == 0:
            if not signbit(desired) == signbit(actual):
                raise AssertionError(msg)

    except (TypeError, ValueError, NotImplementedError):
        pass

    try:
        # Explicitly use __eq__ for comparison, gh-2552
        if not (desired == actual):
            raise AssertionError(msg)

    except (DeprecationWarning, FutureWarning) as e:
        # this handles the case when the two types are not even comparable
        if "elementwise == comparison" in e.args[0]:
            raise AssertionError(msg)  # noqa: B904
        else:
            raise


def assert_equal(left, right, **kwargs) -> None:
    """
    Wrapper for tm.assert_*_equal to dispatch to the appropriate test function.

    Parameters
    ----------
    left, right : Index, Series, DataFrame, ExtensionArray, or np.ndarray
        The two items to be compared.
    **kwargs
        All keyword arguments are passed through to the underlying assert method.
    """
    __tracebackhide__ = True

    if isinstance(left, Index):
        assert_index_equal(left, right, **kwargs)
        if isinstance(left, (DatetimeIndex, TimedeltaIndex)):
            assert left.freq == right.freq, (left.freq, right.freq)
    elif isinstance(left, Series):
        assert_series_equal(left, right, **kwargs)
    elif isinstance(left, DataFrame):
        assert_frame_equal(left, right, **kwargs)
    elif isinstance(left, IntervalArray):
        assert_interval_array_equal(left, right, **kwargs)
    elif isinstance(left, PeriodArray):
        assert_period_array_equal(left, right, **kwargs)
    elif isinstance(left, DatetimeArray):
        assert_datetime_array_equal(left, right, **kwargs)
    elif isinstance(left, TimedeltaArray):
        assert_timedelta_array_equal(left, right, **kwargs)
    elif isinstance(left, ExtensionArray):
        assert_extension_array_equal(left, right, **kwargs)
    elif isinstance(left, np.ndarray):
        assert_numpy_array_equal(left, right, **kwargs)
    elif isinstance(left, str):
        assert kwargs == {}
        assert left == right
    else:
        assert kwargs == {}
        assert_almost_equal(left, right)


def assert_equal(a, b):
    assert a == b


def assert_equal(actual, desired, err_msg=''):
    """
    Asserts that two items are equal.

    """
    # Case #1: dictionary .....
    if isinstance(desired, dict):
        if not isinstance(actual, dict):
            raise AssertionError(repr(type(actual)))
        assert_equal(len(actual), len(desired), err_msg)
        for k in desired:
            if k not in actual:
                raise AssertionError(f"{k} not in {actual}")
            assert_equal(actual[k], desired[k], f'key={k!r}\n{err_msg}')
        return
    # Case #2: lists .....
    if isinstance(desired, (list, tuple)) and isinstance(actual, (list, tuple)):
        return _assert_equal_on_sequences(actual, desired, err_msg='')
    if not (isinstance(actual, ndarray) or isinstance(desired, ndarray)):
        msg = build_err_msg([actual, desired], err_msg,)
        if not desired == actual:
            raise AssertionError(msg)
        return
    # Case #4. arrays or equivalent
    if ((actual is masked) and not (desired is masked)) or \
            ((desired is masked) and not (actual is masked)):
        msg = build_err_msg([actual, desired],
                            err_msg, header='', names=('x', 'y'))
        raise ValueError(msg)
    actual = np.asanyarray(actual)
    desired = np.asanyarray(desired)
    (actual_dtype, desired_dtype) = (actual.dtype, desired.dtype)
    if actual_dtype.char == "S" and desired_dtype.char == "S":
        return _assert_equal_on_sequences(actual.tolist(),
                                          desired.tolist(),
                                          err_msg='')
    return assert_array_equal(actual, desired, err_msg)


def assert_equal(actual, desired, err_msg='', verbose=True, *, strict=False):
    """
    Raises an AssertionError if two objects are not equal.

    Given two objects (scalars, lists, tuples, dictionaries or numpy arrays),
    check that all elements of these objects are equal. An exception is raised
    at the first conflicting values.

    This function handles NaN comparisons as if NaN was a "normal" number.
    That is, AssertionError is not raised if both objects have NaNs in the same
    positions.  This is in contrast to the IEEE standard on NaNs, which says
    that NaN compared to anything must return False.

    Parameters
    ----------
    actual : array_like
        The object to check.
    desired : array_like
        The expected object.
    err_msg : str, optional
        The error message to be printed in case of failure.
    verbose : bool, optional
        If True, the conflicting values are appended to the error message.
    strict : bool, optional
        If True and either of the `actual` and `desired` arguments is an array,
        raise an ``AssertionError`` when either the shape or the data type of
        the arguments does not match. If neither argument is an array, this
        parameter has no effect.

        .. versionadded:: 2.0.0

    Raises
    ------
    AssertionError
        If actual and desired are not equal.

    See Also
    --------
    assert_allclose
    assert_array_almost_equal_nulp,
    assert_array_max_ulp,

    Notes
    -----
    When one of `actual` and `desired` is a scalar and the other is array_like, the
    function checks that each element of the array_like is equal to the scalar.
    Note that empty arrays are therefore considered equal to scalars.
    This behaviour can be disabled by setting ``strict==True``.

    Examples
    --------
    >>> np.testing.assert_equal([4, 5], [4, 6])
    Traceback (most recent call last):
        ...
    AssertionError:
    Items are not equal:
    item=1
     ACTUAL: 5
     DESIRED: 6

    The following comparison does not raise an exception.  There are NaNs
    in the inputs, but they are in the same positions.

    >>> np.testing.assert_equal(np.array([1.0, 2.0, np.nan]), [1, 2, np.nan])

    As mentioned in the Notes section, `assert_equal` has special
    handling for scalars when one of the arguments is an array.
    Here, the test checks that each value in `x` is 3:

    >>> x = np.full((2, 5), fill_value=3)
    >>> np.testing.assert_equal(x, 3)

    Use `strict` to raise an AssertionError when comparing a scalar with an
    array of a different shape:

    >>> np.testing.assert_equal(x, 3, strict=True)
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
    >>> np.testing.assert_equal(x, y, strict=True)
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
    if isinstance(desired, dict):
        if not isinstance(actual, dict):
            raise AssertionError(repr(type(actual)))
        assert_equal(len(actual), len(desired), err_msg, verbose)
        for k in desired:
            if k not in actual:
                raise AssertionError(repr(k))
            assert_equal(actual[k], desired[k], f'key={k!r}\n{err_msg}',
                         verbose)
        return
    if isinstance(desired, (list, tuple)) and isinstance(actual, (list, tuple)):
        assert_equal(len(actual), len(desired), err_msg, verbose)
        for k in range(len(desired)):
            assert_equal(actual[k], desired[k], f'item={k!r}\n{err_msg}',
                         verbose)
        return
    from numpy import imag, iscomplexobj, real
    from numpy._core import isscalar, ndarray, signbit
    if isinstance(actual, ndarray) or isinstance(desired, ndarray):
        return assert_array_equal(actual, desired, err_msg, verbose,
                                  strict=strict)
    msg = build_err_msg([actual, desired], err_msg, verbose=verbose)

    # Handle complex numbers: separate into real/imag to handle
    # nan/inf/negative zero correctly
    # XXX: catch ValueError for subclasses of ndarray where iscomplex fail
    try:
        usecomplex = iscomplexobj(actual) or iscomplexobj(desired)
    except (ValueError, TypeError):
        usecomplex = False

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
            assert_equal(actualr, desiredr)
            assert_equal(actuali, desiredi)
        except AssertionError:
            raise AssertionError(msg)

    # isscalar test to check cases such as [np.nan] != np.nan
    if isscalar(desired) != isscalar(actual):
        raise AssertionError(msg)

    try:
        isdesnat = isnat(desired)
        isactnat = isnat(actual)
        dtypes_match = (np.asarray(desired).dtype.type ==
                        np.asarray(actual).dtype.type)
        if isdesnat and isactnat:
            # If both are NaT (and have the same dtype -- datetime or
            # timedelta) they are considered equal.
            if dtypes_match:
                return
            else:
                raise AssertionError(msg)

    except (TypeError, ValueError, NotImplementedError):
        pass

    # Inf/nan/negative zero handling
    try:
        isdesnan = isnan(desired)
        isactnan = isnan(actual)
        if isdesnan and isactnan:
            return  # both nan, so equal

        # handle signed zero specially for floats
        array_actual = np.asarray(actual)
        array_desired = np.asarray(desired)
        if (array_actual.dtype.char in 'Mm' or
                array_desired.dtype.char in 'Mm'):
            # version 1.18
            # until this version, isnan failed for datetime64 and timedelta64.
            # Now it succeeds but comparison to scalar with a different type
            # emits a DeprecationWarning.
            # Avoid that by skipping the next check
            raise NotImplementedError('cannot compare to a scalar '
                                      'with a different type')

        if desired == 0 and actual == 0:
            if not signbit(desired) == signbit(actual):
                raise AssertionError(msg)

    except (TypeError, ValueError, NotImplementedError):
        pass

    try:
        # Explicitly use __eq__ for comparison, gh-2552
        if not (desired == actual):
            raise AssertionError(msg)

    except (DeprecationWarning, FutureWarning) as e:
        # this handles the case when the two types are not even comparable
        if 'elementwise == comparison' in e.args[0]:
            raise AssertionError(msg)
        else:
            raise


def assert_equal(a: object, b: object, fmt: str = "{} != {}") -> None:
    __tracebackhide__ = True
    if a != b:
        raise AssertionError(fmt.format(good_repr(a), good_repr(b)))


def assert_equal(in_tree, fail_message: str = ''):
  """Verifies that all the hosts have the same tree of values."""
  def concat_in_tree(x):
    if isinstance(x, array.ArrayImpl) and not x.is_fully_addressable:
      return np.asarray(x.addressable_data(0))
    else:
      x = np.asarray(x)
      if x.ndim == 0:
        x = np.expand_dims(x, axis=0)
      return np.concat([x] * jax.process_count())

  out = process_allgather(in_tree, tiled=True)
  expected_in_tree = jax.tree.map(concat_in_tree, in_tree)
  if not jax.tree.all(
      jax.tree.map(lambda *x: np.all(np.equal(*x)), expected_in_tree, out)):
    raise AssertionError(
        f'{fail_message}. Expected: {out}; got: {in_tree}.')


def assert_equal(first: Any, second: Any) -> None:
  """Checks that the two objects are equal as determined by the `==` operator.

  Arrays with more than one element cannot be compared.
  Use ``assert_trees_all_close`` to compare arrays.

  Args:
    first: A first object.
    second: A second object.

  Raises:
    AssertionError: If not ``(first == second)``.
  """
  unittest.TestCase().assertEqual(first, second)

