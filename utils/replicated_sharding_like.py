
def replicated_sharding_like(
    sharding: jax.sharding.Sharding,
) -> jax.sharding.Sharding:
  """Returns a replicated sharding like the given sharding."""
  if isinstance(sharding, jax.sharding.NamedSharding):
    return jax.sharding.NamedSharding(
        sharding.mesh, jax.sharding.PartitionSpec()
    )
  return sharding

