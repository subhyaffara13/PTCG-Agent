
def device_replica_id_map(sharding, global_shape: Shape) -> Mapping[Device, int]:
  try:
    device_indices_map_fn = sharding.devices_indices_map
  except AttributeError:
    raise ValueError(
        f'Cannot calculate replica ids from sharding: {sharding}. Please '
        'create a device to index mapping for your sharding from which replica '
        'ids will be calculated.') from None

  index_to_replica: dict[int, int] = collections.Counter()
  out = {}
  for device, index in device_indices_map_fn(global_shape).items():
    h_index = hashed_index(index)
    replica_id = index_to_replica[h_index]
    index_to_replica[h_index] += 1
    out[device] = replica_id
  return out

