
def get_large_negative_number(dtype):
  # temp WAR as cuDNN has a bug for subtraction between two large negative value
  if dtype == np.dtype('bfloat16'):
    return jnp.asarray(-2 << 40, dtype=dtype)
  elif dtype == np.dtype('float16'):
    return jnp.asarray(-2 << 14, dtype=dtype)
  else:
    raise ValueError("Unsupported dtype for inputs.")

