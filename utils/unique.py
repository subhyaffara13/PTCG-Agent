
def unique(seq, key=None):
    """ Return only unique elements of a sequence

    >>> tuple(unique((1, 2, 3)))
    (1, 2, 3)
    >>> tuple(unique((1, 2, 1, 3)))
    (1, 2, 3)

    Uniqueness can be defined by key keyword

    >>> tuple(unique(['cat', 'mouse', 'dog', 'hen'], key=len))
    ('cat', 'mouse')
    """
    seen = set()
    seen_add = seen.add
    if key is None:
        for item in seq:
            if item not in seen:
                seen_add(item)
                yield item
    else:  # calculate key
        for item in seq:
            val = key(item)
            if val not in seen:
                seen_add(val)
                yield item


def unique(seq: Sequence[T]) -> Generator[T, None, None]:
    seen = set()
    for x in seq:
        if x not in seen:
            yield x
            seen.add(x)


def unique(it: Iterable[_T]) -> ValuesView[_T]:
    return {id(x): x for x in it}.values()


def unique(
    ar: ArrayLike,
    return_index: NotImplementedType = False,
    return_inverse=False,
    return_counts=False,
    axis=None,
    *,
    equal_nan: NotImplementedType = True,
):
    (ar,), axis = _util.axis_none_flatten(ar, axis=axis)
    axis = _util.normalize_axis_index(axis, ar.ndim)

    result = torch.unique(
        ar, return_inverse=return_inverse, return_counts=return_counts, dim=axis
    )

    return result


def unique(iterable, key=None, reverse=False):
    """Yields unique elements in sorted order.

    >>> list(unique([[1, 2], [3, 4], [1, 2]]))
    [[1, 2], [3, 4]]

    *key* and *reverse* are passed to :func:`sorted`.

    >>> list(unique('ABBcCAD', str.casefold))
    ['A', 'B', 'c', 'D']
    >>> list(unique('ABBcCAD', str.casefold, reverse=True))
    ['D', 'c', 'B', 'A']

    The elements in *iterable* need not be hashable, but they must be
    comparable for sorting to work.
    """
    sequenced = sorted(iterable, key=key, reverse=reverse)
    return unique_justseen(sequenced, key=key)


def unique(values: T) -> T: ...


def unique(values: np.ndarray | Series) -> np.ndarray: ...


def unique(values):
    """
    Return unique values based on a hash table.

    Uniques are returned in order of appearance. This does NOT sort.

    Significantly faster than numpy.unique for long enough sequences.
    Includes NA values.

    Parameters
    ----------
    values : 1d array-like
        The input array-like object containing values from which to extract
        unique values.

    Returns
    -------
    numpy.ndarray, ExtensionArray or NumpyExtensionArray

        The return can be:

        * Index : when the input is an Index
        * Categorical : when the input is a Categorical dtype
        * ndarray : when the input is a Series/ndarray

        Return numpy.ndarray, ExtensionArray or NumpyExtensionArray.

    See Also
    --------
    Index.unique : Return unique values from an Index.
    Series.unique : Return unique values of Series object.

    Examples
    --------
    >>> pd.unique(pd.Series([2, 1, 3, 3]))
    array([2, 1, 3])

    >>> pd.unique(pd.Series([2] + [1] * 5))
    array([2, 1])

    >>> pd.unique(pd.Series([pd.Timestamp("20160101"), pd.Timestamp("20160101")]))
    array(['2016-01-01T00:00:00.000000'], dtype='datetime64[us]')

    >>> pd.unique(
    ...     pd.Series(
    ...         [
    ...             pd.Timestamp("20160101", tz="US/Eastern"),
    ...             pd.Timestamp("20160101", tz="US/Eastern"),
    ...         ],
    ...         dtype="M8[ns, US/Eastern]",
    ...     )
    ... )
    <DatetimeArray>
    ['2016-01-01 00:00:00-05:00']
    Length: 1, dtype: datetime64[ns, US/Eastern]

    >>> pd.unique(
    ...     pd.Index(
    ...         [
    ...             pd.Timestamp("20160101", tz="US/Eastern"),
    ...             pd.Timestamp("20160101", tz="US/Eastern"),
    ...         ],
    ...         dtype="M8[ns, US/Eastern]",
    ...     )
    ... )
    DatetimeIndex(['2016-01-01 00:00:00-05:00'],
            dtype='datetime64[ns, US/Eastern]',
            freq=None)

    >>> pd.unique(np.array(list("baabc"), dtype="O"))
    array(['b', 'a', 'c'], dtype=object)

    An unordered Categorical will return categories in the
    order of appearance.

    >>> pd.unique(pd.Series(pd.Categorical(list("baabc"))))
    ['b', 'a', 'c']
    Categories (3, str): ['a', 'b', 'c']

    >>> pd.unique(pd.Series(pd.Categorical(list("baabc"), categories=list("abc"))))
    ['b', 'a', 'c']
    Categories (3, str): ['a', 'b', 'c']

    An ordered Categorical preserves the category ordering.

    >>> pd.unique(
    ...     pd.Series(
    ...         pd.Categorical(list("baabc"), categories=list("abc"), ordered=True)
    ...     )
    ... )
    ['b', 'a', 'c']
    Categories (3, str): ['a' < 'b' < 'c']

    An array of tuples

    >>> pd.unique(pd.Series([("a", "b"), ("b", "a"), ("a", "c"), ("b", "a")]).values)
    array([('a', 'b'), ('b', 'a'), ('a', 'c')], dtype=object)

    A NumpyExtensionArray of complex

    >>> pd.unique(pd.array([1 + 1j, 2, 3]))
    <NumpyExtensionArray>
    [(1+1j), (2+0j), (3+0j)]
    Length: 3, dtype: complex128
    """
    return unique_with_mask(values)


def unique(ar, return_index=False, return_inverse=False,
           return_counts=False, axis=None, *, equal_nan=True,
           sorted=True):
    """
    Find the unique elements of an array.

    Returns the sorted unique elements of an array. There are three optional
    outputs in addition to the unique elements:

    * the indices of the input array that give the unique values
    * the indices of the unique array that reconstruct the input array
    * the number of times each unique value comes up in the input array

    Parameters
    ----------
    ar : array_like
        Input array. Unless `axis` is specified, this will be flattened if it
        is not already 1-D.
    return_index : bool, optional
        If True, also return the indices of `ar` (along the specified axis,
        if provided, or in the flattened array) that result in the unique array.
    return_inverse : bool, optional
        If True, also return the indices of the unique array (for the specified
        axis, if provided) that can be used to reconstruct `ar`.
    return_counts : bool, optional
        If True, also return the number of times each unique item appears
        in `ar`.
    axis : int or None, optional
        The axis to operate on. If None, `ar` will be flattened. If an integer,
        the subarrays indexed by the given axis will be flattened and treated
        as the elements of a 1-D array with the dimension of the given axis,
        see the notes for more details.  Object arrays or structured arrays
        that contain objects are not supported if the `axis` kwarg is used. The
        default is None.

    equal_nan : bool, optional
        If True, collapses multiple NaN values in the return array into one.

        .. versionadded:: 1.24

    sorted : bool, optional
        If True, the unique elements are sorted. Elements may be sorted in
        practice even if ``sorted=False``, but this could change without
        notice.

        .. versionadded:: 2.3

    Returns
    -------
    unique : ndarray
        The sorted unique values.
    unique_indices : ndarray, optional
        The indices of the first occurrences of the unique values in the
        original array. Only provided if `return_index` is True.
    unique_inverse : ndarray, optional
        The indices to reconstruct the original array from the
        unique array. Only provided if `return_inverse` is True.
    unique_counts : ndarray, optional
        The number of times each of the unique values comes up in the
        original array. Only provided if `return_counts` is True.

    See Also
    --------
    repeat : Repeat elements of an array.
    sort : Return a sorted copy of an array.

    Notes
    -----
    When an axis is specified the subarrays indexed by the axis are sorted.
    This is done by making the specified axis the first dimension of the array
    (move the axis to the first dimension to keep the order of the other axes)
    and then flattening the subarrays in C order. The flattened subarrays are
    then viewed as a structured type with each element given a label, with the
    effect that we end up with a 1-D array of structured types that can be
    treated in the same way as any other 1-D array. The result is that the
    flattened subarrays are sorted in lexicographic order starting with the
    first element.

    .. versionchanged:: 1.21
        Like np.sort, NaN will sort to the end of the values.
        For complex arrays all NaN values are considered equivalent
        (no matter whether the NaN is in the real or imaginary part).
        As the representant for the returned array the smallest one in the
        lexicographical order is chosen - see np.sort for how the lexicographical
        order is defined for complex arrays.

    .. versionchanged:: 2.0
        For multi-dimensional inputs, ``unique_inverse`` is reshaped
        such that the input can be reconstructed using
        ``np.take(unique, unique_inverse, axis=axis)``. The result is
        now not 1-dimensional when ``axis=None``.

        Note that in NumPy 2.0.0 a higher dimensional array was returned also
        when ``axis`` was not ``None``.  This was reverted, but
        ``inverse.reshape(-1)`` can be used to ensure compatibility with both
        versions.

    Examples
    --------
    >>> import numpy as np
    >>> np.unique([1, 1, 2, 2, 3, 3])
    array([1, 2, 3])
    >>> a = np.array([[1, 1], [2, 3]])
    >>> np.unique(a)
    array([1, 2, 3])

    Return the unique rows of a 2D array

    >>> a = np.array([[1, 0, 0], [1, 0, 0], [2, 3, 4]])
    >>> np.unique(a, axis=0)
    array([[1, 0, 0], [2, 3, 4]])

    Return the indices of the original array that give the unique values:

    >>> a = np.array(['a', 'b', 'b', 'c', 'a'])
    >>> u, indices = np.unique(a, return_index=True)
    >>> u
    array(['a', 'b', 'c'], dtype='<U1')
    >>> indices
    array([0, 1, 3])
    >>> a[indices]
    array(['a', 'b', 'c'], dtype='<U1')

    Reconstruct the input array from the unique values and inverse:

    >>> a = np.array([1, 2, 6, 4, 2, 3, 2])
    >>> u, indices = np.unique(a, return_inverse=True)
    >>> u
    array([1, 2, 3, 4, 6])
    >>> indices
    array([0, 1, 4, 3, 1, 2, 1])
    >>> u[indices]
    array([1, 2, 6, 4, 2, 3, 2])

    Reconstruct the input values from the unique values and counts:

    >>> a = np.array([1, 2, 6, 4, 2, 3, 2])
    >>> values, counts = np.unique(a, return_counts=True)
    >>> values
    array([1, 2, 3, 4, 6])
    >>> counts
    array([1, 3, 1, 1, 1])
    >>> np.repeat(values, counts)
    array([1, 2, 2, 2, 3, 4, 6])    # original order not preserved

    """
    ar = np.asanyarray(ar)
    if axis is None or ar.ndim == 1:
        if axis is not None:
            normalize_axis_index(axis, ar.ndim)
        ret = _unique1d(ar, return_index, return_inverse, return_counts,
                        equal_nan=equal_nan, inverse_shape=ar.shape, axis=None,
                        sorted=sorted)
        return _unpack_tuple(ret)

    # axis was specified and not None
    try:
        ar = np.moveaxis(ar, axis, 0)
    except np.exceptions.AxisError:
        # this removes the "axis1" or "axis2" prefix from the error message
        raise np.exceptions.AxisError(axis, ar.ndim) from None
    inverse_shape = [1] * ar.ndim
    inverse_shape[axis] = ar.shape[0]

    # Must reshape to a contiguous 2D array for this to work...
    orig_shape, orig_dtype = ar.shape, ar.dtype
    ar = ar.reshape(orig_shape[0], np.prod(orig_shape[1:], dtype=np.intp))
    ar = np.ascontiguousarray(ar)
    dtype = [(f'f{i}', ar.dtype) for i in range(ar.shape[1])]

    # At this point, `ar` has shape `(n, m)`, and `dtype` is a structured
    # data type with `m` fields where each field has the data type of `ar`.
    # In the following, we create the array `consolidated`, which has
    # shape `(n,)` with data type `dtype`.
    try:
        if ar.shape[1] > 0:
            consolidated = ar.view(dtype)
        else:
            # If ar.shape[1] == 0, then dtype will be `np.dtype([])`, which is
            # a data type with itemsize 0, and the call `ar.view(dtype)` will
            # fail.  Instead, we'll use `np.empty` to explicitly create the
            # array with shape `(len(ar),)`.  Because `dtype` in this case has
            # itemsize 0, the total size of the result is still 0 bytes.
            consolidated = np.empty(len(ar), dtype=dtype)
    except TypeError as e:
        # There's no good way to do this for object arrays, etc...
        msg = 'The axis argument to unique is not supported for dtype {dt}'
        raise TypeError(msg.format(dt=ar.dtype)) from e

    def reshape_uniq(uniq):
        n = len(uniq)
        uniq = uniq.view(orig_dtype)
        uniq = uniq.reshape(n, *orig_shape[1:])
        uniq = np.moveaxis(uniq, 0, axis)
        return uniq

    output = _unique1d(consolidated, return_index,
                       return_inverse, return_counts,
                       equal_nan=equal_nan, inverse_shape=inverse_shape,
                       axis=axis, sorted=sorted)
    output = (reshape_uniq(output[0]),) + output[1:]
    return _unpack_tuple(output)


def unique(ar1, return_index=False, return_inverse=False):
    """
    Finds the unique elements of an array.

    Masked values are considered the same element (masked). The output array
    is always a masked array. See `numpy.unique` for more details.

    See Also
    --------
    numpy.unique : Equivalent function for ndarrays.

    Examples
    --------
    >>> import numpy as np
    >>> a = [1, 2, 1000, 2, 3]
    >>> mask = [0, 0, 1, 0, 0]
    >>> masked_a = np.ma.masked_array(a, mask)
    >>> masked_a
    masked_array(data=[1, 2, --, 2, 3],
                mask=[False, False,  True, False, False],
        fill_value=999999)
    >>> np.ma.unique(masked_a)
    masked_array(data=[1, 2, 3, --],
                mask=[False, False, False,  True],
        fill_value=999999)
    >>> np.ma.unique(masked_a, return_index=True)
    (masked_array(data=[1, 2, 3, --],
                mask=[False, False, False,  True],
        fill_value=999999), array([0, 1, 4, 2]))
    >>> np.ma.unique(masked_a, return_inverse=True)
    (masked_array(data=[1, 2, 3, --],
                mask=[False, False, False,  True],
        fill_value=999999), array([0, 1, 3, 1, 2]))
    >>> np.ma.unique(masked_a, return_index=True, return_inverse=True)
    (masked_array(data=[1, 2, 3, --],
                mask=[False, False, False,  True],
        fill_value=999999), array([0, 1, 4, 2]), array([0, 1, 3, 1, 2]))
    """
    output = np.unique(ar1,
                       return_index=return_index,
                       return_inverse=return_inverse)
    if isinstance(output, tuple):
        output = list(output)
        output[0] = output[0].view(MaskedArray)
        output = tuple(output)
    else:
        output = output.view(MaskedArray)
    return output


def unique(ar: ArrayLike, return_index: bool = False, return_inverse: bool = False,
           return_counts: bool = False, axis: int | None = None,
           *, equal_nan: bool = True, size: int | None = None, fill_value: ArrayLike | None = None,
           sorted: bool = True):
  """Return the unique values from an array.

  JAX implementation of :func:`numpy.unique`.

  Because the size of the output of ``unique`` is data-dependent, the function
  is not typically compatible with :func:`~jax.jit` and other JAX transformations.
  The JAX version adds the optional ``size`` argument which must be specified
  statically for ``jnp.unique`` to be used in such contexts.

  Args:
    ar: N-dimensional array from which unique values will be extracted.
    return_index: if True, also return the indices in ``ar`` where each value occurs
    return_inverse: if True, also return the indices that can be used to reconstruct
      ``ar`` from the unique values.
    return_counts: if True, also return the number of occurrences of each unique value.
    axis: if specified, compute unique values along the specified axis. If None (default),
      then flatten ``ar`` before computing the unique values.
    equal_nan: if True, consider NaN values equivalent when determining uniqueness.
    size: if specified, return only the first ``size`` sorted unique elements. If there are fewer
      unique elements than ``size`` indicates, the return value will be padded with ``fill_value``.
    fill_value: when ``size`` is specified and there are fewer than the indicated number of
      elements, fill the remaining entries ``fill_value``. Defaults to the minimum unique value.
    sorted: unused by JAX.

  Returns:
    An array or tuple of arrays, depending on the values of ``return_index``, ``return_inverse``,
    and ``return_counts``. Returned values are

    - ``unique_values``:
        if ``axis`` is None, a 1D array of length ``n_unique``, If ``axis`` is
        specified, shape is ``(*ar.shape[:axis], n_unique, *ar.shape[axis + 1:])``.
    - ``unique_index``:
        *(returned only if return_index is True)* An array of shape ``(n_unique,)``. Contains
        the indices of the first occurrence of each unique value in ``ar``. For 1D inputs,
        ``ar[unique_index]`` is equivalent to ``unique_values``.
    - ``unique_inverse``:
        *(returned only if return_inverse is True)* An array of shape ``(ar.size,)`` if ``axis``
        is None, or of shape ``(ar.shape[axis],)`` if ``axis`` is specified.
        Contains the indices within ``unique_values`` of each value in ``ar``. For 1D inputs,
        ``unique_values[unique_inverse]`` is equivalent to ``ar``.
    - ``unique_counts``:
        *(returned only if return_counts is True)* An array of shape ``(n_unique,)``.
        Contains the number of occurrences of each unique value in ``ar``.

  See also:
    - :func:`jax.numpy.unique_counts`: shortcut to ``unique(arr, return_counts=True)``.
    - :func:`jax.numpy.unique_inverse`: shortcut to ``unique(arr, return_inverse=True)``.
    - :func:`jax.numpy.unique_all`: shortcut to ``unique`` with all return values.
    - :func:`jax.numpy.unique_values`: like ``unique``, but no optional return values.

  Examples:
    >>> x = jnp.array([3, 4, 1, 3, 1])
    >>> jnp.unique(x)
    Array([1, 3, 4], dtype=int32)

    **JIT compilation & the size argument**

    If you try this under :func:`~jax.jit` or another transformation, you will get an
    error because the output shape is dynamic:

    >>> jax.jit(jnp.unique)(x)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
       ...
    jax.errors.ConcretizationTypeError: Abstract tracer value encountered where concrete value is expected: traced array with shape int32[5].
    The error arose for the first argument of jnp.unique(). To make jnp.unique() compatible with JIT and other transforms, you can specify a concrete value for the size argument, which will determine the output size.

    The issue is that the output of transformed functions must have static shapes.
    In order to make this work, you can pass a static ``size`` parameter:

    >>> jit_unique = jax.jit(jnp.unique, static_argnames=['size'])
    >>> jit_unique(x, size=3)
    Array([1, 3, 4], dtype=int32)

    If your static size is smaller than the true number of unique values, they will be truncated.

    >>> jit_unique(x, size=2)
    Array([1, 3], dtype=int32)

    If the static size is larger than the true number of unique values, they will be padded with
    ``fill_value``, which defaults to the minimum unique value:

    >>> jit_unique(x, size=5)
    Array([1, 3, 4, 1, 1], dtype=int32)
    >>> jit_unique(x, size=5, fill_value=0)
    Array([1, 3, 4, 0, 0], dtype=int32)

    **Multi-dimensional unique values**

    If you pass a multi-dimensional array to ``unique``, it will be flattened by default:

    >>> M = jnp.array([[1, 2],
    ...                [2, 3],
    ...                [1, 2]])
    >>> jnp.unique(M)
    Array([1, 2, 3], dtype=int32)

    If you pass an ``axis`` keyword, you can find unique *slices* of the array along
    that axis:

    >>> jnp.unique(M, axis=0)
    Array([[1, 2],
           [2, 3]], dtype=int32)

    **Returning indices**

    If you set ``return_index=True``, then ``unique`` returns the indices of the
    first occurrence of each unique value:

    >>> x = jnp.array([3, 4, 1, 3, 1])
    >>> values, indices = jnp.unique(x, return_index=True)
    >>> print(values)
    [1 3 4]
    >>> print(indices)
    [2 0 1]
    >>> jnp.all(values == x[indices])
    Array(True, dtype=bool)

    In multiple dimensions, the unique values can be extracted with :func:`jax.numpy.take`
    evaluated along the specified axis:

    >>> values, indices = jnp.unique(M, axis=0, return_index=True)
    >>> jnp.all(values == jnp.take(M, indices, axis=0))
    Array(True, dtype=bool)

    **Returning inverse**

    If you set ``return_inverse=True``, then ``unique`` returns the indices within the
    unique values for every entry in the input array:

    >>> x = jnp.array([3, 4, 1, 3, 1])
    >>> values, inverse = jnp.unique(x, return_inverse=True)
    >>> print(values)
    [1 3 4]
    >>> print(inverse)
    [1 2 0 1 0]
    >>> jnp.all(values[inverse] == x)
    Array(True, dtype=bool)

    In multiple dimensions, the input can be reconstructed using
    :func:`jax.numpy.take`:

    >>> values, inverse = jnp.unique(M, axis=0, return_inverse=True)
    >>> jnp.all(jnp.take(values, inverse, axis=0) == M)
    Array(True, dtype=bool)

    **Returning counts**

    If you set ``return_counts=True``, then ``unique`` returns the number of occurrences
    within the input for every unique value:

    >>> x = jnp.array([3, 4, 1, 3, 1])
    >>> values, counts = jnp.unique(x, return_counts=True)
    >>> print(values)
    [1 3 4]
    >>> print(counts)
    [2 2 1]

    For multi-dimensional arrays, this also returns a 1D array of counts
    indicating number of occurrences along the specified axis:

    >>> values, counts = jnp.unique(M, axis=0, return_counts=True)
    >>> print(values)
    [[1 2]
     [2 3]]
    >>> print(counts)
    [2 1]
  """
  # TODO: Investigate if it's possible that we could save some work in
  # _unique_sorted_mask when sorting is not requested, but that would require
  # refactoring the implementation a bit.
  del sorted  # unused
  arr = ensure_arraylike("unique", ar)
  if size is None:
    arr = core.concrete_or_error(None, arr,
        "The error arose for the first argument of jnp.unique(). " + UNIQUE_SIZE_HINT)
  else:
    size = core.concrete_or_error(operator.index, size,
         "The error arose for the size argument of jnp.unique(). " + UNIQUE_SIZE_HINT)
  arr_shape = arr.shape
  if axis is None:
    axis_int: int = 0
    arr = arr.flatten()
  else:
    axis_int = canonicalize_axis(axis, arr.ndim)
  result = _unique(arr, axis_int, return_index, return_inverse, return_counts,
                   equal_nan=equal_nan, size=size, fill_value=fill_value)
  if return_inverse and axis is None:
    idx = 2 if return_index else 1
    result = (*result[:idx], result[idx].reshape(arr_shape), *result[idx + 1:])
  return result

