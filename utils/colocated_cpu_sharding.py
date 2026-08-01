
def colocated_cpu_sharding(
    sharding: jax.sharding.Sharding,
) -> jax.sharding.Sharding:
  """Returns a CPU sharding colocated with the given sharding."""
  if isinstance(sharding, jax.sharding.SingleDeviceSharding):
    cpu_devices = cp.colocated_cpu_devices(list(sharding.device_set))
    return jax.sharding.SingleDeviceSharding(
        cpu_devices[0], memory_kind=sharding.memory_kind
    )
  if isinstance(sharding, jax.sharding.NamedSharding):
    cpu_mesh = colocated_cpu_mesh(sharding.mesh)
    return jax.sharding.NamedSharding(
        cpu_mesh, sharding.spec, memory_kind=sharding.memory_kind
    )
  raise TypeError(
      f'Sharding type {type(sharding)} not supported in to_colocated_python.'
  )

