
def _repeat_val(val, dimension: int, repeat_count: int) -> jax.Array:
  if _is_host_array(val):
    # Ensure that host arrays are repeated on CPU, to avoid unnecessary
    # device transfers.
    return _cpu_repeat(val, repeats=repeat_count, axis=dimension)
  elif isinstance(val, np.ndarray):
    return np.repeat(val, repeat_count, axis=dimension)
  else:
    return jnp.repeat(val, repeat_count, axis=dimension)

