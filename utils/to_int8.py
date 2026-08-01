
def to_int8(x: jnp.ndarray, h: jnp.ndarray) -> jnp.ndarray:
  """Converts a float array to an int8 array with a scale.

  Args:
    x: Float array.
    h: Quantization scale.

  Returns:
    Int8 array.
  """
  return jnp.int8(jnp.rint(x * (MAX_INT8 / h)))

