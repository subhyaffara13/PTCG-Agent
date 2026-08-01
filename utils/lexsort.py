
def lexsort(keys, axis=-1):
    """
    lexsort(keys, axis=-1)

    Perform an indirect stable sort using a sequence of keys.

    Given multiple sorting keys, lexsort returns an array of integer indices
    that describes the sort order by multiple keys. The last key in the
    sequence is used for the primary sort order, ties are broken by the
    second-to-last key, and so on.

    Parameters
    ----------
    keys : (k, m, n, ...) array-like
        The `k` keys to be sorted. The *last* key (e.g, the last
        row if `keys` is a 2D array) is the primary sort key.
        Each element of `keys` along the zeroth axis must be
        an array-like object of the same shape.
    axis : int, optional
        Axis to be indirectly sorted. By default, sort over the last axis
        of each sequence. Separate slices along `axis` sorted over
        independently; see last example.

    Returns
    -------
    indices : (m, n, ...) ndarray of ints
        Array of indices that sort the keys along the specified axis.

    See Also
    --------
    argsort : Indirect sort.
    ndarray.sort : In-place sort.
    sort : Return a sorted copy of an array.

    Examples
    --------
    Sort names: first by surname, then by name.

    >>> import numpy as np
    >>> surnames =    ('Hertz',    'Galilei', 'Hertz')
    >>> first_names = ('Heinrich', 'Galileo', 'Gustav')
    >>> ind = np.lexsort((first_names, surnames))
    >>> ind
    array([1, 2, 0])

    >>> [surnames[i] + ", " + first_names[i] for i in ind]
    ['Galilei, Galileo', 'Hertz, Gustav', 'Hertz, Heinrich']

    Sort according to two numerical keys, first by elements
    of ``a``, then breaking ties according to elements of ``b``:

    >>> a = [1, 5, 1, 4, 3, 4, 4]  # First sequence
    >>> b = [9, 4, 0, 4, 0, 2, 1]  # Second sequence
    >>> ind = np.lexsort((b, a))  # Sort by `a`, then by `b`
    >>> ind
    array([2, 0, 4, 6, 5, 3, 1])
    >>> [(a[i], b[i]) for i in ind]
    [(1, 0), (1, 9), (3, 0), (4, 1), (4, 2), (4, 4), (5, 4)]

    Compare against `argsort`, which would sort each key independently.

    >>> np.argsort((b, a), kind='stable')
    array([[2, 4, 6, 5, 1, 3, 0],
           [0, 2, 4, 3, 5, 6, 1]])

    To sort lexicographically with `argsort`, we would need to provide a
    structured array.

    >>> x = np.array([(ai, bi) for ai, bi in zip(a, b)],
    ...              dtype = np.dtype([('x', int), ('y', int)]))
    >>> np.argsort(x)  # or np.argsort(x, order=('x', 'y'))
    array([2, 0, 4, 6, 5, 3, 1])

    The zeroth axis of `keys` always corresponds with the sequence of keys,
    so 2D arrays are treated just like other sequences of keys.

    >>> arr = np.asarray([b, a])
    >>> ind2 = np.lexsort(arr)
    >>> np.testing.assert_equal(ind2, ind)

    Accordingly, the `axis` parameter refers to an axis of *each* key, not of
    the `keys` argument itself. For instance, the array ``arr`` is treated as
    a sequence of two 1-D keys, so specifying ``axis=0`` is equivalent to
    using the default axis, ``axis=-1``.

    >>> np.testing.assert_equal(np.lexsort(arr, axis=0),
    ...                         np.lexsort(arr, axis=-1))

    For higher-dimensional arrays, the axis parameter begins to matter. The
    resulting array has the same shape as each key, and the values are what
    we would expect if `lexsort` were performed on corresponding slices
    of the keys independently. For instance,

    >>> x = [[1, 2, 3, 4],
    ...      [4, 3, 2, 1],
    ...      [2, 1, 4, 3]]
    >>> y = [[2, 2, 1, 1],
    ...      [1, 2, 1, 2],
    ...      [1, 1, 2, 1]]
    >>> np.lexsort((x, y), axis=1)
    array([[2, 3, 0, 1],
           [2, 0, 3, 1],
           [1, 0, 3, 2]])

    Each row of the result is what we would expect if we were to perform
    `lexsort` on the corresponding row of the keys:

    >>> for i in range(3):
    ...     print(np.lexsort((x[i], y[i])))
    [2 3 0 1]
    [2 0 3 1]
    [1 0 3 2]

    """
    if isinstance(keys, tuple):
        return keys
    else:
        return (keys,)


def lexsort(keys: Array | np.ndarray | Sequence[ArrayLike], axis: int = -1) -> Array:
  """Sort a sequence of keys in lexicographic order.

  JAX implementation of :func:`numpy.lexsort`.

  Args:
    keys: a sequence of arrays to sort; all arrays must have the same shape.
      The last key in the sequence is used as the primary key.
    axis: the axis along which to sort (default: -1).

  Returns:
    An array of integers of shape ``keys[0].shape`` giving the indices of the
    entries in lexicographically-sorted order.

  See also:
    - :func:`jax.numpy.argsort`: sort a single entry by index.
    - :func:`jax.lax.sort`: direct XLA sorting API.

  Examples:
    :func:`lexsort` with a single key is equivalent to :func:`argsort`:

    >>> key1 = jnp.array([4, 2, 3, 2, 5])
    >>> jnp.lexsort([key1])
    Array([1, 3, 2, 0, 4], dtype=int32)
    >>> jnp.argsort(key1)
    Array([1, 3, 2, 0, 4], dtype=int32)

    With multiple keys, :func:`lexsort` uses the last key as the primary key:

    >>> key2 = jnp.array([2, 1, 1, 2, 2])
    >>> jnp.lexsort([key1, key2])
    Array([1, 2, 3, 0, 4], dtype=int32)

    The meaning of the indices become more clear when printing the sorted keys:

    >>> indices = jnp.lexsort([key1, key2])
    >>> print(f"{key1[indices]}\\n{key2[indices]}")
    [2 3 2 4 5]
    [1 1 2 2 2]

    Notice that the elements of ``key2`` appear in order, and within the sequences
    of duplicated values the corresponding elements of ```key1`` appear in order.

    For multi-dimensional inputs, :func:`lexsort` defaults to sorting along the
    last axis:

    >>> key1 = jnp.array([[2, 4, 2, 3],
    ...                   [3, 1, 2, 2]])
    >>> key2 = jnp.array([[1, 2, 1, 3],
    ...                   [2, 1, 2, 1]])
    >>> jnp.lexsort([key1, key2])
    Array([[0, 2, 1, 3],
           [1, 3, 2, 0]], dtype=int32)

    A different sort axis can be chosen using the ``axis`` keyword; here we sort
    along the leading axis:

    >>> jnp.lexsort([key1, key2], axis=0)
    Array([[0, 1, 0, 1],
           [1, 0, 1, 0]], dtype=int32)
  """
  key_arrays = util.ensure_arraylike_tuple("lexsort", tuple(keys))
  if len(key_arrays) == 0:
    raise TypeError("need sequence of keys with len > 0 in lexsort")
  if len({np.shape(key) for key in key_arrays}) > 1:
    raise ValueError("all keys need to be the same shape")
  if np.ndim(key_arrays[0]) == 0:
    return lax.full((), 0, dtypes.default_int_dtype())
  axis = canonicalize_axis(axis, np.ndim(key_arrays[0]))
  idx_dtype = lax_utils.int_dtype_for_dim(key_arrays[0].shape[axis],
                                          signed=True)
  # We'd give the correct output values with int32, but use the default dtype to
  # match NumPy type semantics if x64 mode is enabled for now.
  if idx_dtype == np.dtype(np.int32):
    idx_dtype = dtypes.default_int_dtype()
  iota = lax.broadcasted_iota(idx_dtype, np.shape(key_arrays[0]), axis)
  return lax.sort((*key_arrays[::-1], iota), dimension=axis, num_keys=len(key_arrays))[-1]

