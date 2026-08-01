
def bitwise_or(a: TensorLikeType, b: TensorLikeType) -> TensorLikeType:
    return prims.bitwise_or(a, b)


def bitwise_or(g, self, other):
    if not symbolic_helper._is_bool(self):
        raise errors.SymbolicValueError(
            "ONNX export does NOT support exporting bitwise OR "
            "for non-boolean input values. self: ",
            self,
        )
    if not symbolic_helper._is_bool(other):
        raise errors.SymbolicValueError(
            "ONNX export does NOT support exporting bitwise OR "
            "for non-boolean input values. other: ",
            other,
        )
    return g.op("Or", self, other)


def bitwise_or(x: ArrayLike, y: ArrayLike) -> Array:
  r"""Elementwise OR: :math:`x \vee y`.

  This function lowers directly to the `stablehlo.or`_ operation.

  Args:
    x, y: Input arrays. Must have matching boolean or integer dtypes.
      If neither is a scalar, ``x`` and ``y`` must have the same number
      of dimensions and be broadcast compatible.

  Returns:
    An array of the same dtype as ``x`` and ``y`` containing the bitwise
    OR of each pair of broadcasted entries.

  See also:
    - :func:`jax.numpy.invert`: NumPy wrapper for this API, also accessible
      via the ``x | y`` operator on JAX arrays.
    - :func:`jax.lax.bitwise_not`: Elementwise NOT.
    - :func:`jax.lax.bitwise_and`: Elementwise AND.
    - :func:`jax.lax.bitwise_xor`: Elementwise exclusive OR.

  .. _stablehlo.or: https://openxla.org/stablehlo/spec#or
  """
  x, y = core.auto_insert_reshard(x, y)
  return or_p.bind(x, y)


def bitwise_or(x: ArrayLike, y: ArrayLike, /) -> Array:
  """Compute the bitwise OR operation elementwise.

  JAX implementation of :obj:`numpy.bitwise_or`. This is a universal function,
  and supports the additional APIs described at :class:`jax.numpy.ufunc`.
  This function provides the implementation of the ``|`` operator for
  JAX arrays.

  Args:
    x, y: integer or boolean arrays. Must be broadcastable to a common shape.

  Returns:
    Array containing the result of the element-wise bitwise OR.

  Examples:
    Calling ``bitwise_or`` explicitly:

    >>> x = jnp.arange(4)
    >>> jnp.bitwise_or(x, 1)
    Array([1, 1, 3, 3], dtype=int32)

    Calling ``bitwise_or`` via the ``|`` operator:

    >>> x | 1
    Array([1, 1, 3, 3], dtype=int32)
  """
  return lax.bitwise_or(*promote_args("bitwise_or", x, y))


def bitwise_or(lst):
    return reduce(operator.or_, lst)

