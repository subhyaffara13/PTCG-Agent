
def _is_valid_grid_dim(dim: int | jax_typing.Array) -> bool:
  if isinstance(dim, jax_typing.Array):
    return True
  return jax_core.is_dim(dim)

