
def fully_replicated_host_local_array_to_global_array(
    arr: jax.Array,
) -> jax.Array:
  """Converts a host local array from to global jax.Array.

  In most cases, the local array is expected to have been produced by pmap.

  Args:
    arr: Host local array

  Returns:
    A global array.
  """
  # input `arr` is fully replicated, so it's shape is the global shape.
  global_shape = arr.addressable_data(0).shape

  # Create a 1D mesh to create fully replicated global jax.Array.
  mesh = jax.sharding.Mesh(np.array(jax.devices()), axis_names=('x',))
  partition_spec = (
      jax.sharding.PartitionSpec(None)
      if global_shape
      else jax.sharding.PartitionSpec()
  )
  # pmap-produced Array has a "scrambled" device order.
  dbs = sorted(
      [shard.data for shard in arr.addressable_shards],
      key=lambda x: list(x.devices())[0].id,
  )
  if global_shape != arr.shape:
    dbs = [s[0] for s in dbs]
    global_shape = global_shape[1:]
  result = jax.make_array_from_single_device_arrays(
      global_shape, jax.sharding.NamedSharding(mesh, partition_spec), dbs
  )
  return result

