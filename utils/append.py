
def append(a, vancestors):
    """
    Append ``a`` to the list of the virtual ancestors, unless it is already
    included.
    """
    add = True
    for j, va in enumerate(vancestors):
        if issubclass(va, a):
            add = False
            break
        if issubclass(a, va):
            vancestors[j] = a
            add = False
    if add:
        vancestors.append(a)


def append(arr: ArrayLike, values: ArrayLike, axis=None):
    if axis is None:
        if arr.ndim != 1:
            arr = arr.flatten()
        values = values.flatten()
        axis = arr.ndim - 1
    return _concatenate((arr, values), axis=axis)


def append(g: jit_utils.GraphContext, self, tensor):
    return g.op("SequenceInsert", self, tensor)


def append(
    state: ReplayBufferState,
    experience: Experience,
) -> ReplayBufferState:
  """Potentially adds `experience` to the replay buffer.

  Args:
    state: `ReplayBufferState`, current state of the buffer
    experience: data to be added to the reservoir buffer.

  Returns:
    An updated `ReplayBufferState`
  """

  chex.assert_trees_all_equal_dtypes(experience, state.experience)

  index = state.entry_index % state.capacity

  def update_leaf(buffer_leaf: Experience, exp_leaf: Experience):
    return buffer_leaf.at[index].set(exp_leaf)

  new_experience = jax.tree.map(update_leaf, state.experience, experience)

  new_entry_index = state.entry_index + 1
  new_is_full = state.is_full | (new_entry_index >= state.capacity)

  return ReplayBufferState(
      capacity=state.capacity,
      experience=new_experience,
      entry_index=new_entry_index,
      is_full=new_is_full,
  )


def append(arr, values, axis=None):
    """
    Append values to the end of an array.

    Parameters
    ----------
    arr : array_like
        Values are appended to a copy of this array.
    values : array_like
        These values are appended to a copy of `arr`.  It must be of the
        correct shape (the same shape as `arr`, excluding `axis`).  If
        `axis` is not specified, `values` can be any shape and will be
        flattened before use.
    axis : int, optional
        The axis along which `values` are appended.  If `axis` is not
        given, both `arr` and `values` are flattened before use.

    Returns
    -------
    append : ndarray
        A copy of `arr` with `values` appended to `axis`.  Note that
        `append` does not occur in-place: a new array is allocated and
        filled.  If `axis` is None, `out` is a flattened array.

    See Also
    --------
    insert : Insert elements into an array.
    delete : Delete elements from an array.

    Examples
    --------
    >>> import numpy as np
    >>> np.append([1, 2, 3], [[4, 5, 6], [7, 8, 9]])
    array([1, 2, 3, ..., 7, 8, 9])

    When `axis` is specified, `values` must have the correct shape.

    >>> np.append([[1, 2, 3], [4, 5, 6]], [[7, 8, 9]], axis=0)
    array([[1, 2, 3],
           [4, 5, 6],
           [7, 8, 9]])

    >>> np.append([[1, 2, 3], [4, 5, 6]], [7, 8, 9], axis=0)
    Traceback (most recent call last):
        ...
    ValueError: all the input arrays must have same number of dimensions, but
    the array at index 0 has 2 dimension(s) and the array at index 1 has 1
    dimension(s)

    >>> a = np.array([1, 2], dtype=np.int_)
    >>> c = np.append(a, [])
    >>> c
    array([1., 2.])
    >>> c.dtype
    float64

    Default dtype for empty ndarrays is `float64` thus making the output of dtype
    `float64` when appended with dtype `int64`

    """
    arr = asanyarray(arr)
    if axis is None:
        if arr.ndim != 1:
            arr = arr.ravel()
        values = ravel(values)
        axis = arr.ndim - 1
    return concatenate((arr, values), axis=axis)


def append(a, b, axis=None):
    """Append values to the end of an array.

    Parameters
    ----------
    a : array_like
        Values are appended to a copy of this array.
    b : array_like
        These values are appended to a copy of `a`.  It must be of the
        correct shape (the same shape as `a`, excluding `axis`).  If `axis`
        is not specified, `b` can be any shape and will be flattened
        before use.
    axis : int, optional
        The axis along which `v` are appended.  If `axis` is not given,
        both `a` and `b` are flattened before use.

    Returns
    -------
    append : MaskedArray
        A copy of `a` with `b` appended to `axis`.  Note that `append`
        does not occur in-place: a new array is allocated and filled.  If
        `axis` is None, the result is a flattened array.

    See Also
    --------
    numpy.append : Equivalent function in the top-level NumPy module.

    Examples
    --------
    >>> import numpy as np
    >>> import numpy.ma as ma
    >>> a = ma.masked_values([1, 2, 3], 2)
    >>> b = ma.masked_values([[4, 5, 6], [7, 8, 9]], 7)
    >>> ma.append(a, b)
    masked_array(data=[1, --, 3, 4, 5, 6, --, 8, 9],
                 mask=[False,  True, False, False, False, False,  True, False,
                       False],
           fill_value=999999)
    """
    return concatenate([a, b], axis)


def append(acc=[]):
    return acc


def append(
    arr: ArrayLike, values: ArrayLike, axis: int | None = None
) -> Array:
  """Return a new array with values appended to the end of the original array.

  JAX implementation of :func:`numpy.append`.

  Args:
    arr: original array.
    values: values to be appended to the array. The ``values`` must have
      the same number of dimensions as ``arr``, and all dimensions must
      match except in the specified axis.
    axis: axis along which to append values. If None (default), both ``arr``
      and ``values`` will be flattened before appending.

  Returns:
    A new array with values appended to ``arr``.

  See also:
    - :func:`jax.numpy.insert`
    - :func:`jax.numpy.delete`

  Examples:
    >>> a = jnp.array([1, 2, 3])
    >>> b = jnp.array([4, 5, 6])
    >>> jnp.append(a, b)
    Array([1, 2, 3, 4, 5, 6], dtype=int32)

    Appending along a specific axis:

    >>> a = jnp.array([[1, 2],
    ...                [3, 4]])
    >>> b = jnp.array([[5, 6]])
    >>> jnp.append(a, b, axis=0)
    Array([[1, 2],
           [3, 4],
           [5, 6]], dtype=int32)

    Appending along a trailing axis:

    >>> a = jnp.array([[1, 2, 3],
    ...                [4, 5, 6]])
    >>> b = jnp.array([[7], [8]])
    >>> jnp.append(a, b, axis=1)
    Array([[1, 2, 3, 7],
           [4, 5, 6, 8]], dtype=int32)
  """
  if axis is None:
    return concatenate([ravel(arr), ravel(values)], 0)
  else:
    return concatenate([arr, values], axis=axis)

