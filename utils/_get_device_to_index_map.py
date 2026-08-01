
def _get_device_to_index_map(
    global_shape: Shape, sharding: jax.sharding.Sharding
) -> Mapping[jax.Device, Index]:
  return sharding.devices_indices_map(global_shape)

