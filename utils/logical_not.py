
def logical_not(a: TensorLikeType):
    if not utils.is_boolean_dtype(a.dtype):
        return a == 0
    return ~a


def logical_not(g: jit_utils.GraphContext, input):
    return g.op("Not", g.op("Cast", input, to_i=_C_onnx.TensorProtoDataType.BOOL))


def logical_not(x: ArrayLike, /) -> Array:
  """Compute NOT bool(x) element-wise.

  JAX implementation of :func:`numpy.logical_not`.

  Args:
    x: input array of any dtype.

  Returns:
    A boolean array that computes NOT bool(x) element-wise

  See also:
    - :func:`jax.numpy.invert` or :func:`jax.numpy.bitwise_invert`: bitwise NOT operation

  Examples:
    Compute NOT x element-wise on a boolean array:

    >>> x = jnp.array([True, False, True])
    >>> jnp.logical_not(x)
    Array([False,  True, False], dtype=bool)

    For boolean input, this is equivalent to :func:`~jax.numpy.invert`, which implements
    the unary ``~`` operator:

    >>> ~x
    Array([False,  True, False], dtype=bool)

    For non-boolean input, the input of :func:`logical_not` is implicitly cast to boolean:

    >>> x = jnp.array([-1, 0, 1])
    >>> jnp.logical_not(x)
    Array([False,  True, False], dtype=bool)
  """
  return lax.bitwise_not(*map(_to_bool, promote_args("logical_not", x)))

