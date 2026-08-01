
def _to_serializable_cpu_device(device: jax.Device) -> jax.Device:
  """Normalizes a device to the CPU device used by colocated Python."""
  if device.platform == 'cpu':
    return device
  return cp.colocated_cpu_devices((device,))[0]

