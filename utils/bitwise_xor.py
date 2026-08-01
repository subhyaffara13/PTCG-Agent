
def bitwise_xor(a: TensorLikeType, b: TensorLikeType) -> TensorLikeType:
    return prims.bitwise_xor(a, b)


def bitwise_xor(x: ArrayLike, y: ArrayLike) -> Array:
  r"""Elementwise exclusive OR: :math:`x \oplus y`.

  This function lowers directly to the `stablehlo.xor`_ operation.

  Args:
    x, y: Input arrays. Must have matching boolean or integer dtypes.
      If neither is a scalar, ``x`` and ``y`` must have the same number
      of dimensions and be broadcast compatible.

  Returns:
    An array of the same dtype as ``x`` and ``y`` containing the bitwise
    XOR of each pair of broadcasted entries.

  See also:
    - :func:`jax.numpy.bitwise_xor`: NumPy wrapper for this API, also accessible
      via the ``x ^ y`` operator on JAX arrays.
    - :func:`jax.lax.bitwise_not`: Elementwise NOT.
    - :func:`jax.lax.bitwise_and`: Elementwise AND.
    - :func:`jax.lax.bitwise_or`: Elementwise OR.

  .. _stablehlo.xor: https://openxla.org/stablehlo/spec#xor
  """
  x, y = core.auto_insert_reshard(x, y)
  return xor_p.bind(x, y)


def bitwise_xor(x: ArrayLike, y: ArrayLike, /) -> Array:
  """Compute the bitwise XOR operation elementwise.

  JAX implementation of :obj:`numpy.bitwise_xor`. This is a universal function,
  and supports the additional APIs described at :class:`jax.numpy.ufunc`.
  This function provides the implementation of the ``^`` operator for
  JAX arrays.

  Args:
    x, y: integer or boolean arrays. Must be broadcastable to a common shape.

  Returns:
    Array containing the result of the element-wise bitwise XOR.

  Examples:
    Calling ``bitwise_xor`` explicitly:

    >>> x = jnp.arange(4)
    >>> jnp.bitwise_xor(x, 1)
    Array([1, 0, 3, 2], dtype=int32)

    Calling ``bitwise_xor`` via the ``^`` operator:

    >>> x ^ 1
    Array([1, 0, 3, 2], dtype=int32)
  """
  return lax.bitwise_xor(*promote_args("bitwise_xor", x, y))

