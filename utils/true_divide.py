
def true_divide(a: TensorLikeType, b: TensorLikeType) -> TensorLikeType:
    return prims.div(a, b)


def true_divide(g: jit_utils.GraphContext, self, other):
    """Division where both inputs are cast to floating types

    If both inputs are floating, performs div as usual
    If only one input is a floating type, the other input is cast to its type
    If neither input is a floating type, both inputs are cast to the default scalar type
    """

    # Case 1: either values are floating
    # Performs div as usual.
    # Implicit casting will be handled in scalar type analysis pass.
    if symbolic_helper._is_fp(self) or symbolic_helper._is_fp(other):
        return g.op("Div", self, other)

    # Case 2: neither is floating
    # Casts both inputs to the default scalar type
    scalar_type = torch.get_default_dtype()
    onnx_scalar_type = _C_onnx.TensorProtoDataType.FLOAT
    if scalar_type is not torch.float and scalar_type is not torch.double:
        raise AssertionError(f"Expected float or double, got {scalar_type}")
    if torch.get_default_dtype() is torch.double:
        onnx_scalar_type = _C_onnx.TensorProtoDataType.DOUBLE

    self = g.op("Cast", self, to_i=onnx_scalar_type)
    other = g.op("Cast", other, to_i=onnx_scalar_type)
    return g.op("Div", self, other)


def true_divide(x1: ArrayLike, x2: ArrayLike, /) -> Array:
  """Calculates the division of x1 by x2 element-wise

  JAX implementation of :func:`numpy.true_divide`.

  Args:
    x1: Input array, the dividend
    x2: Input array, the divisor

  Returns:
    An array containing the elementwise quotients, will always use
    floating point division.

  Examples:
    >>> x1 = jnp.array([3, 4, 5])
    >>> x2 = 2
    >>> jnp.true_divide(x1, x2)
    Array([1.5, 2. , 2.5], dtype=float32)

    >>> x1 = 24
    >>> x2 = jnp.array([3, 4, 6j])
    >>> jnp.true_divide(x1, x2)
    Array([8.+0.j, 6.+0.j, 0.-4.j], dtype=complex64)

    >>> x1 = jnp.array([1j, 9+5j, -4+2j])
    >>> x2 = 3j
    >>> jnp.true_divide(x1, x2)
    Array([0.33333334+0.j       , 1.6666666 -3.j       ,
           0.6666667 +1.3333334j], dtype=complex64)

  See Also:
    :func:`jax.numpy.floor_divide` for integer division
  """
  x1, x2 = promote_args_inexact("true_divide", x1, x2)
  jnp_error._set_error_if_divide_by_zero(x2)
  out = lax.div(x1, x2)
  jnp_error._set_error_if_nan(out)
  return out

