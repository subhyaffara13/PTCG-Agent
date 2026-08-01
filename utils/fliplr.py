
def fliplr(m: ArrayLike):
    return torch.fliplr(m)


def fliplr(a: TensorLikeType) -> TensorLikeType:
    if a.ndim < 2:
        raise RuntimeError("Input must be >= 2-d.")

    return flip(a, (1,))


def fliplr(m):
    """
    Reverse the order of elements along axis 1 (left/right).

    For a 2-D array, this flips the entries in each row in the left/right
    direction. Columns are preserved, but appear in a different order than
    before.

    Parameters
    ----------
    m : array_like
        Input array, must be at least 2-D.

    Returns
    -------
    f : ndarray
        A view of `m` with the columns reversed.  Since a view
        is returned, this operation is :math:`\\mathcal O(1)`.

    See Also
    --------
    flipud : Flip array in the up/down direction.
    flip : Flip array in one or more dimensions.
    rot90 : Rotate array counterclockwise.

    Notes
    -----
    Equivalent to ``m[:,::-1]`` or ``np.flip(m, axis=1)``.
    Requires the array to be at least 2-D.

    Examples
    --------
    >>> import numpy as np
    >>> A = np.diag([1.,2.,3.])
    >>> A
    array([[1.,  0.,  0.],
           [0.,  2.,  0.],
           [0.,  0.,  3.]])
    >>> np.fliplr(A)
    array([[0.,  0.,  1.],
           [0.,  2.,  0.],
           [3.,  0.,  0.]])

    >>> rng = np.random.default_rng()
    >>> A = rng.normal(size=(2,3,5))
    >>> np.all(np.fliplr(A) == A[:,::-1,...])
    True

    """
    m = asanyarray(m)
    if m.ndim < 2:
        raise ValueError("Input must be >= 2-d.")
    return m[:, ::-1]


def fliplr(m: ArrayLike) -> Array:
  """Reverse the order of elements of an array along axis 1.

  JAX implementation of :func:`numpy.fliplr`.

  Args:
    m: Array with at least two dimensions.

  Returns:
    An array with the elements in reverse order along axis 1.

  See Also:
    - :func:`jax.numpy.flip`: reverse the order along the given axis
    - :func:`jax.numpy.flipud`: reverse the order along axis 0

  Examples:
    >>> x = jnp.array([[1, 2],
    ...                [3, 4]])
    >>> jnp.fliplr(x)
    Array([[2, 1],
           [4, 3]], dtype=int32)
  """
  arr = util.ensure_arraylike("fliplr", m)
  return _flip(arr, 1)

