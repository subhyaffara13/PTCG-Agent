import functools

def global_max(values: list[int]) -> list[int]:
  """Computes the global max of a list of integers across all hosts."""
  host_mesh = jax.sharding.Mesh(
      np.asarray(jax.devices()).reshape(
          process_count(), jax.local_device_count()
      ),
      ['host', 'dev'],
  )
  sharding = jax.sharding.NamedSharding(
      host_mesh, jax.sharding.PartitionSpec('host', None)
  )
  local_array = np.array([values], dtype=np.int32)
  # Create the global array, which is sharded across hosts.
  global_array = jax.make_array_from_process_local_data(sharding, local_array)

  @jax.jit
  @functools.partial(
      jax.shard_map,
      mesh=host_mesh,
      in_specs=jax.sharding.PartitionSpec('host', None),
      out_specs=jax.sharding.PartitionSpec(),
  )
  def reduce_max_fn(x):
    return jax.lax.pmax(x, axis_name='host')

  max_values_array = reduce_max_fn(global_array).squeeze(axis=0)
  return list(np.asarray(max_values_array).astype(int))

