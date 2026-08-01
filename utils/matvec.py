
def matvec(v):
    if not hasattr(count, 'c'):
        count.c = [0]
    count.c[0] += 1
    return Am@v


def matvec(v):
    if not hasattr(count, 'c'):
        count.c = [0]
    count.c[0] += 1
    return Am@v


def matvec(x1: ArrayLike, x2: ArrayLike, /) -> Array:
  """Batched matrix-vector product.

  JAX implementation of :func:`numpy.matvec`.

  Args:
    x1: array of shape ``(..., M, N)``
    x2: array of shape ``(..., N)``. Leading dimensions must be broadcast-compatible
      with leading dimensions of ``x1``.

  Returns:
    An array of shape ``(..., M)`` containing the batched matrix-vector product.

  See also:
    - :func:`jax.numpy.linalg.vecdot`: batched vector product.
    - :func:`jax.numpy.vecmat`: vector-matrix product.
    - :func:`jax.numpy.matmul`: general matrix multiplication.

  Examples:
    Simple matrix-vector product:

    >>> x1 = jnp.array([[1, 2, 3],
    ...                 [4, 5, 6]])
    >>> x2 = jnp.array([7, 8, 9])
    >>> jnp.matvec(x1, x2)
    Array([ 50, 122], dtype=int32)

    Batched matrix-vector product:

    >>> x2 = jnp.array([[7, 8, 9],
    ...                 [5, 6, 7]])
    >>> jnp.matvec(x1, x2)
    Array([[ 50, 122],
           [ 38,  92]], dtype=int32)
  """
  x1, x2 = util.ensure_arraylike("matvec", x1, x2)
  return vectorize(matmul, signature="(n,m),(m)->(n)")(x1, x2)

