
def replicate_sharded_array(arr: jax.Array):
  """Returns the input array, but replicated across all devices."""
  mesh = jax.sharding.Mesh(np.asarray(jax.devices()), ('x',))
  replicated_sharding = jax.sharding.NamedSharding(
      mesh,
      jax.sharding.PartitionSpec(
          None,
      ),
  )
  return pjit.pjit(lambda x: x, out_shardings=replicated_sharding)(arr)

