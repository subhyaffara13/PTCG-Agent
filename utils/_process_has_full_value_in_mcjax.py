
def _process_has_full_value_in_mcjax(s, shape):
  # Return False for single host as a fast path.
  if xla_bridge.process_count() == 1:
    return False

  num_unique_indices = len(
      {hashed_index(v) for v in s.devices_indices_map(shape).values()})
  num_addressable_unique_indices = len(
      {hashed_index(v) for v in s.addressable_devices_indices_map(shape).values()})
  return num_unique_indices == num_addressable_unique_indices

