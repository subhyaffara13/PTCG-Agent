
def vecmat(x1: ArrayLike, x2: ArrayLike, /) -> Array:
  """Batched conjugate vector-matrix product.

  JAX implementation of :func:`numpy.vecmat`.

  Args:
    x1: array of shape ``(..., M)``.
    x2: array of shape ``(..., M, N)``. Leading dimensions must be broadcast-compatible
      with leading dimensions of ``x1``.

  Returns:
    An array of shape ``(..., N)`` containing the batched conjugate vector-matrix product.

  See also:
    - :func:`jax.numpy.linalg.vecdot`: batched vector product.
    - :func:`jax.numpy.matvec`: matrix-vector product.
    - :func:`jax.numpy.matmul`: general matrix multiplication.

  Examples:
    Simple vector-matrix product:

    >>> x1 = jnp.array([[1, 2, 3]])
    >>> x2 = jnp.array([[4, 5],
    ...                 [6, 7],
    ...                 [8, 9]])
    >>> jnp.vecmat(x1, x2)
    Array([[40, 46]], dtype=int32)

    Batched vector-matrix product:

    >>> x1 = jnp.array([[1, 2, 3],
    ...                 [4, 5, 6]])
    >>> jnp.vecmat(x1, x2)
    Array([[ 40,  46],
           [ 94, 109]], dtype=int32)
  """
  x1, x2 = util.ensure_arraylike("matvec", x1, x2)
  return vectorize(matmul, signature="(n),(n,m)->(m)")(ufuncs.conj(x1), x2)

