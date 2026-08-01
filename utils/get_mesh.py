
def get_mesh() -> Mesh:
  if not core.trace_state_clean():
    raise ValueError(
        '`get_mesh` can only be used outside of `jax.jit`. Maybe you want'
        ' `jax.sharding.get_abstract_mesh()`?')
  return get_concrete_mesh()


def get_mesh(sharding):
  if isinstance(sharding, PartitionSpec) or isinstance(sharding, tuple):
    return None
  elif isinstance(sharding, NamedSharding):
    return sharding.mesh
  elif isinstance(sharding, Format):
    return get_mesh(sharding.sharding)

