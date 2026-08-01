
def _fm32_to_float32(value):
  if value.dtype == fm32:
    return lax.convert_element_type(value, jnp.float32)
  return value

