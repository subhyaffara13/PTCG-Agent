
def unquantize_from_int8(
    x: QuantizedTensor,
    dtype: jnp.dtype = jnp.bfloat16,
) -> jnp.ndarray:
  """Unquantizes an int8 QuantizedTensor to a float array.

  Args:
    x: Int8 QuantizedTensor to unquantize.
    dtype: Float dtype to unquantize to.

  Returns:
    Float array.
  """
  return from_int8(x.weight, x.scales, dtype)

