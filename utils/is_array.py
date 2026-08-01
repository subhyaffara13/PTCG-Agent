
def is_array(checker, instance):
    return isinstance(instance, list)


def is_array(x: Any) -> bool:
  """Returns `True` if array is np or `jnp` array."""
  if isinstance(x, np.ndarray):
    return True
  elif lazy.has_jax and isinstance(x, lazy.jnp.ndarray):
    return True
  else:
    return False

