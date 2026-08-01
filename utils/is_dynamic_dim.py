
def is_dynamic_dim(d) -> bool:
  return d is None or not jax_core.is_constant_dim(d)

