
def jax_to_nnx_path(jax_path: tuple, /):
  return tuple(_key_path_to_key(part) for part in jax_path)

