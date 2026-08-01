
def negative(mode: str = "RGB") -> ImagePalette:
    palette = list(range(256 * len(mode)))
    palette.reverse()
    return ImagePalette(mode, [i // len(mode) for i in palette])


def negative(x: ArrayLike, /) -> Array:
  """Return element-wise negative values of the input.

  JAX implementation of :obj:`numpy.negative`.

  Args:
    x: input array or scalar.

  Returns:
    An array with same shape and dtype as ``x`` containing ``-x``.

  See also:
    - :func:`jax.numpy.positive`: Returns element-wise positive values of the input.
    - :func:`jax.numpy.sign`: Returns element-wise indication of sign of the input.

  Note:
    ``jnp.negative``, when applied over ``unsigned integer``, produces the result
    of their two's complement negation, which typically results in unexpected
    large positive values due to integer underflow.

  Examples:
    For real-valued inputs:

    >>> x = jnp.array([0., -3., 7])
    >>> jnp.negative(x)
    Array([-0.,  3., -7.], dtype=float32)

    For complex inputs:

    >>> x1 = jnp.array([1-2j, -3+4j, 5-6j])
    >>> jnp.negative(x1)
    Array([-1.+2.j,  3.-4.j, -5.+6.j], dtype=complex64)

    For unit32:

    >>> x2 = jnp.array([5, 0, -7]).astype(jnp.uint32)
    >>> x2
    Array([         5,          0, 4294967289], dtype=uint32)
    >>> jnp.negative(x2)
    Array([4294967291,          0,          7], dtype=uint32)
  """
  return lax.neg(*promote_args('negative', x))

