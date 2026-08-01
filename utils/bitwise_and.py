
def bitwise_and(a: TensorLikeType, b: TensorLikeType) -> TensorLikeType:
    return prims.bitwise_and(a, b)


def bitwise_and(x: ArrayLike, y: ArrayLike) -> Array:
  r"""Elementwise AND: :math:`x \wedge y`.

  This function lowers directly to the `stablehlo.and`_ operation.

  Args:
    x, y: Input arrays. Must have matching boolean or integer dtypes.
      If neither is a scalar, ``x`` and ``y`` must have the same number
      of dimensions and be broadcast compatible.

  Returns:
    An array of the same dtype as ``x`` and ``y`` containing the bitwise
    AND of each pair of broadcasted entries.

  See also:
    - :func:`jax.numpy.bitwise_and`: NumPy wrapper for this API, also accessible
      via the ``x & y`` operator on JAX arrays.
    - :func:`jax.lax.bitwise_not`: Elementwise NOT.
    - :func:`jax.lax.bitwise_or`: Elementwise OR.
    - :func:`jax.lax.bitwise_xor`: Elementwise exclusive OR.

  .. _stablehlo.and: https://openxla.org/stablehlo/spec#and
  """
  x, y = core.auto_insert_reshard(x, y)
  return and_p.bind(x, y)


def bitwise_and(x: ArrayLike, y: ArrayLike, /) -> Array:
  """Compute the bitwise AND operation elementwise.

  JAX implementation of :obj:`numpy.bitwise_and`. This is a universal function,
  and supports the additional APIs described at :class:`jax.numpy.ufunc`.
  This function provides the implementation of the ``&`` operator for
  JAX arrays.

  Args:
    x, y: integer or boolean arrays. Must be broadcastable to a common shape.

  Returns:
    Array containing the result of the element-wise bitwise AND.

  Examples:
    Calling ``bitwise_and`` explicitly:

    >>> x = jnp.arange(4)
    >>> jnp.bitwise_and(x, 1)
    Array([0, 1, 0, 1], dtype=int32)

    Calling ``bitwise_and`` via the ``&`` operator:

    >>> x & 1
    Array([0, 1, 0, 1], dtype=int32)
  """
  return lax.bitwise_and(*promote_args("bitwise_and", x, y))


def bitwise_and(lst):
    return reduce(operator.and_, lst)

