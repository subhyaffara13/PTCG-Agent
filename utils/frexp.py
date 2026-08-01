
def frexp(self: TensorLikeType) -> tuple[TensorLikeType, TensorLikeType]:
    return torch.return_types.frexp(prims.frexp(self))


def frexp(x):
    # TODO(isuruf): use inline_asm_elementwise here
    y = libdevice.ilogb(x) + 1
    exponent = tl.where(x == 0, 0, y)
    mantissa = tl.where(x == 0, 0, libdevice.ldexp(x, -y))
    return mantissa, exponent


def frexp(x: ArrayLike, /) -> tuple[Array, Array]:
  """Split floating point values into mantissa and twos exponent.

  JAX implementation of :func:`numpy.frexp`.

  Args:
    x: real-valued array

  Returns:
    A tuple ``(mantissa, exponent)`` where ``mantissa`` is a floating point
    value between -1 and 1, and ``exponent`` is an integer such that
    ``x == mantissa * 2 ** exponent``.

  See also:
    - :func:`jax.numpy.ldexp`: compute the inverse of ``frexp``.

  Examples:
    Split values into mantissa and exponent:

    >>> x = jnp.array([1., 2., 3., 4., 5.])
    >>> m, e = jnp.frexp(x)
    >>> m
    Array([0.5  , 0.5  , 0.75 , 0.5  , 0.625], dtype=float32)
    >>> e
    Array([1, 2, 2, 3, 3], dtype=int32)

    Reconstruct the original array:

    >>> m * 2 ** e
    Array([1., 2., 3., 4., 5.], dtype=float32)
  """
  x = ensure_arraylike("frexp", x)
  x, = promote_dtypes_inexact(x)
  if dtypes.issubdtype(x.dtype, np.complexfloating):
    raise TypeError("frexp does not support complex-valued inputs")
  return _frexp(x)

