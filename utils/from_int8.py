
def from_int8(
    x: jnp.ndarray, h: jnp.ndarray, dtype: jnp.dtype = jnp.bfloat16
) -> jnp.ndarray:
  """Converts an int8 array to a float array with a scale.

  Args:
    x: Int8 array.
    h: Quantization scale.
    dtype: Float dtype to convert to.

  Returns:
    Float array.
  """
  return x.astype(dtype) * h / MAX_INT8

