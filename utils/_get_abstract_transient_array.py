
def _get_abstract_transient_array(
    shape: tuple[int, ...],
    dtype: np.dtype,
    global_mesh: jax.sharding.Mesh,
    num_hosts: int,
) -> jax.ShapeDtypeStruct:
  """Determines the sharding strategy and shape for the transient array."""
  num_devices_per_host = jax.local_device_count()

  if _should_replicate_array(shape):
    # Cannot shard across devices, so replicate as a fallback.
    sharding = jax.sharding.NamedSharding(
        global_mesh, jax.sharding.PartitionSpec("hosts")
    )
    transient_shape = (num_hosts,) + shape
  else:
    # Enforce that the first dimension is divisible by the number of
    # devices per host. This allows us to shard the tensor across local
    # devices in host memory.
    # TODO(b/496270336): relax this constraint
    if shape[0] % num_devices_per_host != 0:
      raise ValueError(
          f"First dimension {shape[0]} is not divisible"
          f" by number of devices per host ({num_devices_per_host})."
      )
    # Fully shard across all devices. No replication. Keeps memory usage low.
    sharding = jax.sharding.NamedSharding(
        global_mesh, jax.sharding.PartitionSpec("hosts", "devices")
    )
    transient_shape = (num_hosts,) + shape

  return jax.ShapeDtypeStruct(
      shape=transient_shape, dtype=dtype, sharding=sharding
  )

