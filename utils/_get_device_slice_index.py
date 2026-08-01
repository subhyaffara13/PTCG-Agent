
def _get_device_slice_index(device: jax.Device) -> int | None:
  if hasattr(device, 'slice_index') and device.slice_index is not None:
    return int(device.slice_index)
  return None

