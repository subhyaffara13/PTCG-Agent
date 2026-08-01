
def tril_indices_from(arr: ArrayLike, k=0):
    if arr.ndim != 2:
        raise ValueError("input array must be 2-d")
    # Return a tensor rather than a tuple to avoid a graphbreak
    return torch.tril_indices(arr.shape[0], arr.shape[1], offset=k)


def tril_indices_from(arr, k=0):
    """
    Return the indices for the lower-triangle of arr.

    See `tril_indices` for full details.

    Parameters
    ----------
    arr : array_like
        The indices will be valid for square arrays whose dimensions are
        the same as arr.
    k : int, optional
        Diagonal offset (see `tril` for details).

    Examples
    --------
    >>> import numpy as np

    Create a 4 by 4 array

    >>> a = np.arange(16).reshape(4, 4)
    >>> a
    array([[ 0,  1,  2,  3],
           [ 4,  5,  6,  7],
           [ 8,  9, 10, 11],
           [12, 13, 14, 15]])

    Pass the array to get the indices of the lower triangular elements.

    >>> trili = np.tril_indices_from(a)
    >>> trili
    (array([0, 1, 1, 2, 2, 2, 3, 3, 3, 3]), array([0, 0, 1, 0, 1, 2, 0, 1, 2, 3]))

    >>> a[trili]
    array([ 0,  4,  5,  8,  9, 10, 12, 13, 14, 15])

    This is syntactic sugar for tril_indices().

    >>> np.tril_indices(a.shape[0])
    (array([0, 1, 1, 2, 2, 2, 3, 3, 3, 3]), array([0, 0, 1, 0, 1, 2, 0, 1, 2, 3]))

    Use the `k` parameter to return the indices for the lower triangular array
    up to the k-th diagonal.

    >>> trili1 = np.tril_indices_from(a, k=1)
    >>> a[trili1]
    array([ 0,  1,  4,  5,  6,  8,  9, 10, 11, 12, 13, 14, 15])

    See Also
    --------
    tril_indices, tril, triu_indices_from
    """
    if arr.ndim != 2:
        raise ValueError("input array must be 2-d")
    return tril_indices(arr.shape[-2], k=k, m=arr.shape[-1])


def tril_indices_from(arr: ArrayLike | SupportsShape, k: int = 0) -> tuple[Array, Array]:
  """Return the indices of lower triangle of a given array.

  JAX implementation of :func:`numpy.tril_indices_from`.

  Args:
    arr: input array. Must have ``arr.ndim == 2``.
    k: optional, int, default=0. Specifies the sub-diagonal on and below which
      the indices of upper triangle are returned. ``k=0`` refers to main diagonal,
      ``k<0`` refers to sub-diagonal below the main diagonal and ``k>0`` refers
      to sub-diagonal above the main diagonal.

  Returns:
    A tuple of two arrays containing the indices of the lower triangle, one along
    each axis.

  See also:
    - :func:`jax.numpy.triu_indices_from`: Returns the indices of upper triangle
      of a given array.
    - :func:`jax.numpy.tril_indices`: Returns the indices of lower triangle of an
      array of size ``(n, m)``.
    - :func:`jax.numpy.tril`: Returns a lower triangle of an array

  Examples:
    >>> arr = jnp.array([[1, 2, 3],
    ...                  [4, 5, 6],
    ...                  [7, 8, 9]])
    >>> jnp.tril_indices_from(arr)
    (Array([0, 1, 1, 2, 2, 2], dtype=int32), Array([0, 0, 1, 0, 1, 2], dtype=int32))

    Elements indexed by ``jnp.tril_indices_from`` correspond to those in the
    output of ``jnp.tril``.

    >>> ind = jnp.tril_indices_from(arr)
    >>> arr[ind]
    Array([1, 4, 5, 7, 8, 9], dtype=int32)
    >>> jnp.tril(arr)
    Array([[1, 0, 0],
           [4, 5, 0],
           [7, 8, 9]], dtype=int32)

    When ``k > 0``:

    >>> jnp.tril_indices_from(arr, k=1)
    (Array([0, 0, 1, 1, 1, 2, 2, 2], dtype=int32), Array([0, 1, 0, 1, 2, 0, 1, 2], dtype=int32))

    When ``k < 0``:

    >>> jnp.tril_indices_from(arr, k=-1)
    (Array([1, 2, 2], dtype=int32), Array([0, 0, 1], dtype=int32))
  """
  if hasattr(arr, "shape"):
    arr_shape = arr.shape
  else:
    arr = util.ensure_arraylike("tril_indices_from", arr)
    arr_shape = arr.shape
  if len(arr_shape) != 2:
    raise ValueError("Only 2-D inputs are accepted")
  return tril_indices(arr_shape[0], k=k, m=arr_shape[1])

