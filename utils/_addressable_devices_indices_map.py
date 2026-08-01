
def _addressable_devices_indices_map(
    sharding: Sharding, global_shape: Shape) -> Mapping[Device, Index | None]:
  global_map = sharding.devices_indices_map(global_shape)
  if sharding.is_fully_addressable:
    return global_map
  return {d: global_map[d]
          for d in sharding._internal_device_list.addressable_device_list}

