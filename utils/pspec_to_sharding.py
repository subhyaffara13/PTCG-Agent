
def pspec_to_sharding(name, val):
  if isinstance(val, P):
    mesh = get_concrete_mesh()
    if mesh.empty:
      raise ValueError(
          "Please set a mesh via `jax.set_mesh` if a PartitionSpec is"
          f" passed to {name}")
    return NamedSharding(mesh, val)
  return val

