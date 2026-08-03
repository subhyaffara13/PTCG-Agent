import logging

def _get_dummy_input_array_from_result_specs(
    result_specs: PyTree,
) -> jax.Array:
  """Returns a dummy array with replicated sharding on a mesh found in specs."""
  device_lists = set()
  devices = set()

  def _collect(x):
    if hasattr(x, 'sharding') and x.sharding is not None:
      devices.update(x.sharding.device_set)
      if isinstance(x.sharding, jax.sharding.NamedSharding):
        device_lists.add(tuple(x.sharding.mesh.devices.flatten()))

  jax.tree.map(_collect, result_specs)

  if not device_lists:
    logging.warning('No mesh found in result_specs, using sorted device set.')
    if not devices:
      devices = set(jax.devices())
    device_list = sorted(list(devices), key=lambda d: d.id)
    return get_dummy_input_array(device_list)

  # colocated_python requires all args to be on the same device list.
  if len(device_lists) > 1:
    raise ValueError(f'Multiple meshes found in result specs: {device_lists}.')
  return get_dummy_input_array(device_lists.pop())

