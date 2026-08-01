
def make_single_device_sharding(device, *, memory_kind=None):
  return jax.sharding.SingleDeviceSharding(device, memory_kind=memory_kind)


def make_single_device_sharding(device, *, memory_kind=None):
  return SingleDeviceSharding(device, memory_kind=memory_kind)

