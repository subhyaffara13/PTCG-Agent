
def _get_out_sharding(x):
  """Compute the desired sharding of x.reshape(-1, *x.shape[2:], order='F')."""
  # We use dict because jax doesn't have out_sharding in older jax versions.
  if jax.__version__ < '0.7.0':
    return {}
  sharding = jax.typeof(x).sharding
  if sharding.mesh.are_all_axes_explicit:
    if sharding.spec:
      # The first axis is not sharded, so we simply drop it.
      spec = jax.sharding.PartitionSpec(*sharding.spec[1:])
    else:
      spec = jax.sharding.PartitionSpec()
    return {'out_sharding': jax.sharding.NamedSharding(sharding.mesh, spec)}
  return {}

