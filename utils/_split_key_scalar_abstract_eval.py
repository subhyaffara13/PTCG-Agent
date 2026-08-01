
def _split_key_scalar_abstract_eval(seed):
  key_shape = seed.dtype._impl.key_shape
  if len(key_shape) != 2 or key_shape[0] != 1:
    raise ValueError(f"Key shape must be (1, N), got {key_shape}")
  return [jax_core.ShapedArray((), jnp.dtype("uint32"))] * key_shape[1]

