
def __array_module__(self, types):
  if all(issubclass(t, _HANDLED_ARRAY_TYPES) for t in types):
    import jax.numpy  # pyrefly: ignore[missing-import]
    return jax.numpy
  else:
    return NotImplemented

