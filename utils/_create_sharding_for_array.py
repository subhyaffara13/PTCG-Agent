
def _create_sharding_for_array(mesh, x, name, api_name):
  if x is None:
    if api_name == 'jit' or mesh.empty:
      return UNSPECIFIED
    return sharding_impls.cached_named_sharding(mesh, PartitionSpec())
  if isinstance(x, (UnspecifiedValue, Sharding)):
    return x
  if mesh.empty:
    raise RuntimeError(
        f'{api_name} requires a non-empty mesh in context if you are passing'
        f' `PartitionSpec`s to {name}. You can define a context mesh via'
        ' `jax.set_mesh(mesh)`. Alternatively, provide `Sharding`s to'
        f' {name} and then the mesh context manager is not required.')
  assert isinstance(x, PartitionSpec), x
  return sharding_impls.cached_named_sharding(mesh, x)

