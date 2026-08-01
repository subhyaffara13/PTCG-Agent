
def place(arr, mask, vals):
    """
    Change elements of an array based on conditional and input values.

    Similar to ``np.copyto(arr, vals, where=mask)``, the difference is that
    `place` uses the first N elements of `vals`, where N is the number of
    True values in `mask`, while `copyto` uses the elements where `mask`
    is True.

    Note that `extract` does the exact opposite of `place`.

    Parameters
    ----------
    arr : ndarray
        Array to put data into.
    mask : array_like
        Boolean mask array. Must have the same size as `arr`.
    vals : 1-D sequence
        Values to put into `arr`. Only the first N elements are used, where
        N is the number of True values in `mask`. If `vals` is smaller
        than N, it will be repeated, and if elements of `arr` are to be masked,
        this sequence must be non-empty.

    See Also
    --------
    copyto, put, take, extract

    Examples
    --------
    >>> import numpy as np
    >>> arr = np.arange(6).reshape(2, 3)
    >>> np.place(arr, arr>2, [44, 55])
    >>> arr
    array([[ 0,  1,  2],
           [44, 55, 44]])

    """
    return _place(arr, mask, vals)


def place(arr: ArrayLike, mask: ArrayLike, vals: ArrayLike, *,
          inplace: bool = True) -> Array:
  """Update array elements based on a mask.

  JAX implementation of :func:`numpy.place`.

  The semantics of :func:`numpy.place` are to modify arrays in-place, which
  is not possible for JAX's immutable arrays. The JAX version returns a modified
  copy of the input, and adds the ``inplace`` parameter which must be set to
  `False`` by the user as a reminder of this API difference.

  Args:
    arr: array into which values will be placed.
    mask: boolean mask with the same size as ``arr``.
    vals: values to be inserted into ``arr`` at the locations indicated
      by mask. If too many values are supplied, they will be truncated.
      If not enough values are supplied, they will be repeated.
    inplace: must be set to False to indicate that the input is not modified
      in-place, but rather a modified copy is returned.

  Returns:
    A copy of ``arr`` with masked values set to entries from `vals`.

  See Also:
    - :func:`jax.numpy.put`: put elements into an array at numerical indices.
    - :func:`jax.numpy.ndarray.at`: array updates using NumPy-style indexing

  Examples:
    >>> x = jnp.zeros((3, 5), dtype=int)
    >>> mask = (jnp.arange(x.size) % 3 == 0).reshape(x.shape)
    >>> mask
    Array([[ True, False, False,  True, False],
           [False,  True, False, False,  True],
           [False, False,  True, False, False]], dtype=bool)

    Placing a scalar value:

    >>> jnp.place(x, mask, 1, inplace=False)
    Array([[1, 0, 0, 1, 0],
           [0, 1, 0, 0, 1],
           [0, 0, 1, 0, 0]], dtype=int32)

    In this case, ``jnp.place`` is similar to the masked array update syntax:

    >>> x.at[mask].set(1)
    Array([[1, 0, 0, 1, 0],
           [0, 1, 0, 0, 1],
           [0, 0, 1, 0, 0]], dtype=int32)

    ``place`` differs when placing values from an array. The array is repeated
    to fill the masked entries:

    >>> vals = jnp.array([1, 3, 5])
    >>> jnp.place(x, mask, vals, inplace=False)
    Array([[1, 0, 0, 3, 0],
           [0, 5, 0, 0, 1],
           [0, 0, 3, 0, 0]], dtype=int32)
  """
  data, mask_arr, vals_arr = util.ensure_arraylike("place", arr, mask, vals)
  vals_arr = vals_arr.ravel()
  if inplace:
    raise ValueError(
      "jax.numpy.place cannot modify arrays in-place, because JAX arrays are immutable. "
      "Pass inplace=False to instead return an updated array.")
  if data.size != mask_arr.size:
    raise ValueError("place: arr and mask must be the same size")
  if not vals_arr.size:
    raise ValueError("Cannot place values from an empty array")
  if not data.size:
    return data
  indices = lax_numpy.where(mask_arr.ravel(), size=mask_arr.size, fill_value=mask_arr.size)[0]
  vals_arr = lax_numpy._tile_to_size(vals_arr, len(indices))
  return data.ravel().at[indices].set(vals_arr, mode='drop').reshape(data.shape)

