
def matrix_transpose(A):
    """Return the matrix transpose of `A`.

    Parameters
    ----------
    A : sparse array
        Input array.

    Returns
    -------
    sparse array
        The matrix transpose of `A`.

    See Also
    --------
    coo_array.mT : equivalent attribute
    coo_array.T : full transposition reversing all dimensions
    numpy.matrix_transpose : equivalent function in NumPy

    Notes
    -----
    This is equivalent to ``A.T`` for 2-D arrays, and interprets
    greater dimensional `A` as a stack of 2-D arrays on which
    to perform the transpose.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.sparse import coo_array, matrix_transpose
    >>> data = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
    >>> array = coo_array(data)
    >>> array.T.toarray()
    array([[[1, 5],
            [3, 7]],
    <BLANKLINE>
           [[2, 6],
            [4, 8]]])
    >>> matrix_transpose(array).toarray()
    array([[[1, 3],
            [2, 4]],
    <BLANKLINE>
           [[5, 7],
            [6, 8]]])
    """
    return A.mT


def matrix_transpose(x: Array, /, xp: Namespace) -> Array:
    if x.ndim < 2:
        raise ValueError("x must be at least 2-dimensional for matrix_transpose")
    return xp.swapaxes(x, -1, -2)


def matrix_transpose(x, /):
    return _core_matrix_transpose(x)


def matrix_transpose(x, /):
    """
    Transposes a matrix (or a stack of matrices) ``x``.

    This function is Array API compatible.

    Parameters
    ----------
    x : array_like
        Input array having shape (..., M, N) and whose two innermost
        dimensions form ``MxN`` matrices.

    Returns
    -------
    out : ndarray
        An array containing the transpose for each matrix and having shape
        (..., N, M).

    See Also
    --------
    transpose : Generic transpose method.

    Examples
    --------
    >>> import numpy as np
    >>> np.matrix_transpose([[1, 2], [3, 4]])
    array([[1, 3],
           [2, 4]])

    >>> np.matrix_transpose([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
    array([[[1, 3],
            [2, 4]],
           [[5, 7],
            [6, 8]]])

    """
    x = asanyarray(x)
    if x.ndim < 2:
        raise ValueError(
            f"Input array must be at least 2-dimensional, but it is {x.ndim}"
        )
    return swapaxes(x, -1, -2)


def matrix_transpose(x: ArrayLike, /) -> Array:
  """Transpose the last two dimensions of an array.

  JAX implementation of :func:`numpy.matrix_transpose`, implemented in terms of
  :func:`jax.lax.transpose`.

  Args:
    x: input array, Must have ``x.ndim >= 2``

  Returns:
    matrix-transposed copy of the array.

  See Also:
    - :attr:`jax.Array.mT`: same operation accessed via an :func:`~jax.Array` property.
    - :func:`jax.numpy.transpose`: general multi-axis transpose

  Note:
    Unlike :func:`numpy.matrix_transpose`, :func:`jax.numpy.matrix_transpose` will return a
    copy rather than a view of the input array. However, under JIT, the compiler will
    optimize-away such copies when possible, so this doesn't have performance impacts in practice.

  Examples:
    Here is a 2x2x2 matrix representing a batched 2x2 matrix:

    >>> x = jnp.array([[[1, 2],
    ...                 [3, 4]],
    ...                [[5, 6],
    ...                 [7, 8]]])
    >>> jnp.matrix_transpose(x)
    Array([[[1, 3],
            [2, 4]],
    <BLANKLINE>
           [[5, 7],
            [6, 8]]], dtype=int32)

    For convenience, you can perform the same transpose via the :attr:`~jax.Array.mT`
    property of :class:`jax.Array`:

    >>> x.mT
    Array([[[1, 3],
            [2, 4]],
    <BLANKLINE>
           [[5, 7],
            [6, 8]]], dtype=int32)
  """
  x = util.ensure_arraylike("matrix_transpose", x)
  ndim = x.ndim
  if ndim < 2:
    raise ValueError(f"x must be at least two-dimensional for matrix_transpose; got {ndim=}")
  axes = (*range(ndim - 2), ndim - 1, ndim - 2)
  return lax.transpose(x, axes)


def matrix_transpose(x: ArrayLike, /) -> Array:
  """Transpose a matrix or stack of matrices.

  JAX implementation of :func:`numpy.linalg.matrix_transpose`.

  Args:
    x: array of shape ``(..., M, N)``

  Returns:
    array of shape ``(..., N, M)`` containing the matrix transpose of ``x``.

  See also:
    :func:`jax.numpy.transpose`: more general transpose operation.

  Examples:
    Transpose of a single matrix:

    >>> x = jnp.array([[1, 2, 3],
    ...                [4, 5, 6]])
    >>> jnp.linalg.matrix_transpose(x)
    Array([[1, 4],
           [2, 5],
           [3, 6]], dtype=int32)

    Transpose of a stack of matrices:

    >>> x = jnp.array([[[1, 2],
    ...                 [3, 4]],
    ...                [[5, 6],
    ...                 [7, 8]]])
    >>> jnp.linalg.matrix_transpose(x)
    Array([[[1, 3],
            [2, 4]],
    <BLANKLINE>
           [[5, 7],
            [6, 8]]], dtype=int32)

    For convenience, the same computation can be done via the
    :attr:`~jax.Array.mT` property of JAX array objects:

    >>> x.mT
    Array([[[1, 3],
            [2, 4]],
    <BLANKLINE>
           [[5, 7],
            [6, 8]]], dtype=int32)
  """
  x_arr = ensure_arraylike('jnp.linalg.matrix_transpose', x)
  ndim = x_arr.ndim
  if ndim < 2:
    raise ValueError(f"matrix_transpose requires at least 2 dimensions; got {ndim=}")
  return lax.transpose(x_arr, (*range(ndim - 2), ndim - 1, ndim - 2))

