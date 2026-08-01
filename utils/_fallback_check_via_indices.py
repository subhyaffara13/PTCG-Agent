
def _fallback_check_via_indices(src_sharding, dst_sharding, shape):
  src_indices = src_sharding.addressable_devices_indices_map(shape).values()
  dst_indices = dst_sharding.addressable_devices_indices_map(shape).values()
  return tuple(src_indices) == tuple(dst_indices)

