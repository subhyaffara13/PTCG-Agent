
def positive(x):
    return +x


def positive(a: TensorLikeType) -> TensorLikeType:
    if not isinstance(a, TensorLike):
        raise AssertionError(f"a must be TensorLike, got {type(a)}")
    if a.dtype is torch.bool:
        msg = "positive does not support bool tensors."
        raise RuntimeError(msg)
    return a


def positive(x: ArrayLike, /) -> Array:
  """Return element-wise positive values of the input.

  JAX implementation of :obj:`numpy.positive`.

  Args:
    x: input array or scalar

  Returns:
    An array of same shape and dtype as ``x`` containing ``+x``.

  Note:
    ``jnp.positive`` is equivalent to ``x.copy()`` and is defined only for the
    types that support arithmetic operations.

  See also:
    - :func:`jax.numpy.negative`: Returns element-wise negative values of the input.
    - :func:`jax.numpy.sign`: Returns element-wise indication of sign of the input.

  Examples:
    For real-valued inputs:

    >>> x = jnp.array([-5, 4, 7., -9.5])
    >>> jnp.positive(x)
    Array([-5. ,  4. ,  7. , -9.5], dtype=float32)
    >>> x.copy()
    Array([-5. ,  4. ,  7. , -9.5], dtype=float32)

    For complex inputs:

    >>> x1 = jnp.array([1-2j, -3+4j, 5-6j])
    >>> jnp.positive(x1)
    Array([ 1.-2.j, -3.+4.j,  5.-6.j], dtype=complex64)
    >>> x1.copy()
    Array([ 1.-2.j, -3.+4.j,  5.-6.j], dtype=complex64)

    For uint32:

    >>> x2 = jnp.array([6, 0, -4]).astype(jnp.uint32)
    >>> x2
    Array([         6,          0, 4294967292], dtype=uint32)
    >>> jnp.positive(x2)
    Array([         6,          0, 4294967292], dtype=uint32)
  """
  return lax.asarray(*promote_args('positive', x))

