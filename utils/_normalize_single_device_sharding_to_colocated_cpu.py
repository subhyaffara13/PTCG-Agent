
def _normalize_single_device_sharding_to_colocated_cpu(
    sharding: jax.sharding.SingleDeviceSharding,
) -> jax.sharding.SingleDeviceSharding:
  device = next(iter(sharding.device_set))
  if _device_platform(device) == 'cpu':
    return sharding
  return jax.sharding.SingleDeviceSharding(
      _to_serializable_cpu_device(device), memory_kind=sharding.memory_kind
  )

