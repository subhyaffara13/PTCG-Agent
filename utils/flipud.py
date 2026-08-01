
def flipud(m: ArrayLike):
    return torch.flipud(m)


def flipud(a: TensorLikeType) -> TensorLikeType:
    if a.ndim < 1:
        raise RuntimeError("Input must be >= 1-d.")

    return flip(a, (0,))


def flipud(m):
    """
    Reverse the order of elements along axis 0 (up/down).

    For a 2-D array, this flips the entries in each column in the up/down
    direction. Rows are preserved, but appear in a different order than before.

    Parameters
    ----------
    m : array_like
        Input array.

    Returns
    -------
    out : array_like
        A view of `m` with the rows reversed.  Since a view is
        returned, this operation is :math:`\\mathcal O(1)`.

    See Also
    --------
    fliplr : Flip array in the left/right direction.
    flip : Flip array in one or more dimensions.
    rot90 : Rotate array counterclockwise.

    Notes
    -----
    Equivalent to ``m[::-1, ...]`` or ``np.flip(m, axis=0)``.
    Requires the array to be at least 1-D.

    Examples
    --------
    >>> import numpy as np
    >>> A = np.diag([1.0, 2, 3])
    >>> A
    array([[1.,  0.,  0.],
           [0.,  2.,  0.],
           [0.,  0.,  3.]])
    >>> np.flipud(A)
    array([[0.,  0.,  3.],
           [0.,  2.,  0.],
           [1.,  0.,  0.]])

    >>> rng = np.random.default_rng()
    >>> A = rng.normal(size=(2,3,5))
    >>> np.all(np.flipud(A) == A[::-1,...])
    True

    >>> np.flipud([1,2])
    array([2, 1])

    """
    m = asanyarray(m)
    if m.ndim < 1:
        raise ValueError("Input must be >= 1-d.")
    return m[::-1, ...]


def flipud(m: ArrayLike) -> Array:
  """Reverse the order of elements of an array along axis 0.

  JAX implementation of :func:`numpy.flipud`.

  Args:
    m: Array with at least one dimension.

  Returns:
    An array with the elements in reverse order along axis 0.

  See Also:
    - :func:`jax.numpy.flip`: reverse the order along the given axis
    - :func:`jax.numpy.fliplr`: reverse the order along axis 1

  Examples:
    >>> x = jnp.array([[1, 2],
    ...                [3, 4]])
    >>> jnp.flipud(x)
    Array([[3, 4],
           [1, 2]], dtype=int32)
  """
  arr = util.ensure_arraylike("flipud", m)
  return _flip(arr, 0)

