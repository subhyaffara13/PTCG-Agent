
def get_quantization_scales(x: jnp.ndarray) -> jnp.ndarray:
  """Computes the quantization scales for a float array.

  These are the maximum values of the trailing dimension.

  Args:
    x: Float array to quantize.

  Returns:
    Array of the same shape as input but with the trailing dimension reduced to
    a size 1 absolute max value.
  """
  return jnp.max(jnp.abs(x), axis=-1, keepdims=True)

