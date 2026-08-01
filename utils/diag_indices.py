
def diag_indices(n, ndim=2):
    idx = torch.arange(n)
    return (idx,) * ndim


def diag_indices(n, ndim=2):
    """
    Return the indices to access the main diagonal of an array.

    This returns a tuple of indices that can be used to access the main
    diagonal of an array `a` with ``a.ndim >= 2`` dimensions and shape
    (n, n, ..., n). For ``a.ndim = 2`` this is the usual diagonal, for
    ``a.ndim > 2`` this is the set of indices to access ``a[i, i, ..., i]``
    for ``i = [0..n-1]``.

    Parameters
    ----------
    n : int
      The size, along each dimension, of the arrays for which the returned
      indices can be used.

    ndim : int, optional
      The number of dimensions.

    See Also
    --------
    diag_indices_from

    Examples
    --------
    >>> import numpy as np

    Create a set of indices to access the diagonal of a (4, 4) array:

    >>> di = np.diag_indices(4)
    >>> di
    (array([0, 1, 2, 3]), array([0, 1, 2, 3]))
    >>> a = np.arange(16).reshape(4, 4)
    >>> a
    array([[ 0,  1,  2,  3],
           [ 4,  5,  6,  7],
           [ 8,  9, 10, 11],
           [12, 13, 14, 15]])
    >>> a[di] = 100
    >>> a
    array([[100,   1,   2,   3],
           [  4, 100,   6,   7],
           [  8,   9, 100,  11],
           [ 12,  13,  14, 100]])

    Now, we create indices to manipulate a 3-D array:

    >>> d3 = np.diag_indices(2, 3)
    >>> d3
    (array([0, 1]), array([0, 1]), array([0, 1]))

    And use it to set the diagonal of an array of zeros to 1:

    >>> a = np.zeros((2, 2, 2), dtype=np.int_)
    >>> a[d3] = 1
    >>> a
    array([[[1, 0],
            [0, 0]],
           [[0, 0],
            [0, 1]]])

    """
    idx = np.arange(n)
    return (idx,) * ndim


def diag_indices(n: int, ndim: int = 2) -> tuple[Array, ...]:
  """Return indices for accessing the main diagonal of a multidimensional array.

  JAX implementation of :func:`numpy.diag_indices`.

  Args:
    n: int. The size of each dimension of the square array.
    ndim: optional, int, default=2. The number of dimensions of the array.

  Returns:
    A tuple of arrays, each of length `n`, containing the indices to access
    the main diagonal.

  See also:
    - :func:`jax.numpy.diag_indices_from`
    - :func:`jax.numpy.diagonal`

  Examples:
    >>> jnp.diag_indices(3)
    (Array([0, 1, 2], dtype=int32), Array([0, 1, 2], dtype=int32))
    >>> jnp.diag_indices(4, ndim=3)
    (Array([0, 1, 2, 3], dtype=int32),
    Array([0, 1, 2, 3], dtype=int32),
    Array([0, 1, 2, 3], dtype=int32))
  """
  n = core.concrete_or_error(operator.index, n, "'n' argument of jnp.diag_indices()")
  ndim = core.concrete_or_error(operator.index, ndim, "'ndim' argument of jnp.diag_indices()")
  if n < 0:
    raise ValueError("n argument to diag_indices must be nonnegative, got {}"
                     .format(n))
  if ndim < 0:
    raise ValueError("ndim argument to diag_indices must be nonnegative, got {}"
                     .format(ndim))
  index_dtype = lax_utils.int_dtype_for_dim(n, signed=True)
  # We'd give the correct output values with int32, but use the default dtype to
  # match NumPy type semantics if x64 mode is enabled for now.
  if index_dtype == np.dtype(np.int32):
    index_dtype = dtypes.default_int_dtype()
  return (lax.iota(index_dtype, n),) * ndim

