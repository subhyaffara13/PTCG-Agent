
def put_along_axis(arr: ArrayLike, indices: ArrayLike, values: ArrayLike, axis):
    (arr,), axis = _util.axis_none_flatten(arr, axis=axis)
    axis = _util.normalize_axis_index(axis, arr.ndim)

    indices, values = torch.broadcast_tensors(indices, values)
    values = _util.cast_if_needed(values, arr.dtype)
    result = torch.scatter(arr, axis, indices, values)
    arr.copy_(result.reshape(arr.shape))
    return None


def put_along_axis(arr, indices, values, axis):
    """
    Put values into the destination array by matching 1d index and data slices.

    This iterates over matching 1d slices oriented along the specified axis in
    the index and data arrays, and uses the former to place values into the
    latter. These slices can be different lengths.

    Functions returning an index along an axis, like `argsort` and
    `argpartition`, produce suitable indices for this function.

    Parameters
    ----------
    arr : ndarray (Ni..., M, Nk...)
        Destination array.
    indices : ndarray (Ni..., J, Nk...)
        Indices to change along each 1d slice of `arr`. This must match the
        dimension of arr, but dimensions in Ni and Nj may be 1 to broadcast
        against `arr`.
    values : array_like (Ni..., J, Nk...)
        values to insert at those indices. Its shape and dimension are
        broadcast to match that of `indices`.
    axis : int
        The axis to take 1d slices along. If axis is None, the destination
        array is treated as if a flattened 1d view had been created of it.

    Notes
    -----
    This is equivalent to (but faster than) the following use of `ndindex` and
    `s_`, which sets each of ``ii`` and ``kk`` to a tuple of indices::

        Ni, M, Nk = a.shape[:axis], a.shape[axis], a.shape[axis+1:]
        J = indices.shape[axis]  # Need not equal M

        for ii in ndindex(Ni):
            for kk in ndindex(Nk):
                a_1d       = a      [ii + s_[:,] + kk]
                indices_1d = indices[ii + s_[:,] + kk]
                values_1d  = values [ii + s_[:,] + kk]
                for j in range(J):
                    a_1d[indices_1d[j]] = values_1d[j]

    Equivalently, eliminating the inner loop, the last two lines would be::

                a_1d[indices_1d] = values_1d

    See Also
    --------
    take_along_axis :
        Take values from the input array by matching 1d index and data slices

    Examples
    --------
    >>> import numpy as np

    For this sample array

    >>> a = np.array([[10, 30, 20], [60, 40, 50]])

    We can replace the maximum values with:

    >>> ai = np.argmax(a, axis=1, keepdims=True)
    >>> ai
    array([[1],
           [0]])
    >>> np.put_along_axis(a, ai, 99, axis=1)
    >>> a
    array([[10, 99, 20],
           [99, 40, 50]])

    """
    # normalize inputs
    if axis is None:
        if indices.ndim != 1:
            raise ValueError(
                'when axis=None, `indices` must have a single dimension.')
        arr = np.array(arr.flat)
        axis = 0
    else:
        axis = normalize_axis_index(axis, arr.ndim)

    # use the fancy index
    arr[_make_along_axis_idx(arr.shape, indices, axis)] = values


def put_along_axis(
  arr: ArrayLike,
  indices: ArrayLike,
  values: ArrayLike,
  axis: int | None,
  inplace: bool = True,
  *,
  mode: str | None = None,
) -> Array:
  """Put values into the destination array by matching 1d index and data slices.

  JAX implementation of :func:`numpy.put_along_axis`.

  The semantics of :func:`numpy.put_along_axis` are to modify arrays in-place, which
  is not possible for JAX's immutable arrays. The JAX version returns a modified
  copy of the input, and adds the ``inplace`` parameter which must be set to
  `False`` by the user as a reminder of this API difference.

  Args:
    arr: array into which values will be put.
    indices: array of indices at which to put values.
    values: array of values to put into the array.
    axis: the axis along which to put values. If not specified, the array will
      be flattened before indexing is applied.
    inplace: must be set to False to indicate that the input is not modified
      in-place, but rather a modified copy is returned.
    mode: Out-of-bounds indexing mode. For more discussion of ``mode`` options,
      see :attr:`jax.numpy.ndarray.at`.

  Returns:
    A copy of ``a`` with specified entries updated.

  See Also:
    - :func:`jax.numpy.put`: put elements into an array at given indices.
    - :func:`jax.numpy.place`: place elements into an array via boolean mask.
    - :func:`jax.numpy.ndarray.at`: array updates using NumPy-style indexing.
    - :func:`jax.numpy.take`: extract values from an array at given indices.
    - :func:`jax.numpy.take_along_axis`: extract values from an array along an axis.

  Examples:
    >>> from jax import numpy as jnp
    >>> a = jnp.array([[10, 30, 20], [60, 40, 50]])
    >>> i = jnp.argmax(a, axis=1, keepdims=True)
    >>> print(i)
    [[1]
     [0]]
    >>> b = jnp.put_along_axis(a, i, 99, axis=1, inplace=False)
    >>> print(b)
    [[10 99 20]
     [99 40 50]]
  """
  if inplace:
    raise ValueError(
      "jax.numpy.put_along_axis cannot modify arrays in-place, because JAX arrays"
      "are immutable. Pass inplace=False to instead return an updated array.")

  arr, indices, values = util.ensure_arraylike("put_along_axis", arr, indices, values)

  original_axis = axis
  original_arr_shape = arr.shape

  if axis is None:
    arr = arr.ravel()
    axis = 0

  if not arr.ndim == indices.ndim:
    raise ValueError(
      "put_along_axis arguments 'arr' and 'indices' must have same ndim. Got "
      f"{arr.ndim=} and {indices.ndim=}."
    )

  try:
    values = util._broadcast_to(values, indices.shape)
  except ValueError:
    raise ValueError(
      "put_along_axis argument 'values' must be broadcastable to 'indices'. Got "
      f"{values.shape=} and {indices.shape=}."
    )

  idx = _make_along_axis_idx(arr.shape, indices, axis)
  result = arr.at[idx].set(values, mode=mode)

  if original_axis is None:
    result = result.reshape(original_arr_shape)

  return result

