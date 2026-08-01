
def bitwise_count(x: ArrayLike, /) -> Array:
  r"""Counts the number of 1 bits in the binary representation of the absolute value
  of each element of ``x``.

  JAX implementation of :obj:`numpy.bitwise_count`.

  Args:
    x: Input array, only accepts integer subtypes

  Returns:
    An array-like object containing the binary 1 bit counts of the absolute value of
    each element in ``x``, with the same shape as ``x`` of dtype uint8.

  Examples:
    >>> x1 = jnp.array([64, 32, 31, 20])
    >>> # 64 = 0b1000000, 32 = 0b100000, 31 = 0b11111, 20 = 0b10100
    >>> jnp.bitwise_count(x1)
    Array([1, 1, 5, 2], dtype=uint8)

    >>> x2 = jnp.array([-16, -7, 7])
    >>> # |-16| = 0b10000, |-7| = 0b111, 7 = 0b111
    >>> jnp.bitwise_count(x2)
    Array([1, 3, 3], dtype=uint8)

    >>> x3 = jnp.array([[2, -7],[-9, 7]])
    >>> # 2 = 0b10, |-7| = 0b111, |-9| = 0b1001, 7 = 0b111
    >>> jnp.bitwise_count(x3)
    Array([[1, 3],
           [2, 3]], dtype=uint8)
  """
  x, = promote_args_numeric("bitwise_count", x)
  # Following numpy we take the absolute value and return uint8.
  return lax.population_count(abs(x)).astype('uint8')

