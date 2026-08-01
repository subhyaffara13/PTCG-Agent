
def _unreduce_single_device_sharding(
    device_id: int, memory_kind: str | None
) -> jax.sharding.SingleDeviceSharding:
  cpu_device_map = _get_cpu_device_map()
  device = _lookup_cpu_device(cpu_device_map, device_id)
  return jax.sharding.SingleDeviceSharding(device, memory_kind=memory_kind)

