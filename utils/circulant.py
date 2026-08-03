import math


def circulant(c):
    """
    Construct a circulant matrix.

    Array argument(s) of this function may have additional
    "batch" dimensions prepended to the core shape. In this case, the array is treated
    as a batch of lower-dimensional slices; see :ref:`linalg_batch` for details.

    Parameters
    ----------
    c : (..., N,)  array_like
        The first column(s) of the matrix. Multidimensional arrays are treated as a
        batch: each slice along the last axis is the first column of an output matrix.

    Returns
    -------
    A : (..., N, N) ndarray
        A circulant matrix whose first column is given by `c`.  For batch input, each
        slice of shape ``(N, N)`` along the last two dimensions of the output
        corresponds with a slice of shape ``(N,)`` along the last dimension of the
        input.


    See Also
    --------
    toeplitz : Toeplitz matrix
    hankel : Hankel matrix
    solve_circulant : Solve a circulant system.

    Notes
    -----
    .. versionadded:: 0.8.0

    Examples
    --------
    >>> from scipy.linalg import circulant
    >>> circulant([1, 2, 3])
    array([[1, 3, 2],
           [2, 1, 3],
           [3, 2, 1]])

    >>> circulant([[1, 2, 3], [4, 5, 6]])
    array([[[1, 3, 2],
            [2, 1, 3],
            [3, 2, 1]],
           [[4, 6, 5],
            [5, 4, 6],
            [6, 5, 4]]])
    """
    c = np.atleast_1d(c)
    batch_shape, N = c.shape[:-1], c.shape[-1]
    # Need to use `prod(batch_shape)` instead of `-1` in case array has zero size
    c = c.reshape(math.prod(batch_shape), N) if batch_shape else c
    # Form an extended array that could be strided to give circulant version
    c_ext = np.concatenate((c[..., ::-1], c[..., :0:-1]), axis=-1).ravel()
    L = c.shape[-1]
    n = c_ext.strides[-1]
    if c.ndim == 1:
        A = as_strided(c_ext[L-1:], shape=(L, L), strides=(-n, n))
    else:
        m = c.shape[0]
        A = as_strided(c_ext[L-1:], shape=(m, L, L), strides=(n*(2*L-1), -n, n))
    return A.reshape(batch_shape + (N, N)).copy()


def circulant(c: ArrayLike) -> Array:
  r"""Construct a circulant matrix.

  JAX implementation of :func:`scipy.linalg.circulant`.

  A circulant matrix has cyclically shifted columns: :math:`A_{ij} = c_{(i - j) \bmod n}`
  for :math:`0 \le i, j < n`, where ``c`` specifies the first column.

  Args:
    c: array of shape ``(..., N)`` specifying the first column.

  Returns:
    A circulant matrix of shape ``(..., N, N)``.

  Examples:
    >>> c = jnp.array([1, 2, 3])
    >>> jax.scipy.linalg.circulant(c)
    Array([[1, 3, 2],
           [2, 1, 3],
           [3, 2, 1]], dtype=int32)

    For N-dimensional ``c``, the result is a batch of circulant matrices:

    >>> c = jnp.array([[1, 2, 3], [4, 5, 6]])
    >>> jax.scipy.linalg.circulant(c)
    Array([[[1, 3, 2],
            [2, 1, 3],
            [3, 2, 1]],
    <BLANKLINE>
           [[4, 6, 5],
            [5, 4, 6],
            [6, 5, 4]]], dtype=int32)
  """
  check_arraylike("circulant", c)
  return _circulant(jnp.atleast_1d(jnp.asarray(c)))

