
def _local_device_indices(local_sharding, shape):
  """Cached device indices for slicing arrays."""
  return tuple(local_sharding.devices_indices_map(shape).values())

