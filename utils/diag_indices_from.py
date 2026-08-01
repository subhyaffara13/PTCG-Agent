
def diag_indices_from(arr: ArrayLike):
    if not arr.ndim >= 2:
        raise ValueError("input array must be at least 2-d")
    # For more than d=2, the strided formula is only valid for arrays with
    # all dimensions equal, so we check first.
    s = arr.shape
    if s[1:] != s[:-1]:
        raise ValueError("All dimensions of input must be of equal length")
    return diag_indices(s[0], arr.ndim)


def diag_indices_from(arr):
    """
    Return the indices to access the main diagonal of an n-dimensional array.

    See `diag_indices` for full details.

    Parameters
    ----------
    arr : array, at least 2-D

    See Also
    --------
    diag_indices

    Examples
    --------
    >>> import numpy as np

    Create a 4 by 4 array.

    >>> a = np.arange(16).reshape(4, 4)
    >>> a
    array([[ 0,  1,  2,  3],
           [ 4,  5,  6,  7],
           [ 8,  9, 10, 11],
           [12, 13, 14, 15]])

    Get the indices of the diagonal elements.

    >>> di = np.diag_indices_from(a)
    >>> di
    (array([0, 1, 2, 3]), array([0, 1, 2, 3]))

    >>> a[di]
    array([ 0,  5, 10, 15])

    This is simply syntactic sugar for diag_indices.

    >>> np.diag_indices(a.shape[0])
    (array([0, 1, 2, 3]), array([0, 1, 2, 3]))

    """

    if not arr.ndim >= 2:
        raise ValueError("input array must be at least 2-d")
    # For more than d=2, the strided formula is only valid for arrays with
    # all dimensions equal, so we check first.
    if not np.all(diff(arr.shape) == 0):
        raise ValueError("All dimensions of input must be of equal length")

    return diag_indices(arr.shape[0], arr.ndim)


def diag_indices_from(arr: ArrayLike) -> tuple[Array, ...]:
  """Return indices for accessing the main diagonal of a given array.

  JAX implementation of :func:`numpy.diag_indices_from`.

  Args:
    arr: Input array. Must be at least 2-dimensional and have equal length along
      all dimensions.

  Returns:
    A tuple of arrays containing the indices to access the main diagonal of
    the input array.

  See also:
    - :func:`jax.numpy.diag_indices`
    - :func:`jax.numpy.diagonal`

  Examples:
    >>> arr = jnp.array([[1, 2, 3],
    ...                  [4, 5, 6],
    ...                  [7, 8, 9]])
    >>> jnp.diag_indices_from(arr)
    (Array([0, 1, 2], dtype=int32), Array([0, 1, 2], dtype=int32))
    >>> arr = jnp.array([[[1, 2], [3, 4]],
    ...                  [[5, 6], [7, 8]]])
    >>> jnp.diag_indices_from(arr)
    (Array([0, 1], dtype=int32),
    Array([0, 1], dtype=int32),
    Array([0, 1], dtype=int32))
  """
  arr = util.ensure_arraylike("diag_indices_from", arr)
  nd = np.ndim(arr)
  if not np.ndim(arr) >= 2:
    raise ValueError("input array must be at least 2-d")

  s = np.shape(arr)
  if len(set(np.shape(arr))) != 1:
    raise ValueError("All dimensions of input must be of equal length")

  return diag_indices(s[0], ndim=nd)

