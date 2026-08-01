
def is_dtype_str(dtype) -> bool:
  """Returns True if the dtype is `str`."""
  # tf.string.as_numpy_dtype is object
  try:
    dtype = np.dtype(dtype)
  except TypeError:  # `jax.random.PRNGKeyArray` fail.
    return False
  return dtype.type in {np.object_, np.str_, np.bytes_}

