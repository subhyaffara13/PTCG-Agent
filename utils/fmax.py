
def fmax(self: torch.Tensor, other: torch.Tensor) -> torch.Tensor:
    return torch.where(torch.isnan(other) | (other < self), self, other)


def fmax(a: TensorLikeType, b: TensorLikeType) -> TensorLikeType:
    return prims.fmax(a, b)


def fmax(x1: ArrayLike, x2: ArrayLike) -> Array:
  """Return element-wise maximum of the input arrays.

  JAX implementation of :func:`numpy.fmax`.

  Args:
    x1: input array or scalar
    x2: input array or scalar. x1 and x1 must either have same shape or be
      broadcast compatible.

  Returns:
    An array containing the element-wise maximum of x1 and x2.

  Note:
    For each pair of elements, ``jnp.fmax`` returns:
      - the larger of the two if both elements are finite numbers.
      - finite number if one element is ``nan``.
      - ``nan`` if both elements are ``nan``.
      - ``inf`` if one element is ``inf`` and the other is finite or ``nan``.
      - ``-inf`` if one element is ``-inf`` and the other is ``nan``.

  Examples:
    >>> jnp.fmax(3, 7)
    Array(7, dtype=int32, weak_type=True)
    >>> jnp.fmax(5, jnp.array([1, 7, 9, 4]))
    Array([5, 7, 9, 5], dtype=int32)

    >>> x1 = jnp.array([1, 3, 7, 8])
    >>> x2 = jnp.array([-1, 4, 6, 9])
    >>> jnp.fmax(x1, x2)
    Array([1, 4, 7, 9], dtype=int32)

    >>> x3 = jnp.array([[2, 3, 5, 10],
    ...                 [11, 9, 7, 5]])
    >>> jnp.fmax(x1, x3)
    Array([[ 2,  3,  7, 10],
           [11,  9,  7,  8]], dtype=int32)

    >>> x4 = jnp.array([jnp.inf, 6, -jnp.inf, nan])
    >>> x5 = jnp.array([[3, 5, 7, nan],
    ...                 [nan, 9, nan, -1]])
    >>> jnp.fmax(x4, x5)
    Array([[ inf,   6.,   7.,  nan],
           [ inf,   9., -inf,  -1.]], dtype=float32)
  """
  # TODO(jakevdp) remove cast when jit type annotations improve
  mask = cast(Array, ufuncs.greater(x1, x2) | ufuncs.isnan(x2))
  return where(mask, x1, x2)

